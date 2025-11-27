from fastapi import FastAPI, Response, Request
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

# CORS middleware - Allow all Vercel preview domains
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development
    allow_credentials=False,  # Set to False when using wildcard origins
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],  # Explicitly list methods
    allow_headers=["*"],
)

# Add explicit OPTIONS handler for pre-flight requests
@app.options("/{path:path}")
async def options_handler(request: Request, path: str):
    """Handle pre-flight OPTIONS requests"""
    return Response(
        status_code=200,
        headers={
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS",
            "Access-Control-Allow-Headers": "*",
        }
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
    return {"message": "CORS test successful", "timestamp": datetime.now().isoformat()}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
