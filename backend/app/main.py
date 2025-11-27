from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from app.routes import upload, chat, documents, session, admin
from app.config import settings
from app.services.cleanup_service import CleanupService
from app.services.embedding_service import EmbeddingService
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="AI Document Chatbot API",
    description="AI-powered document intelligence with voice support",
    version="1.0.0"
)

# Background scheduler
scheduler = AsyncIOScheduler()

# CORS middleware - Most permissive settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "HEAD", "PATCH"],
    allow_headers=["*"],
    expose_headers=["*"]
)

# Include routers
app.include_router(upload.router, prefix="/api", tags=["Upload"])
app.include_router(chat.router, prefix="/api", tags=["Chat"])
app.include_router(documents.router, prefix="/api", tags=["Documents"])
app.include_router(session.router, prefix="/api", tags=["Session"])
app.include_router(admin.router, prefix="/api", tags=["Admin"])

@app.on_event("startup")
async def startup_event():
    """Initialize services on startup"""
    # Initialize Qdrant collection
    await EmbeddingService.initialize_collection()
    
    # Start background scheduler
    scheduler.add_job(
        CleanupService.cleanup_expired_documents,
        'interval',
        hours=1,
        id='cleanup_documents'
    )
    scheduler.start()
    logger.info("Started background cleanup scheduler")

@app.on_event("shutdown")
async def shutdown_event():
    """Clean up resources on shutdown"""
    scheduler.shutdown()

@app.get("/")
async def root():
    return {"message": "AI Document Chatbot API", "status": "running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.get("/test-cors")
async def test_cors():
    return {
        "message": "CORS test successful", 
        "timestamp": datetime.now().isoformat(),
        "cors_headers": "working"
    }

@app.get("/debug")
async def debug_info():
    return {
        "app": "AI Document Chatbot API",
        "version": "1.0.0",
        "cors_config": {
            "allow_origins": ["*"],
            "allow_credentials": False,
            "allow_methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS", "HEAD", "PATCH"],
            "allow_headers": ["*"],
            "expose_headers": ["*"]
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
