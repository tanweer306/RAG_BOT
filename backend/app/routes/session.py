from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel
from app.services.session_service import SessionService

router = APIRouter()

class LanguageUpdate(BaseModel):
    language: str

@router.post("/session")
async def create_session(request: Request):
    """Create or get existing session based on client IP"""
    session = SessionService.get_or_create_session(request)
    # Return dict matching what frontend might expect, or just session_id
    return {
        "session_id": session["session_id"],
        "message": "Session ready",
        "is_existing": True # Since we get_or_create, effectively it exists now
    }

@router.get("/session/current")
async def get_current_session(request: Request):
    """Get current session without creating new one"""
    session_id = SessionService.get_client_identifier(request)
    session = SessionService.get_session(session_id)
    
    if not session:
        # Prompt says return specific structure if not exists
        return {"session_id": None, "exists": False}
    
    return {
        "session_id": session_id,
        "exists": True,
        "language": session.get("language", "en"),
        "documents_count": session.get("total_documents", 0),
        "messages_count": session.get("total_messages", 0)
    }

@router.post("/session/language")
async def update_language(request: Request, data: LanguageUpdate):
    """Update session language"""
    session_id = SessionService.get_client_identifier(request)
    session = SessionService.get_session(session_id)
    
    if not session:
         # Should we create it? Or fail? 
         # If user changes language, they probably should have a session. 
         # Let's create if missing or just fail. 
         # Safer to fail if "current" implies active session. 
         # But if we want seamless, maybe create?
         # Prompt implementation for create_session uses get_or_create.
         # Let's stick to fail if not found for now, or get_or_create.
         # I'll use get_or_create logic to ensure smooth UX.
         session = SessionService.get_or_create_session(request)
         session_id = session["session_id"]
    
    SessionService.update_session(session_id, {"language": data.language})
    return {"message": "Language updated successfully", "language": data.language}

@router.delete("/session")
async def delete_session(request: Request):
    """Delete current session"""
    session_id = SessionService.get_client_identifier(request)
    SessionService.delete_session(session_id)
    return {"message": "Session deleted successfully"}
