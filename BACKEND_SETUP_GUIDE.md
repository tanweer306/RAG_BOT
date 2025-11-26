# 🚀 Backend Setup & Start Guide

## ⚠️ IMPORTANT: You Need API Keys First!

Before starting the backend, you must get API keys from these 3 services:

### 1. OpenAI API Key (Required)
- Go to: https://platform.openai.com/api-keys
- Sign up or log in
- Click "Create new secret key"
- Copy the key (starts with `sk-`)
- Cost: ~$5-10/month for testing

### 2. Qdrant Vector Database (Required)
- Go to: https://cloud.qdrant.io/
- Create free account
- Create a cluster (1GB free)
- Copy the Cluster URL and API Key
- Cost: $0 (free tier)

### 3. Cloudinary File Storage (Required)
- Go to: https://cloudinary.com/
- Create free account
- Go to Dashboard
- Copy: Cloud Name, API Key, API Secret
- Cost: $0 (free tier)

---

## 📋 Backend Setup Steps

### Step 1: Install Python Dependencies

```bash
cd backend

# Create virtual environment (only needed first time)
python -m venv venv

# Activate virtual environment
# On Mac/Linux:
source venv/bin/activate

# On Windows:
venv\Scripts\activate

# Install all dependencies (takes 2-3 minutes)
pip install -r requirements.txt
```

You should see `(venv)` in your terminal prompt when activated.

### Step 2: Create .env File with Your API Keys

```bash
# Copy the example file
cp .env.example .env

# Edit the file (use any editor)
nano .env
# or
code .env
# or
vim .env
```

**Add your API keys to .env:**

```env
# Replace these with your actual keys:
OPENAI_API_KEY=sk-your-actual-key-here
QDRANT_URL=https://your-cluster.qdrant.io
QDRANT_API_KEY=your-qdrant-key-here
CLOUDINARY_CLOUD_NAME=your-cloud-name
CLOUDINARY_API_KEY=your-cloudinary-key
CLOUDINARY_API_SECRET=your-cloudinary-secret

# These can stay as-is:
OPENAI_MODEL=gpt-4o-mini
OPENAI_EMBEDDING_MODEL=text-embedding-3-large
OPENAI_WHISPER_MODEL=whisper-1
OPENAI_TTS_MODEL=tts-1
QDRANT_COLLECTION_NAME=document_embeddings
MAX_FILE_SIZE_MB=10
SESSION_SECRET=change-this-to-random-string
SESSION_TIMEOUT_HOURS=24
ALLOWED_FILE_TYPES=pdf,docx,txt,xlsx,pptx
CHUNK_SIZE=1000
CHUNK_OVERLAP=200
MAX_CHUNKS_RETRIEVAL=5
FRONTEND_URL=http://localhost:3000
RATE_LIMIT_PER_MINUTE=10
```

### Step 3: Initialize Qdrant Database

```bash
# Still in backend directory with venv activated
python init_qdrant.py
```

You should see: `✅ Qdrant collection initialized successfully!`

### Step 4: Start the Backend Server

```bash
uvicorn app.main:app --reload
```

**Success indicators:**
- ✅ `INFO:     Uvicorn running on http://127.0.0.1:8000`
- ✅ `INFO:     Application startup complete.`
- ✅ No error messages

**Backend is now running!**

---

## 🧪 Test Backend is Working

### Option 1: Browser
Open: http://localhost:8000

You should see:
```json
{"message": "AI Document Chatbot API", "status": "running"}
```

### Option 2: API Documentation
Open: http://localhost:8000/docs

You should see interactive API documentation (Swagger UI)

### Option 3: Test Script
```bash
# In a new terminal (keep backend running)
cd backend
python tests/test_api.py
```

---

## ❌ Common Errors & Fixes

### Error: "No module named 'app'"
**Fix:** Make sure you're in the `backend` directory and venv is activated

### Error: "OPENAI_API_KEY not found" or "validation error"
**Fix:** 
1. Check `.env` file exists in backend directory
2. Verify all required keys are set
3. No quotes around the values
4. No spaces around `=` sign

```bash
# Check if .env exists:
ls -la backend/.env

# Check contents (keys will be hidden):
cat backend/.env
```

### Error: "Connection to Qdrant failed"
**Fix:**
1. Verify Qdrant URL starts with `https://`
2. Check API key is correct
3. Ensure your Qdrant cluster is active (login to cloud.qdrant.io)
4. Run `python init_qdrant.py` again

### Error: "Cloudinary configuration error"
**Fix:**
1. Verify all 3 Cloudinary values are set (cloud_name, api_key, api_secret)
2. No quotes around values
3. Login to cloudinary.com and verify credentials

### Error: Port 8000 already in use
**Fix:**
```bash
# Find and kill the process
# Mac/Linux:
lsof -ti:8000 | xargs kill -9

# Windows:
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Or use a different port:
uvicorn app.main:app --reload --port 8001
```

### Error: Module import errors
**Fix:**
```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

---

## 🎯 Quick Start Command Summary

**First Time Setup:**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your API keys
python init_qdrant.py
uvicorn app.main:app --reload
```

**Every Time After:**
```bash
cd backend
source venv/bin/activate  # Windows: venv\Scripts\activate
uvicorn app.main:app --reload
```

---

## 📊 What Backend Provides

When running, the backend provides these API endpoints:

**Session Management:**
- POST `/api/session` - Create new session
- GET `/api/session/{id}` - Get session info
- POST `/api/session/{id}/language` - Update language
- DELETE `/api/session/{id}` - Delete session

**Document Management:**
- POST `/api/upload` - Upload document
- GET `/api/documents` - List documents
- DELETE `/api/documents/{filename}` - Delete document

**Chat:**
- POST `/api/chat` - Text chat
- POST `/api/chat/audio` - Voice chat

**Visit http://localhost:8000/docs for interactive documentation!**

---

## ✅ Success Checklist

Backend is ready when:
- [x] Dependencies installed (no errors)
- [x] .env file created with real API keys
- [x] Qdrant collection initialized
- [x] Server starts without errors
- [x] Can access http://localhost:8000
- [x] Can see docs at http://localhost:8000/docs

---

## 🚀 Next: Start Frontend

Once backend is running successfully, open a **new terminal** and start the frontend:

```bash
# In a NEW terminal (keep backend running)
bun run dev
```

Then open: http://localhost:3000

---

**Need more help?** 
- Check SETUP_CHECKLIST.md for detailed troubleshooting
- See AI_CHATBOT_README.md for complete documentation
