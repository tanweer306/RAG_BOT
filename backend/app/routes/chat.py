from fastapi import APIRouter, HTTPException, UploadFile, File, Request, Form
from pydantic import BaseModel
from app.services.chat_service import ChatService
from app.services.audio_service import AudioService
from app.services.translation_service import TranslationService
from app.services.session_service import SessionService
from app.services.supabase_service import SupabaseService
from fastapi.responses import StreamingResponse
import tempfile
import os
from io import BytesIO

router = APIRouter()

class ChatRequest(BaseModel):
    query: str
    language: str = "en"
    # Remove session_id from request body

import logging
import traceback

logger = logging.getLogger(__name__)

@router.post("/chat")
async def chat(request: Request, chat_request: ChatRequest):
    """Chat with documents using IP-based session"""
    
    # Get session from IP
    session_id = SessionService.get_client_identifier(request)
    session = SessionService.get_or_create_session(request)
    
    try:
        # Get conversation history
        # We can fetch fresh history from Supabase or use session's cached history
        conversation_history = SupabaseService.get_chat_history(session_id, limit=20)
        
        logger.info(f"Generating response for query: {chat_request.query[:50]}... Session: {session_id}")
        
        # Generate response
        try:
            result = await ChatService.generate_response(
                query=chat_request.query,
                session_id=session_id,
                language=chat_request.language,
                conversation_history=conversation_history
            )
        except Exception as e:
            logger.error(f"ChatService failed: {str(e)}")
            logger.error(traceback.format_exc())
            raise HTTPException(status_code=500, detail=f"Chat service failed: {str(e)}")
        
        # Translate if needed
        if chat_request.language != "en":
            # Note: ChatService already attempts to generate in target language via prompt
            # This step might be redundant if LLM follows instructions well, but kept for safety
            result["response"] = await TranslationService.translate_text(
                result["response"],
                chat_request.language
            )
        
        # Messages are now saved within ChatService to capture raw context
        
        return result
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error in chat route: {str(e)}")
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Error generating response: {str(e)}")

@router.post("/chat/audio")
async def chat_audio(
    request: Request,
    audio: UploadFile = File(...),
    language: str = "en" 
):
    """Chat with documents (audio input/output)"""
    
    # Validate session
    session_id = SessionService.get_client_identifier(request)
    session = SessionService.get_or_create_session(request)
    
    try:
        # Save audio temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_audio:
            content = await audio.read()
            tmp_audio.write(content)
            tmp_audio_path = tmp_audio.name
        
        # Transcribe audio to text
        transcribed_text = await AudioService.transcribe_audio(tmp_audio_path)
        os.unlink(tmp_audio_path)
        
        # Get conversation history
        conversation_history = SupabaseService.get_chat_history(session_id, limit=20)
        
        # Generate text response using RAG
        result = await ChatService.generate_response(
            query=transcribed_text,
            session_id=session_id,
            language=language,
            conversation_history=conversation_history
        )
        
        # Translate if needed
        response_text = result["response"]
        if language != "en":
            response_text = await TranslationService.translate_text(response_text, language)
        
        # Convert response to speech
        audio_response = await AudioService.text_to_speech(response_text, language)
        
        # Messages are saved in ChatService
        
        # Return audio response
        return StreamingResponse(
            BytesIO(audio_response),
            media_type="audio/mpeg",
            headers={
                "X-Transcribed-Text": transcribed_text,
                "X-Response-Text": response_text,
                "X-Sources": ",".join(result["sources"])
            }
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing audio: {str(e)}")

@router.get("/chat/history")
async def get_chat_history(
    request: Request,
    limit: int = 50
):
    """Get chat history for current session"""
    session_id = SessionService.get_client_identifier(request)
    
    try:
        history = SupabaseService.get_chat_history(session_id, limit)
        return {
            "history": history,
            "total": len(history)
        }
    except Exception as e:
        logger.error(f"Error getting chat history from Supabase: {str(e)}")
        # Fallback: return empty history
        return {
            "history": [],
            "total": 0
        }
