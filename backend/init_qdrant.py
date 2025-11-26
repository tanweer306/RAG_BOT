"""
Initialize Qdrant Collection
Run this script before starting the application for the first time
"""

import asyncio
from app.services.embedding_service import EmbeddingService
from app.config import settings

async def main():
    print("🔧 Initializing Qdrant collection...")
    print(f"   Collection name: {settings.QDRANT_COLLECTION_NAME}")
    print(f"   Qdrant URL: {settings.QDRANT_URL}")
    
    try:
        await EmbeddingService.initialize_collection()
        print("✅ Qdrant collection initialized successfully!")
        print(f"   Ready to store embeddings in collection: {settings.QDRANT_COLLECTION_NAME}")
    except Exception as e:
        print(f"❌ Error initializing collection: {e}")
        print("\nPlease check:")
        print("  1. QDRANT_URL and QDRANT_API_KEY are set correctly in .env")
        print("  2. Your Qdrant cluster is active and accessible")
        print("  3. You have network connectivity to Qdrant")

if __name__ == "__main__":
    asyncio.run(main())
