from fastapi import APIRouter, Depends, HTTPException, Header, Query
from typing import Dict, List
from app.config import settings
from app.services.supabase_service import SupabaseService
from app.services.cleanup_service import CleanupService
from app.services.embedding_service import EmbeddingService

router = APIRouter()

async def verify_admin(authorization: str = Header(None)):
    """Simple token authentication for admin routes"""
    if not authorization:
        raise HTTPException(status_code=401, detail="Authorization header missing")
    
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid authorization format")
    
    token = authorization.split(" ")[1]
    if token != settings.ADMIN_PASSWORD:
        raise HTTPException(status_code=401, detail="Invalid admin token")
    return True

@router.get("/admin/stats", dependencies=[Depends(verify_admin)])
async def get_stats():
    """Get dashboard statistics"""
    analytics = SupabaseService.get_analytics(days=7)
    
    # Get current counts for sessions and docs (snapshot)
    # We can use get_all_sessions/docs limits to get total count if implemented
    sessions_data = SupabaseService.get_all_sessions(limit=1)
    docs_data = SupabaseService.get_all_documents(limit=1)
    
    return {
        "total_sessions": sessions_data["total"],
        "total_documents": docs_data["total"],
        "total_messages": analytics.get("total_messages", 0),
        # "storage_used_mb": 450, # Would need to sum file sizes if stored
        "daily_stats": analytics.get("daily_stats", [])
    }

@router.get("/admin/sessions", dependencies=[Depends(verify_admin)])
async def get_sessions(page: int = 1, limit: int = 20, status: str = None):
    """List all sessions"""
    return SupabaseService.get_all_sessions(page, limit, status)

@router.get("/admin/sessions/{session_id}", dependencies=[Depends(verify_admin)])
async def get_session_details(session_id: str):
    """Get details for a specific session"""
    session = SupabaseService.get_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    documents = SupabaseService.get_session_documents(session_id)
    history = SupabaseService.get_chat_history(session_id, limit=100)
    
    return {
        "session": session,
        "documents": documents,
        "chat_history": history
    }

@router.delete("/admin/sessions/{session_id}", dependencies=[Depends(verify_admin)])
async def delete_session(session_id: str):
    """Delete a session and its data"""
    # Delete documents first (vectors + storage)
    docs = SupabaseService.get_session_documents(session_id)
    for doc in docs:
        await EmbeddingService.delete_document_vectors(session_id, doc["filename"])
        # If Cloudinary deletion implemented, call it here
        SupabaseService.soft_delete_document(doc["id"])
    
    SupabaseService.delete_session(session_id)
    return {"message": "Session deleted successfully"}

@router.get("/admin/documents", dependencies=[Depends(verify_admin)])
async def get_documents(page: int = 1, limit: int = 20, expired: bool = False):
    """List all documents"""
    return SupabaseService.get_all_documents(page, limit, expired)

@router.delete("/admin/documents/{document_id}", dependencies=[Depends(verify_admin)])
async def delete_document(document_id: str):
    """Delete a document"""
    # Get document details to find session_id and filename
    doc = SupabaseService.get_document(document_id)
    
    if doc:
        # Delete vectors
        await EmbeddingService.delete_document_vectors(doc["session_id"], doc["filename"])
        # Soft delete in DB
        SupabaseService.soft_delete_document(document_id)
        return {"message": "Document deleted successfully"}
    else:
        # Even if not found in DB, we return success or 404. 
        # If it's already deleted/missing, we can just say success or raise.
        raise HTTPException(status_code=404, detail="Document not found")

@router.get("/admin/analytics", dependencies=[Depends(verify_admin)])
async def get_analytics(days: int = 7):
    """Get analytics data"""
    return SupabaseService.get_analytics(days)

@router.post("/admin/cleanup", dependencies=[Depends(verify_admin)])
async def run_cleanup():
    """Trigger manual cleanup"""
    await CleanupService.cleanup_expired_documents()
    return {"message": "Cleanup job triggered"}
