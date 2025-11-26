from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class ChatRequest(BaseModel):
    query: str
    session_id: str
    language: str = "en"

class ChatResponse(BaseModel):
    response: str
    sources: List[str]
    chunks_used: int
    relevant_chunks: Optional[List[dict]] = None

class DocumentUploadResponse(BaseModel):
    message: str
    session_id: str
    filename: str
    chunks_created: int
    file_url: str

class SessionCreate(BaseModel):
    language: str = "en"

class LanguageUpdate(BaseModel):
    language: str

class DocumentInfo(BaseModel):
    filename: str
    url: str
    chunks: int
    uploaded_at: str
