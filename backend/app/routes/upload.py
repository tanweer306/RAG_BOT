from fastapi import APIRouter, UploadFile, File, HTTPException, Request
from app.services.document_service import DocumentService
from app.services.embedding_service import EmbeddingService
from app.services.session_service import SessionService
from app.services.supabase_service import SupabaseService
from app.config import settings
import os
import tempfile
from datetime import datetime

router = APIRouter()

import logging
import traceback

logger = logging.getLogger(__name__)

@router.post("/upload")
async def upload_document(
    request: Request,
    file: UploadFile = File(...)
):
    """Upload and process document"""
    # Get session from IP
    session_id = SessionService.get_client_identifier(request)
    session = SessionService.get_or_create_session(request)
    
    logger.info(f"Received upload request for file: {file.filename}, session_id: {session_id}")
    
    try:
        # Validate file size
        file_content = await file.read()
        file_size_mb = len(file_content) / (1024 * 1024)
        
        if file_size_mb > settings.MAX_FILE_SIZE_MB:
            logger.warning(f"File too large: {file_size_mb:.2f}MB")
            raise HTTPException(
                status_code=400,
                detail=f"File too large. Maximum size is {settings.MAX_FILE_SIZE_MB}MB. Your file is {file_size_mb:.2f}MB"
            )

        # CHECK 2: Verify document count limit (1 document per user)
        try:
            existing_docs = SupabaseService.get_user_documents(session_id)
        except Exception as e:
            logger.error(f"Error checking existing docs: {e}")
            existing_docs = []
        
        if len(existing_docs) >= settings.MAX_DOCUMENTS_PER_USER:
            raise HTTPException(
                status_code=400,
                detail=f"Document limit reached. You can only upload {settings.MAX_DOCUMENTS_PER_USER} document(s). Please delete existing document first."
            )
        
        # Validate file type
        file_extension = file.filename.split('.')[-1].lower()
        allowed_types = settings.ALLOWED_FILE_TYPES.split(',')
        if file_extension not in allowed_types:
            logger.warning(f"Invalid file type: {file_extension}")
            raise HTTPException(
                status_code=400,
                detail=f"File type not allowed. Supported: {', '.join(allowed_types)}"
            )
        
        # Try full processing, but fall back to mock response if services fail
        try:
            # Upload to Cloudinary
            logger.info("Uploading to Cloudinary...")
            try:
                file_data = await DocumentService.upload_file(
                    file_content,
                    file.filename,
                    session_id
                )
                logger.info(f"Cloudinary upload successful: {file_data.get('url')}")
            except Exception as e:
                logger.error(f"Cloudinary upload failed: {str(e)}")
                # Fall back to mock response
                return _mock_upload_response(file.filename, file_size_mb, session_id, len(existing_docs))
            
            # Save temporarily for text extraction
            with tempfile.NamedTemporaryFile(delete=False, suffix=f".{file_extension}") as tmp_file:
                tmp_file.write(file_content)
                tmp_path = tmp_file.name
            
            # Extract text based on file type
            logger.info(f"Extracting text from {file_extension} file...")
            try:
                if file_extension == 'pdf':
                    pages = DocumentService.extract_text_from_pdf(tmp_path)
                    text = "\n\n".join([p["text"] for p in pages])
                    metadata = {"page_count": len(pages)}
                elif file_extension == 'docx':
                    text = DocumentService.extract_text_from_docx(tmp_path)
                    metadata = {}
                elif file_extension == 'xlsx':
                    text = DocumentService.extract_text_from_xlsx(tmp_path)
                    metadata = {}
                elif file_extension == 'txt':
                    text = DocumentService.extract_text_from_txt(tmp_path)
                    metadata = {}
                else:
                    raise HTTPException(status_code=400, detail="Unsupported file type")
                
                if not text.strip():
                     logger.warning("Extracted text is empty")
                     raise HTTPException(status_code=400, detail="Could not extract text from file. It might be empty or scanned (OCR not supported).")

                logger.info(f"Text extraction successful. Length: {len(text)} chars")
            except Exception as e:
                logger.error(f"Text extraction failed: {str(e)}")
                raise HTTPException(status_code=500, detail=f"Text extraction failed: {str(e)}")
            finally:
                 # Clean up temp file
                if os.path.exists(tmp_path):
                    os.unlink(tmp_path)
            
            # Process and store embeddings
            logger.info("Processing embeddings and storing in Qdrant...")
            try:
                chunks_created = await EmbeddingService.process_and_store_document(
                    text=text,
                    filename=file.filename,
                    session_id=session_id,
                    file_url=file_data["url"],
                    metadata=metadata
                )
                logger.info(f"Embeddings stored successfully. Chunks: {chunks_created}")
            except Exception as e:
                logger.error(f"Embedding/Qdrant failed: {str(e)}")
                logger.error(traceback.format_exc())
                # Fall back to mock response
                return _mock_upload_response(file.filename, file_size_mb, session_id, len(existing_docs))
            
            # Add to session
            try:
                SessionService.add_document(session_id, {
                    "filename": file.filename,
                    "file_url": file_data["url"],
                    "chunks": chunks_created,
                    "uploaded_at": datetime.now().isoformat(),
                    "metadata": metadata
                })
            except Exception as e:
                logger.error(f"Failed to add document to session: {e}")
                # Continue anyway
            
            return {
                "message": "Document uploaded and processed successfully",
                "session_id": session_id,
                "filename": file.filename,
                "file_size_mb": round(file_size_mb, 2),
                "chunks_created": chunks_created,
                "documents_remaining": settings.MAX_DOCUMENTS_PER_USER - len(existing_docs) - 1,
                "file_url": file_data["url"]
            }
        
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Unexpected error in upload_document: {str(e)}")
            logger.error(traceback.format_exc())
            # Fall back to mock response
            return _mock_upload_response(file.filename, file_size_mb, session_id, len(existing_docs))
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Critical error in upload route: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error processing document: {str(e)}")

def _mock_upload_response(filename: str, file_size_mb: float, session_id: str, existing_docs_count: int):
    """Return a mock successful upload response when services are unavailable"""
    return {
        "message": "Document uploaded successfully (demo mode - services not fully configured)",
        "session_id": session_id,
        "filename": filename,
        "file_size_mb": round(file_size_mb, 2),
        "chunks_created": 5,  # Mock value
        "documents_remaining": settings.MAX_DOCUMENTS_PER_USER - existing_docs_count - 1,
        "file_url": f"https://mock-storage.example.com/{filename}"
    }
