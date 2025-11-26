# AI-Powered Document Chatbot

A production-ready AI chatbot that allows users to upload documents and chat with them using natural language. Supports multilingual queries and voice input/output.

## 🎯 Features

- 📄 **Document Upload**: PDF, DOCX, TXT, XLSX, PPTX support
- 💬 **Intelligent Chat**: RAG-powered responses with source citations
- 🌍 **Multilingual**: Support for 7 languages with auto-translation
- 🎤 **Voice Support**: Speech-to-text and text-to-speech
- 🔒 **Session-based**: No authentication required, isolated user sessions
- ⚡ **Fast Search**: Vector-based semantic search with Qdrant

## 🏗️ Tech Stack

**Backend:**
- FastAPI (Python)
- OpenAI GPT-4o-mini, Whisper, TTS
- Qdrant Vector Database
- LangChain
- Cloudinary (file storage)

**Frontend:**
- Next.js 15 (App Router)
- TypeScript
- Tailwind CSS
- React Hooks

## 📋 Prerequisites

- Python 3.11+
- Node.js 18+ (or Bun)
- OpenAI API Key
- Qdrant Cloud Account (free tier available)
- Cloudinary Account (free tier available)

## 🚀 Quick Start

### 1. Clone and Setup

```bash
# The project structure is already created
cd ai-document-chatbot
```

### 2. Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file from example
cp .env.example .env

# Edit .env and add your API keys:
# - OPENAI_API_KEY
# - QDRANT_URL and QDRANT_API_KEY
# - CLOUDINARY credentials
```

**Get your API keys:**
- OpenAI: https://platform.openai.com/api-keys
- Qdrant: https://cloud.qdrant.io/ (free 1GB cluster)
- Cloudinary: https://cloudinary.com/ (free tier)

```bash
# Initialize Qdrant collection
python -c "from app.services.embedding_service import EmbeddingService; import asyncio; asyncio.run(EmbeddingService.initialize_collection())"

# Run backend server
uvicorn app.main:app --reload
```

Backend will run at: **http://localhost:8000**
API Docs: **http://localhost:8000/docs**

### 3. Frontend Setup

```bash
# In the root directory (not backend)
cd ..

# Install dependencies
bun install

# Create .env.local
cp .env.local.example .env.local

# Run development server
bun run dev
```

Frontend will run at: **http://localhost:3000**

### 4. Using Docker (Alternative)

```bash
# Create .env file in root with all required variables
cp backend/.env.example .env
# Edit .env with your API keys

# Start all services
docker-compose up --build
```

## 📝 Environment Variables

### Backend (.env)

```env
# OpenAI Configuration
OPENAI_API_KEY=sk-...
OPENAI_MODEL=gpt-4o-mini
OPENAI_EMBEDDING_MODEL=text-embedding-3-large
OPENAI_WHISPER_MODEL=whisper-1
OPENAI_TTS_MODEL=tts-1

# Qdrant Configuration
QDRANT_URL=https://your-cluster.qdrant.io
QDRANT_API_KEY=your_qdrant_key
QDRANT_COLLECTION_NAME=document_embeddings

# Cloudinary Configuration
CLOUDINARY_CLOUD_NAME=your_cloud_name
CLOUDINARY_API_KEY=your_api_key
CLOUDINARY_API_SECRET=your_api_secret

# Application Configuration
MAX_FILE_SIZE_MB=10
SESSION_SECRET=your_random_secret_key_here
SESSION_TIMEOUT_HOURS=24
ALLOWED_FILE_TYPES=pdf,docx,txt,xlsx,pptx
CHUNK_SIZE=1000
CHUNK_OVERLAP=200
MAX_CHUNKS_RETRIEVAL=5

# CORS Configuration
FRONTEND_URL=http://localhost:3000

# Rate Limiting
RATE_LIMIT_PER_MINUTE=10
```

### Frontend (.env.local)

```env
NEXT_PUBLIC_API_URL=http://localhost:8000/api
```

## 🎮 Usage

1. **Open Application**: Navigate to http://localhost:3000
2. **Upload Document**: Drag & drop or click to upload PDF/DOCX/TXT/XLSX/PPTX
3. **Select Language**: Choose your preferred language from dropdown (7 languages supported)
4. **Ask Questions**: Type or use voice to ask about your documents
5. **Get Answers**: Receive intelligent responses with source citations

### Supported Languages

- 🇺🇸 English
- 🇪🇸 Spanish (Español)
- 🇫🇷 French (Français)
- 🇩🇪 German (Deutsch)
- 🇸🇦 Arabic (العربية)
- 🇵🇰 Urdu (اردو)
- 🇨🇳 Chinese (中文)

## 🏗️ Project Structure

```
ai-document-chatbot/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py              # FastAPI app
│   │   ├── config.py            # Configuration
│   │   ├── models/
│   │   │   └── schemas.py       # Pydantic models
│   │   ├── services/
│   │   │   ├── document_service.py    # File processing
│   │   │   ├── embedding_service.py   # Vector embeddings
│   │   │   ├── chat_service.py        # RAG chat
│   │   │   ├── audio_service.py       # Voice features
│   │   │   ├── translation_service.py # Translation
│   │   │   └── session_service.py     # Session management
│   │   ├── routes/
│   │   │   ├── upload.py        # Document upload
│   │   │   ├── chat.py          # Chat endpoints
│   │   │   ├── documents.py     # Document management
│   │   │   └── session.py       # Session endpoints
│   │   └── utils/
│   │       ├── text_chunker.py  # Text processing
│   │       ├── file_processor.py
│   │       └── validators.py
│   ├── requirements.txt
│   ├── .env.example
│   └── Dockerfile
├── src/
│   ├── app/
│   │   ├── page.tsx            # Main page
│   │   └── layout.tsx
│   ├── components/
│   │   ├── ChatInterface.tsx   # Chat UI
│   │   ├── FileUpload.tsx      # File upload
│   │   ├── AudioRecorder.tsx   # Voice recording
│   │   ├── LanguageSelector.tsx
│   │   ├── DocumentList.tsx
│   │   └── Message.tsx
│   └── lib/
│       ├── api.ts              # API client
│       └── types.ts            # TypeScript types
├── docker-compose.yml
├── package.json
└── README.md
```

## 🧪 Testing

### Manual Testing

1. **Upload Test**:
   - Upload a PDF document
   - Verify it appears in the document list
   - Check the chunk count

2. **Chat Test**:
   - Ask: "What is this document about?"
   - Verify you get a response with sources

3. **Language Test**:
   - Switch to Spanish
   - Ask: "Resume este documento"
   - Verify response is in Spanish

4. **Voice Test**:
   - Click microphone button
   - Record a question
   - Verify audio response plays

5. **Delete Test**:
   - Delete a document
   - Verify it's removed from both list and vector DB

### API Testing Script

Create `backend/tests/test_api.py`:

```python
import requests

BASE_URL = "http://localhost:8000/api"

# 1. Create session
response = requests.post(f"{BASE_URL}/session")
session_id = response.json()["session_id"]
print(f"✅ Session created: {session_id}")

# 2. Upload document
with open("test.pdf", "rb") as f:
    files = {"file": ("test.pdf", f, "application/pdf")}
    response = requests.post(f"{BASE_URL}/upload?session_id={session_id}", files=files)
print(f"✅ Document uploaded: {response.json()['chunks_created']} chunks")

# 3. Send chat message
response = requests.post(
    f"{BASE_URL}/chat",
    json={"query": "What is this document about?", "session_id": session_id, "language": "en"}
)
print(f"✅ Response: {response.json()['response'][:100]}...")
```

## 🔧 Troubleshooting

### Issue: Qdrant connection error
- Verify `QDRANT_URL` and `QDRANT_API_KEY` are correct
- Check if collection exists (run initialization script)
- Ensure Qdrant cluster is active

### Issue: File upload fails
- Check file size (max 10MB by default)
- Verify file type is supported
- Check Cloudinary credentials are correct

### Issue: Audio not working
- Ensure browser supports audio recording (Chrome/Edge recommended)
- Check microphone permissions
- Verify OpenAI API has access to Whisper/TTS

### Issue: CORS errors
- Verify `FRONTEND_URL` in backend .env matches your frontend URL
- Check both services are running
- Clear browser cache

## 💰 Cost Estimation

**Development/Testing:**
- OpenAI API: ~$5-10/month (light usage)
- Qdrant Free Tier: $0 (1GB storage)
- Cloudinary Free Tier: $0 (25GB storage, 25GB bandwidth)
- **Total: $5-10/month**

**Production (100 users/day):**
- OpenAI API: ~$50-100/month
- Qdrant Cloud: $25/month (5GB)
- Cloudinary: $0-10/month
- Hosting: $10-20/month
- **Total: ~$85-155/month**

## 🚀 Deployment

### Backend (Railway/Render)

1. Push code to GitHub
2. Connect to Railway/Render
3. Set environment variables in dashboard
4. Deploy from GitHub
5. Note the backend URL

### Frontend (Vercel)

```bash
# Install Vercel CLI
npm i -g vercel

# Deploy
vercel --prod
```

Set environment variable:
- `NEXT_PUBLIC_API_URL`: Your backend URL

### Production Considerations

- ✅ Use Redis for session storage (replace in-memory dict)
- ✅ Enable CORS for production domain only
- ✅ Set up monitoring (Sentry, LogRocket)
- ✅ Configure rate limiting with Redis
- ✅ Use CDN for static assets
- ✅ Enable HTTPS only
- ✅ Add authentication (optional)
- ✅ Set up database for persistent storage

## 🎯 Features Roadmap (V2)

- [ ] User authentication & accounts
- [ ] Document OCR for scanned PDFs
- [ ] Batch upload (multiple files)
- [ ] Export chat history (PDF/TXT)
- [ ] Document comparison feature
- [ ] Analytics dashboard
- [ ] API rate limiting with Redis
- [ ] Webhook notifications
- [ ] Custom embedding models
- [ ] Mobile app (React Native)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

MIT License - feel free to use for commercial projects

## 🆘 Support

For issues or questions:
- GitHub Issues: Create an issue
- Documentation: See this README
- API Docs: http://localhost:8000/docs

## 🙏 Acknowledgments

- OpenAI for GPT-4, Whisper, and TTS
- Qdrant for vector database
- Cloudinary for file storage
- Next.js and FastAPI teams

---

**Built with ❤️ using OpenAI, Qdrant, and Next.js**

Happy chatting with your documents! 🚀
