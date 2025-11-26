from app.config import settings
from qdrant_client import QdrantClient
import sys

def create_index():
    print(f"🔧 Connecting to Qdrant: {settings.QDRANT_URL}...")
    client = QdrantClient(url=settings.QDRANT_URL, api_key=settings.QDRANT_API_KEY)
    
    print(f"Creating payload index for 'session_id' on collection '{settings.QDRANT_COLLECTION_NAME}'...")
    try:
        client.create_payload_index(
            collection_name=settings.QDRANT_COLLECTION_NAME,
            field_name="session_id",
            field_schema="keyword"
        )
        print("✅ Index created successfully!")
    except Exception as e:
        print(f"❌ Error creating index (it might already exist): {e}")

if __name__ == "__main__":
    create_index()
