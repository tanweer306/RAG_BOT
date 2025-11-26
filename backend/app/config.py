from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    # OpenAI
    OPENAI_API_KEY: str
    OPENAI_MODEL: str = "gpt-4o-mini"
    OPENAI_EMBEDDING_MODEL: str = "text-embedding-3-large"
    OPENAI_WHISPER_MODEL: str = "whisper-1"
    OPENAI_TTS_MODEL: str = "tts-1"
    
    # Qdrant
    QDRANT_URL: str
    QDRANT_API_KEY: str
    QDRANT_COLLECTION_NAME: str = "document_embeddings"
    
    # Cloudinary
    CLOUDINARY_CLOUD_NAME: str
    CLOUDINARY_API_KEY: str
    CLOUDINARY_API_SECRET: str
    
    # Supabase
    SUPABASE_URL: str
    SUPABASE_KEY: str
    
    # Admin
    ADMIN_PASSWORD: str
    
    # Application
    MAX_FILE_SIZE_MB: int = 50
    MAX_DOCUMENTS_PER_USER: int = 1
    SESSION_SECRET: str
    SESSION_TIMEOUT_HOURS: int = 24
    ALLOWED_FILE_TYPES: str = "pdf,docx,txt,xlsx,pptx"
    CHUNK_SIZE: int = 1000
    CHUNK_OVERLAP: int = 200
    MAX_CHUNKS_RETRIEVAL: int = 5
    
    # CORS
    FRONTEND_URL: str = "http://localhost:3000"
    
    # Rate Limiting
    RATE_LIMIT_PER_MINUTE: int = 10
    
    class Config:
        env_file = ".env"

settings = Settings()
