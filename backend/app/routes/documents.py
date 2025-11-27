from fastapi import APIRouter, HTTPException, Request
from app.services.session_service import SessionService
from app.services.embedding_service import EmbeddingService
from app.services.supabase_service import SupabaseService
from app.config import settings

router = APIRouter()

@router.get("/documents")
async def list_documents(request: Request):
    """List all documents in session"""
    
    session_id = SessionService.get_client_identifier(request)
    session = SessionService.get_session(session_id)
    
    try:
        # Even if session is None (not active), we might have docs? 
        # But we need session_id. get_client_identifier gives us the ID.
        # session object is just for validation or extra info.
        
        # We can fetch documents directly.
        documents = SupabaseService.get_user_documents(session_id)
        
        return {
            "session_id": session_id,
            "documents": documents,
            "total": len(documents)
        }
    except Exception as e:
        # Fallback: return empty documents list
        return {
            "session_id": session_id,
            "documents": [],
            "total": 0
        }

@router.delete("/documents/{filename}")
async def delete_document(request: Request, filename: str):
    """Delete a document from session"""
    
    session_id = SessionService.get_client_identifier(request)
    
    try:
        # Find document to get ID
        docs = SupabaseService.get_user_documents(session_id)
        target_doc = next((d for d in docs if d["filename"] == filename), None)
        
        if not target_doc:
            raise HTTPException(status_code=404, detail="Document not found")
            
        # Remove from Qdrant
        await EmbeddingService.delete_document_vectors(session_id, filename)
        
        # Remove from Supabase (soft delete)
        SupabaseService.soft_delete_document(target_doc["id"])
        
        return {"message": f"Document {filename} deleted successfully"}
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting document: {str(e)}")
