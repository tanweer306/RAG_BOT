from openai import AsyncOpenAI
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct, Filter, FieldCondition, MatchValue
from app.config import settings
from app.utils.text_chunker import TextChunker
from typing import List, Dict
import uuid

client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
# Increase timeout to 60s (default is usually 5-10s)
qdrant = QdrantClient(url=settings.QDRANT_URL, api_key=settings.QDRANT_API_KEY, timeout=60)

class EmbeddingService:
    @staticmethod
    async def initialize_collection():
        """Create Qdrant collection if it doesn't exist and ensure indexes"""
        try:
            qdrant.get_collection(settings.QDRANT_COLLECTION_NAME)
        except Exception as e:
            # If it's a validation error, the collection exists but client is outdated/incompatible
            # We should only try to create if it's strictly a "Not Found" or if we are sure it doesn't exist.
            # For now, we try to create and ignore "Conflict" errors.
            try:
                qdrant.create_collection(
                    collection_name=settings.QDRANT_COLLECTION_NAME,
                    vectors_config=VectorParams(size=3072, distance=Distance.COSINE),
                )
            except Exception as create_error:
                # Check if error is because it already exists (409 Conflict)
                error_str = str(create_error)
                if "already exists" in error_str or "Conflict" in error_str:
                    print(f"Collection {settings.QDRANT_COLLECTION_NAME} already exists.")
                else:
                    print(f"Error ensuring collection: {create_error}")
                    # Pass for now to allow app to start if it's just a connection check issue
        
        # Create payload index for session_id to allow filtering
        try:
            qdrant.create_payload_index(
                collection_name=settings.QDRANT_COLLECTION_NAME,
                field_name="session_id",
                field_schema="keyword"
            )
        except Exception as e:
            # Ignore if index already exists or other minor issue
            # print(f"Warning creating index: {e}")
            pass
    
    @staticmethod
    async def create_embedding(text: str) -> List[float]:
        """Generate embedding for text"""
        response = await client.embeddings.create(
            model=settings.OPENAI_EMBEDDING_MODEL,
            input=text
        )
        return response.data[0].embedding
    
    @staticmethod
    async def process_and_store_document(
        text: str,
        filename: str,
        session_id: str,
        file_url: str,
        metadata: Dict = None
    ) -> int:
        """Chunk text, create embeddings, and store in Qdrant"""
        chunks = TextChunker.chunk_text(text, settings.CHUNK_SIZE, settings.CHUNK_OVERLAP)
        
        points = []
        for idx, chunk in enumerate(chunks):
            embedding = await EmbeddingService.create_embedding(chunk)
            
            point = PointStruct(
                id=str(uuid.uuid4()),
                vector=embedding,
                payload={
                    "text": chunk,
                    "filename": filename,
                    "session_id": session_id,
                    "chunk_index": idx,
                    "total_chunks": len(chunks),
                    "file_url": file_url,
                    **(metadata or {})
                }
            )
            points.append(point)
        
        # Upload in batches to avoid timeouts
        batch_size = 50
        for i in range(0, len(points), batch_size):
            batch = points[i:i + batch_size]
            qdrant.upsert(
                collection_name=settings.QDRANT_COLLECTION_NAME,
                points=batch
            )
        
        return len(chunks)
    
    @staticmethod
    async def delete_document_vectors(session_id: str, filename: str):
        """Delete all vectors for a specific document"""
        try:
            qdrant.delete(
                collection_name=settings.QDRANT_COLLECTION_NAME,
                points_selector=Filter(
                    must=[
                        FieldCondition(key="session_id", match=MatchValue(value=session_id)),
                        FieldCondition(key="filename", match=MatchValue(value=filename))
                    ]
                )
            )
        except Exception as e:
            print(f"Error deleting vectors for {filename}: {e}")
            # Non-blocking error
            pass

    @staticmethod
    async def search_similar_chunks(
        query: str,
        session_id: str,
        limit: int = 5
    ) -> List[Dict]:
        """Search for similar chunks in Qdrant"""
        query_embedding = await EmbeddingService.create_embedding(query)
        
        search_result = qdrant.search(
            collection_name=settings.QDRANT_COLLECTION_NAME,
            query_vector=query_embedding,
            query_filter=Filter(
                must=[
                    FieldCondition(
                        key="session_id",
                        match=MatchValue(value=session_id)
                    )
                ]
            ),
            limit=limit
        )
        
        return [
            {
                "text": hit.payload["text"],
                "filename": hit.payload["filename"],
                "chunk_index": hit.payload.get("chunk_index", 0),
                "score": hit.score,
                "metadata": {k: v for k, v in hit.payload.items() 
                           if k not in ["text", "filename", "session_id"]}
            }
            for hit in search_result
        ]
