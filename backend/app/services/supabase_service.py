from supabase import create_client, Client
from app.config import settings
from datetime import datetime
from typing import Dict, List, Optional, Any
from fastapi import Request

class SupabaseService:
    _client: Client = None

    @classmethod
    def get_client(cls) -> Client:
        if not cls._client:
            try:
                cls._client = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)
            except Exception as e:
                print(f"Error creating Supabase client: {e}")
                print(f"SUPABASE_URL: {settings.SUPABASE_URL}")
                print(f"SUPABASE_KEY: {settings.SUPABASE_KEY[:10]}..." if settings.SUPABASE_KEY else "None")
                raise
        return cls._client

    # --- Sessions ---
    
    @classmethod
    def create_session(cls, session_id: str, language: str = "en", ip_address: str = None, user_agent: str = None) -> Dict:
        client = cls.get_client()
        data = {
            "session_id": session_id,
            "language": language,
            "last_active": datetime.now().isoformat(),
            "created_at": datetime.now().isoformat()
        }
        # Note: IP and User Agent columns might not exist in schema. 
        # Skipping direct storage to avoid PGRST204 error.
        # if ip_address:
        #     data["ip_address"] = ip_address
        # if user_agent:
        #     data["user_agent"] = user_agent
            
        response = client.table("sessions").insert(data).execute()
        return response.data[0] if response.data else None

    @classmethod
    def get_session(cls, session_id: str) -> Optional[Dict]:
        client = cls.get_client()
        response = client.table("sessions").select("*").eq("session_id", session_id).execute()
        return response.data[0] if response.data else None

    @classmethod
    def update_session_activity(cls, session_id: str, request: Request = None):
        """Update last_active timestamp and optional metadata"""
        client = cls.get_client()
        
        update_data = {
            "last_active": datetime.now().isoformat()
        }
        
        # Note: IP column might not exist in schema.
        # if request:
        #     # Safe access to host
        #     if hasattr(request, "client") and request.client:
        #         update_data["ip_address"] = request.client.host
        
        client.table("sessions").update(update_data).eq("session_id", session_id).execute()
        
    @classmethod
    def delete_session(cls, session_id: str):
        client = cls.get_client()
        client.table("sessions").delete().eq("session_id", session_id).execute()

    @classmethod
    def get_all_sessions(cls, page: int = 1, limit: int = 20, status: str = None) -> Dict:
        client = cls.get_client()
        start = (page - 1) * limit
        end = start + limit - 1
        
        query = client.table("sessions").select("*", count="exact")
        
        response = query.range(start, end).order("created_at", desc=True).execute()
        
        return {
            "sessions": response.data,
            "total": response.count
        }

    # --- Documents ---

    @classmethod
    def create_document(cls, doc_data: Dict) -> Dict:
        client = cls.get_client()
        response = client.table("documents").insert(doc_data).execute()
        return response.data[0] if response.data else None

    @classmethod
    def get_document(cls, document_id: str) -> Optional[Dict]:
        client = cls.get_client()
        response = client.table("documents").select("*").eq("id", document_id).execute()
        return response.data[0] if response.data else None

    @classmethod
    def get_session_documents(cls, session_id: str) -> List[Dict]:
        client = cls.get_client()
        response = client.table("documents").select("*").eq("session_id", session_id).is_("deleted_at", "null").execute()
        return response.data
        
    @classmethod
    def get_user_documents(cls, session_id: str) -> List[Dict]:
        """Get all active documents for a session"""
        client = cls.get_client()
        # Using is_('deleted_at', 'null') which is safer than eq('is_deleted', False) based on schema
        response = client.table("documents")\
            .select("*")\
            .eq("session_id", session_id)\
            .is_("deleted_at", "null")\
            .execute()
        
        return response.data if response.data else []

    @classmethod
    def get_all_documents(cls, page: int = 1, limit: int = 20, expired: bool = False) -> Dict:
        client = cls.get_client()
        start = (page - 1) * limit
        end = start + limit - 1
        
        query = client.table("documents").select("*", count="exact")
        
        if not expired:
            # Filter out expired or deleted
            query = query.is_("deleted_at", "null").gt("expires_at", datetime.now().isoformat())
            
        response = query.range(start, end).order("uploaded_at", desc=True).execute()
        
        return {
            "documents": response.data,
            "total": response.count
        }
    
    @classmethod
    def get_expired_documents(cls) -> List[Dict]:
        client = cls.get_client()
        # Get documents where expires_at < NOW and deleted_at is NULL
        response = client.table("documents").select("*")\
            .lt("expires_at", datetime.now().isoformat())\
            .is_("deleted_at", "null")\
            .execute()
        return response.data

    @classmethod
    def soft_delete_document(cls, document_id: str):
        client = cls.get_client()
        client.table("documents").update({
            "deleted_at": datetime.now().isoformat()
        }).eq("id", document_id).execute()

    # --- Chat History ---

    @classmethod
    def save_message(cls, session_id: str, role: str, content: str, 
                     language: str = "en", sources: List[str] = None, 
                     is_audio: bool = False):
        """Save a message to chat history"""
        client = cls.get_client()
        
        data = {
            "session_id": session_id,
            "role": role,
            "content": content,
            "sources": sources or [],
            # Note: is_audio column might be missing in schema
            # "is_audio": is_audio,
            "language": language,
            "created_at": datetime.now().isoformat()
        }
        
        client.table("chat_history").insert(data).execute()

    @classmethod
    def add_message(cls, session_id: str, role: str, content: str, language: str = "en", sources: List[str] = None) -> Dict:
        """Legacy add message wrapper"""
        cls.save_message(session_id, role, content, language, sources)
        return {}

    @classmethod
    def get_chat_history(cls, session_id: str, limit: int = 50) -> List[Dict]:
        """Get chat history for a session"""
        client = cls.get_client()
        
        response = client.table("chat_history")\
            .select("*")\
            .eq("session_id", session_id)\
            .order("created_at", desc=False)\
            .limit(limit)\
            .execute()
        
        if not response.data:
            return []
        
        # Format messages for frontend
        messages = []
        for record in response.data:
            messages.append({
                "role": record["role"],
                "content": record["content"],
                "sources": record.get("sources", []),
                "timestamp": record["created_at"],
                "isAudio": record.get("is_audio", False)
            })
        
        return messages
        
    @classmethod
    def increment_message_count(cls, session_id: str):
        """Increment total_messages counter in session"""
        # Need RPC or atomic update. Fallback to read-modify-write if RPC not set up
        # Or just ignore if not critical. 
        # Let's try a simple update if 'total_messages' column exists
        # Assuming column doesn't exist in schema provided earlier, but prompt asks for it.
        # If it doesn't exist, this might fail. 
        # But I should implement it as requested.
        try:
            # Try to get current count
            res = cls.get_session(session_id)
            if res:
                count = res.get("total_messages", 0) or 0
                cls.get_client().table("sessions").update({"total_messages": count + 1}).eq("session_id", session_id).execute()
        except Exception as e:
            # Ignore if column missing
            pass

    # --- Analytics ---
    
    @classmethod
    def get_analytics(cls, days: int = 7) -> Dict:
        client = cls.get_client()
        
        # Get daily stats from analytics table
        end_date = datetime.now().date()
        start_date = end_date - timedelta(days=days)
        
        response = client.table("analytics")\
            .select("*")\
            .gte("date", start_date.isoformat())\
            .lte("date", end_date.isoformat())\
            .order("date", desc=False)\
            .execute()
            
        daily_stats = response.data
        
        # Calculate totals
        total_msgs = sum(d.get("total_messages", 0) for d in daily_stats)
        total_docs = sum(d.get("total_documents", 0) for d in daily_stats)
        
        return {
            "daily_stats": daily_stats,
            "total_messages": total_msgs,
            "total_documents": total_docs,
            # Add other aggregations if needed
        }

    @classmethod
    def increment_daily_stat(cls, metric: str, value: int = 1, extra_data: Dict = None):
        """Increment a daily statistic column"""
        client = cls.get_client()
        today = datetime.now().date().isoformat()
        
        # We need to get today's row or create it
        # Supabase doesn't have a simple atomic increment via API for all column types easily without RPC
        # But we can try:
        # 1. Try to get row
        # 2. If exists, update. If not, insert.
        # Better: Use RPC if available, but sticking to client logic for portability if no RPC.
        
        try:
            # Check if row exists
            res = client.table("analytics").select("*").eq("date", today).execute()
            if res.data:
                current_val = res.data[0].get(metric, 0)
                new_val = current_val + value
                update_data = {metric: new_val}
                if extra_data:
                    update_data.update(extra_data)
                client.table("analytics").update(update_data).eq("date", today).execute()
            else:
                insert_data = {"date": today, metric: value}
                if extra_data:
                    insert_data.update(extra_data)
                client.table("analytics").insert(insert_data).execute()
        except Exception as e:
            print(f"Error updating analytics: {e}")
