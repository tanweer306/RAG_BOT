from fastapi import Request
import hashlib
from typing import Dict, Optional, List
import uuid
from datetime import datetime, timedelta
from app.config import settings
from app.services.supabase_service import SupabaseService

class SessionService:
    
    @staticmethod
    def get_client_identifier(request: Request) -> str:
        """
        Generate unique identifier from client IP and user agent
        This creates a stable session ID that persists across page reloads
        """
        # Get client IP (handle proxy/load balancer headers)
        client_ip = (
            request.headers.get("X-Forwarded-For", "").split(",")[0].strip()
            or request.headers.get("X-Real-IP", "")
            or request.client.host
        )
        
        # Get user agent for additional uniqueness
        user_agent = request.headers.get("User-Agent", "unknown")
        
        # Create stable hash from IP + partial user agent
        identifier = f"{client_ip}_{user_agent[:50]}"
        session_id = hashlib.sha256(identifier.encode()).hexdigest()[:32]
        
        return session_id
    
    @staticmethod
    def get_or_create_session(request: Request) -> dict:
        """
        Get existing session by IP or create new one
        This ensures same user always gets same session
        """
        session_id = SessionService.get_client_identifier(request)
        
        # Check if session exists in Supabase (raw check)
        session = SupabaseService.get_session(session_id)
        
        if session:
            # Check expiry logic here too?
            # If expired, we might want to clean it up and create new, or just reset.
            # Existing get_session handles expiry deletion.
            # But for get_or_create, if it's expired, we probably want a fresh one or re-activate.
            # For now, simple update.
            SupabaseService.update_session_activity(session_id, request)
            return session
        else:
            # Create new session
            return SupabaseService.create_session(
                session_id=session_id,
                ip_address=request.client.host,
                user_agent=request.headers.get("User-Agent", "")
            )

    @staticmethod
    def create_session() -> str:
        """Legacy create session (random) - kept for compatibility if needed"""
        session_id = str(uuid.uuid4())
        SupabaseService.create_session(session_id)
        return session_id
    
    @staticmethod
    def get_session(session_id: str) -> Optional[Dict]:
        """Get session data with documents and recent history"""
        try:
            # 1. Get Session
            session = SupabaseService.get_session(session_id)
            if not session:
                return None
            
            # 2. Check Expiry
            # Handle timezone offset mismatch safely
            try:
                last_active = datetime.fromisoformat(session["last_active"])
                if last_active.tzinfo:
                    last_active = last_active.replace(tzinfo=None)
                
                if datetime.now() - last_active > timedelta(hours=settings.SESSION_TIMEOUT_HOURS):
                    SupabaseService.delete_session(session_id)
                    return None
            except Exception as e:
                print(f"Error checking session expiry: {e}")
                # If date parsing fails, assume session is valid or invalid?
                # Safe to proceed and update activity.
            
            # 3. Update Activity
            SupabaseService.update_session_activity(session_id)
            
            # 4. Fetch Documents
            documents = SupabaseService.get_session_documents(session_id)
            
            # 5. Fetch Chat History (limit to last 50 for context and summarization)
            history = SupabaseService.get_chat_history(session_id, limit=50)
            
            # 6. Construct Legacy Dict Structure
            return {
                "session_id": session_id,
                "created_at": session["created_at"],
                "last_active": session["last_active"],
                "language": session.get("language", "en"),
                "documents": documents,
                "conversation_history": history,
                # Add new fields if helpful
                "total_documents": len(documents),
                "total_messages": len(history)
            }
        except Exception as e:
            print(f"Error getting session from Supabase: {e}")
            # Fallback: return basic session structure
            return {
                "session_id": session_id,
                "created_at": datetime.now().isoformat(),
                "last_active": datetime.now().isoformat(),
                "language": "en",
                "documents": [],
                "conversation_history": [],
                "total_documents": 0,
                "total_messages": 0
            }
    
    @staticmethod
    def update_session(session_id: str, data: Dict):
        """Update session data (mostly activity)"""
        SupabaseService.update_session_activity(session_id)
    
    @staticmethod
    def delete_session(session_id: str):
        """Delete session"""
        SupabaseService.delete_session(session_id)
    
    @staticmethod
    def add_document(session_id: str, document: Dict):
        """Add document to session"""
        # Schema expectations: session_id, filename, file_url, chunks_count, qdrant_point_ids (if any), expires_at
        doc_data = {
            "session_id": session_id,
            "filename": document.get("filename"),
            "file_url": document.get("file_url", ""),
            "chunks_count": document.get("chunks", 0),
            "expires_at": (datetime.now() + timedelta(days=7)).isoformat(),
            "uploaded_at": datetime.now().isoformat(),
            "metadata": document.get("metadata", {})
        }
        SupabaseService.create_document(doc_data)
    
    @staticmethod
    def add_message(session_id: str, role: str, content: str):
        """Add message to conversation history"""
        SupabaseService.add_message(session_id, role, content)
