import asyncio
import os
import sys
from app.config import settings
from qdrant_client import QdrantClient
import cloudinary
import cloudinary.api
from openai import AsyncOpenAI

async def check_setup():
    print("🔍 Checking Backend Setup...\n")
    
    # 1. Check Environment Variables
    print("1. Environment Variables")
    required_vars = [
        "OPENAI_API_KEY", "QDRANT_URL", "QDRANT_API_KEY",
        "CLOUDINARY_CLOUD_NAME", "CLOUDINARY_API_KEY", "CLOUDINARY_API_SECRET"
    ]
    missing = []
    for var in required_vars:
        val = getattr(settings, var, None)
        if not val or val == "sk-..." or val == "your_qdrant_key" or val == "your_cloud_name":
            missing.append(var)
        else:
            print(f"   ✅ {var} is set")
    
    if missing:
        print(f"   ❌ Missing or default values for: {', '.join(missing)}")
        print("   Please update your backend/.env file with real API keys.")
        return
    else:
        print("   ✅ All required environment variables seem to be present.")

    # 2. Check OpenAI
    print("\n2. Checking OpenAI Connection...")
    try:
        client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
        response = await client.models.list()
        print(f"   ✅ OpenAI connection successful. Available models: {len(response.data)}")
    except Exception as e:
        print(f"   ❌ OpenAI connection failed: {str(e)}")

    # 3. Check Qdrant
    print("\n3. Checking Qdrant Connection...")
    try:
        qdrant = QdrantClient(url=settings.QDRANT_URL, api_key=settings.QDRANT_API_KEY)
        collections = qdrant.get_collections()
        print(f"   ✅ Qdrant connection successful. Collections found: {len(collections.collections)}")
        
        # Check if specific collection exists
        exists = False
        for col in collections.collections:
            if col.name == settings.QDRANT_COLLECTION_NAME:
                exists = True
                break
        
        if exists:
            print(f"   ✅ Collection '{settings.QDRANT_COLLECTION_NAME}' exists.")
        else:
            print(f"   ⚠️ Collection '{settings.QDRANT_COLLECTION_NAME}' NOT found.")
            print("      Run 'python init_qdrant.py' to create it.")
            
    except Exception as e:
        print(f"   ❌ Qdrant connection failed: {str(e)}")

    # 4. Check Cloudinary
    print("\n4. Checking Cloudinary Connection...")
    try:
        cloudinary.config(
            cloud_name=settings.CLOUDINARY_CLOUD_NAME,
            api_key=settings.CLOUDINARY_API_KEY,
            api_secret=settings.CLOUDINARY_API_SECRET
        )
        # Ping Cloudinary (fetch resource types)
        cloudinary.api.resource_types()
        print("   ✅ Cloudinary connection successful.")
    except Exception as e:
        print(f"   ❌ Cloudinary connection failed: {str(e)}")

if __name__ == "__main__":
    # Add the current directory to sys.path so we can import app
    sys.path.append(os.getcwd())
    asyncio.run(check_setup())
