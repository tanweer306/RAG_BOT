# 🏗️ System Architecture

## High-Level Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                         USER BROWSER                             │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │              Next.js Frontend (Port 3000)                 │  │
│  │  ┌────────────┐  ┌────────────┐  ┌──────────────────┐   │  │
│  │  │   Upload   │  │    Chat    │  │   Voice Input    │   │  │
│  │  │  Component │  │ Component  │  │    Component     │   │  │
│  │  └────────────┘  └────────────┘  └──────────────────┘   │  │
│  └───────────────────────┬──────────────────────────────────┘  │
└────────────────────────┬─┴───────────────────────────────────┬─┘
                         │                                     │
                    HTTP API Calls                      WebSocket (future)
                         │                                     │
┌────────────────────────┴─────────────────────────────────────┴─┐
│                  FastAPI Backend (Port 8000)                    │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                    API Routes                            │   │
│  │  /upload  /chat  /documents  /session  /chat/audio     │   │
│  └───────┬─────────────────────────────────────────────────┘   │
│          │                                                       │
│  ┌───────┴─────────────────────────────────────────────────┐   │
│  │                   Service Layer                          │   │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐  │   │
│  │  │ Document │ │ Embedding│ │   Chat   │ │  Audio   │  │   │
│  │  │ Service  │ │ Service  │ │ Service  │ │ Service  │  │   │
│  │  └──────────┘ └──────────┘ └──────────┘ └──────────┘  │   │
│  │  ┌──────────┐ ┌──────────┐                             │   │
│  │  │Translation│ │ Session  │                             │   │
│  │  │ Service  │ │ Service  │                             │   │
│  │  └──────────┘ └──────────┘                             │   │
│  └──────────────────────────────────────────────────────────┘  │
└────────────────────────────────────────────────────────────────┘
                         │  │  │
         ┌───────────────┘  │  └────────────────┐
         │                  │                    │
         ▼                  ▼                    ▼
┌─────────────────┐  ┌─────────────┐  ┌──────────────────┐
│   OpenAI API    │  │   Qdrant    │  │   Cloudinary     │
│                 │  │   Vector    │  │   File Storage   │
│  • GPT-4o-mini  │  │   Database  │  │                  │
│  • Embeddings   │  │             │  │  • Store PDFs    │
│  • Whisper      │  │  • Store    │  │  • Store DOCX    │
│  • TTS          │  │    vectors  │  │  • Store images  │
│                 │  │  • Search   │  │                  │
└─────────────────┘  └─────────────┘  └──────────────────┘
```

## Data Flow

### 1. Document Upload Flow

```
User selects file
       │
       ▼
┌─────────────────┐
│  FileUpload.tsx │
│  - Validates    │
│  - Shows UI     │
└────────┬────────┘
         │
         │ FormData (file)
         ▼
┌─────────────────┐
│ POST /upload    │
│  upload.py      │
└────────┬────────┘
         │
         ├──────────────────┐
         │                  │
         ▼                  ▼
┌──────────────────┐  ┌──────────────────┐
│ DocumentService  │  │ Cloudinary       │
│ - Extract text   │  │ - Store file     │
│ - Parse PDF/DOCX │  │ - Return URL     │
└────────┬─────────┘  └──────────────────┘
         │
         │ Raw text
         ▼
┌──────────────────┐
│ EmbeddingService │
│ - Chunk text     │
│ - Create vectors │
└────────┬─────────┘
         │
         │ Vectors + metadata
         ▼
┌──────────────────┐
│ Qdrant Database  │
│ - Store vectors  │
│ - Index for      │
│   similarity     │
└──────────────────┘
```

### 2. Chat Query Flow

```
User types question
       │
       ▼
┌──────────────────┐
│ ChatInterface.tsx│
│ - Show message   │
│ - Handle state   │
└────────┬─────────┘
         │
         │ { query, session_id, language }
         ▼
┌──────────────────┐
│  POST /chat      │
│  chat.py         │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│  ChatService     │
│  - Get history   │
└────────┬─────────┘
         │
         │ query text
         ▼
┌──────────────────┐
│ EmbeddingService │
│ - Create query   │
│   embedding      │
└────────┬─────────┘
         │
         │ query vector
         ▼
┌──────────────────┐
│ Qdrant Search    │
│ - Find similar   │
│ - Return top N   │
└────────┬─────────┘
         │
         │ relevant chunks
         ▼
┌──────────────────┐
│  ChatService     │
│ - Build context  │
│ - Add history    │
└────────┬─────────┘
         │
         │ prompt + context
         ▼
┌──────────────────┐
│  OpenAI GPT      │
│ - Generate       │
│   response       │
└────────┬─────────┘
         │
         │ answer
         ▼
┌──────────────────┐
│TranslationService│
│ (if needed)      │
└────────┬─────────┘
         │
         │ translated answer + sources
         ▼
┌──────────────────┐
│  User sees       │
│  response        │
└──────────────────┘
```

### 3. Voice Chat Flow

```
User clicks mic
       │
       ▼
┌──────────────────┐
│AudioRecorder.tsx │
│ - Record audio   │
└────────┬─────────┘
         │
         │ audio blob
         ▼
┌──────────────────┐
│POST /chat/audio  │
│  chat.py         │
└────────┬─────────┘
         │
         │ audio file
         ▼
┌──────────────────┐
│  AudioService    │
│  - Transcribe    │
└────────┬─────────┘
         │
         │ text
         ▼
┌──────────────────┐
│  OpenAI Whisper  │
│  - STT           │
└────────┬─────────┘
         │
         │ transcribed text
         ▼
┌──────────────────┐
│  ChatService     │
│  (same as above) │
└────────┬─────────┘
         │
         │ response text
         ▼
┌──────────────────┐
│  AudioService    │
│  - TTS           │
└────────┬─────────┘
         │
         │ audio
         ▼
┌──────────────────┐
│  OpenAI TTS      │
│  - Generate      │
│    speech        │
└────────┬─────────┘
         │
         │ audio blob
         ▼
┌──────────────────┐
│  User hears      │
│  response        │
└──────────────────┘
```

## Component Architecture

### Frontend Components

```
page.tsx (Main Page)
    │
    ├── FileUpload
    │   └── react-dropzone
    │
    ├── LanguageSelector
    │   └── <select> dropdown
    │
    ├── DocumentList
    │   └── Document items
    │       └── Delete button
    │
    └── ChatInterface
        ├── Message[]
        │   └── Message
        │       ├── User bubble (blue)
        │       └── Bot bubble (gray)
        │           └── Sources list
        │
        ├── AudioRecorder
        │   └── MediaRecorder API
        │
        └── Input form
            ├── Text input
            ├── Voice button
            └── Send button
```

### Backend Services

```
main.py (FastAPI App)
    │
    ├── routes/
    │   ├── session.py
    │   │   └── SessionService
    │   ├── upload.py
    │   │   ├── DocumentService
    │   │   └── EmbeddingService
    │   ├── chat.py
    │   │   ├── ChatService
    │   │   ├── TranslationService
    │   │   └── AudioService
    │   └── documents.py
    │       └── SessionService
    │
    └── services/
        ├── document_service.py
        │   ├── upload_file()
        │   ├── extract_text_from_pdf()
        │   ├── extract_text_from_docx()
        │   └── extract_text_from_xlsx()
        │
        ├── embedding_service.py
        │   ├── initialize_collection()
        │   ├── create_embedding()
        │   ├── process_and_store_document()
        │   └── search_similar_chunks()
        │
        ├── chat_service.py
        │   └── generate_response()
        │
        ├── audio_service.py
        │   ├── transcribe_audio()
        │   └── text_to_speech()
        │
        ├── translation_service.py
        │   └── translate_text()
        │
        └── session_service.py
            ├── create_session()
            ├── get_session()
            ├── update_session()
            └── delete_session()
```

## Database Schema

### Qdrant Collection Structure

```
Collection: document_embeddings
├── Vector size: 3072 (OpenAI text-embedding-3-large)
├── Distance metric: COSINE
└── Points:
    ├── id: UUID
    ├── vector: [3072 floats]
    └── payload:
        ├── text: "chunk content"
        ├── filename: "document.pdf"
        ├── session_id: "uuid"
        ├── chunk_index: 0
        ├── total_chunks: 10
        ├── file_url: "cloudinary url"
        └── metadata: {
            ├── page_count: 5
            └── ...custom fields
        }
```

### Session Storage (In-Memory)

```python
sessions = {
    "session-id-uuid": {
        "created_at": datetime,
        "last_active": datetime,
        "language": "en",
        "documents": [
            {
                "filename": "doc.pdf",
                "url": "cloudinary-url",
                "chunks": 15,
                "uploaded_at": "ISO timestamp"
            }
        ],
        "conversation_history": [
            {
                "role": "user",
                "content": "question",
                "timestamp": "ISO timestamp"
            },
            {
                "role": "assistant",
                "content": "answer",
                "timestamp": "ISO timestamp"
            }
        ]
    }
}
```

## API Endpoints

### Session Management
```
POST   /api/session               - Create new session
GET    /api/session/{id}          - Get session info
POST   /api/session/{id}/language - Update language
DELETE /api/session/{id}          - Delete session
```

### Document Management
```
POST   /api/upload                - Upload document
GET    /api/documents             - List documents
DELETE /api/documents/{filename}  - Delete document
```

### Chat
```
POST   /api/chat                  - Text chat
POST   /api/chat/audio            - Voice chat
```

## Technology Stack Details

### Frontend
- **Framework**: Next.js 15 (App Router)
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **HTTP Client**: Axios
- **File Upload**: react-dropzone
- **Icons**: lucide-react
- **Audio**: MediaRecorder API

### Backend
- **Framework**: FastAPI
- **Language**: Python 3.11
- **Web Server**: Uvicorn
- **Validation**: Pydantic
- **Document Processing**:
  - PDF: PyPDF2
  - DOCX: python-docx
  - XLSX: openpyxl
- **AI/ML**:
  - LLM: OpenAI GPT-4o-mini
  - Embeddings: text-embedding-3-large
  - STT: Whisper
  - TTS: OpenAI TTS

### External Services
- **Vector DB**: Qdrant Cloud
- **File Storage**: Cloudinary
- **AI API**: OpenAI

## Security Considerations

### Current Implementation
- ✅ Session-based isolation (no cross-session data)
- ✅ File type validation
- ✅ File size limits
- ✅ CORS configuration
- ✅ Input validation with Pydantic
- ✅ Environment-based secrets

### Production Recommendations
- 🔒 Add authentication (OAuth/JWT)
- 🔒 Use Redis for session storage
- 🔒 Implement rate limiting
- 🔒 Add request signing
- 🔒 Enable HTTPS only
- 🔒 Implement CSP headers
- 🔒 Add API key management
- 🔒 Set up WAF (Web Application Firewall)

## Performance Optimization

### Current Optimizations
- ✅ Async/await for I/O operations
- ✅ Vector-based similarity search (fast)
- ✅ Chunking for large documents
- ✅ Session caching
- ✅ Streaming responses (FastAPI)

### Production Optimizations
- 🚀 Add Redis for caching
- 🚀 Use CDN for static assets
- 🚀 Implement connection pooling
- 🚀 Add database indexes
- 🚀 Use batch processing for embeddings
- 🚀 Implement query result caching
- 🚀 Add load balancing
- 🚀 Use horizontal scaling

## Monitoring & Observability

### Recommended Tools
- **Logging**: Python logging → ELK Stack
- **Metrics**: Prometheus + Grafana
- **Tracing**: OpenTelemetry
- **Error Tracking**: Sentry
- **APM**: New Relic / DataDog
- **Uptime**: UptimeRobot / Pingdom

### Key Metrics to Monitor
- API response times
- OpenAI API latency
- Qdrant query performance
- Upload success rate
- Session creation rate
- Error rates by endpoint
- Token usage (OpenAI costs)
- Storage usage (Cloudinary, Qdrant)

## Scalability

### Vertical Scaling
- Increase server resources (CPU, RAM)
- Optimize chunk sizes
- Add caching layers

### Horizontal Scaling
- Multiple backend instances behind load balancer
- Shared Redis for sessions
- Database read replicas
- Separate services (microservices)

### Cost Scaling
| Users/Day | OpenAI | Qdrant | Cloudinary | Total/Month |
|-----------|--------|--------|------------|-------------|
| 10        | $5     | $0     | $0         | $5          |
| 100       | $50    | $25    | $10        | $85         |
| 1,000     | $500   | $75    | $50        | $625        |
| 10,000    | $5,000 | $200   | $200       | $5,400      |

---

This architecture provides a solid foundation for:
- 📈 Scalability to thousands of users
- 🔒 Security best practices
- ⚡ Fast response times
- 💰 Cost-effective operation
- 🛠️ Easy maintenance and updates
