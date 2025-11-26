# ✅ Setup Checklist

Use this checklist to set up your AI Document Chatbot step by step.

## Pre-Setup (5 minutes)

### Get API Keys

- [ ] **OpenAI API Key**
  - Go to: https://platform.openai.com/api-keys
  - Create account / Sign in
  - Click "Create new secret key"
  - Copy key (starts with `sk-`)
  - Estimated cost: $5-10/month for testing

- [ ] **Qdrant Vector Database**
  - Go to: https://cloud.qdrant.io/
  - Create account (GitHub/Google sign-in available)
  - Create a cluster (Free tier: 1GB)
  - Copy cluster URL (e.g., `https://xyz-example.qdrant.io`)
  - Copy API key from cluster settings
  - Cost: $0 (free tier)

- [ ] **Cloudinary File Storage**
  - Go to: https://cloudinary.com/users/register/free
  - Create free account
  - Go to Dashboard
  - Copy: Cloud Name, API Key, API Secret
  - Cost: $0 (free tier: 25GB storage)

## Installation (10 minutes)

### Prerequisites Check

- [ ] Python 3.11+ installed
  ```bash
  python --version
  ```

- [ ] Node.js 18+ or Bun installed
  ```bash
  node --version
  # or
  bun --version
  ```

- [ ] Git installed (optional)
  ```bash
  git --version
  ```

### Backend Setup

- [ ] Navigate to backend folder
  ```bash
  cd backend
  ```

- [ ] Create virtual environment
  ```bash
  python -m venv venv
  ```

- [ ] Activate virtual environment
  ```bash
  # Mac/Linux:
  source venv/bin/activate
  
  # Windows:
  venv\Scripts\activate
  ```

- [ ] Install Python dependencies
  ```bash
  pip install -r requirements.txt
  ```
  ⏱️ This takes 2-3 minutes

- [ ] Create .env file
  ```bash
  cp .env.example .env
  ```

- [ ] Edit .env file with your API keys
  ```bash
  # Use your favorite editor
  nano .env
  # or
  code .env
  # or
  notepad .env  # Windows
  ```

  Add your keys:
  ```env
  OPENAI_API_KEY=sk-your-key-here
  QDRANT_URL=https://your-cluster.qdrant.io
  QDRANT_API_KEY=your-qdrant-key
  CLOUDINARY_CLOUD_NAME=your-cloud-name
  CLOUDINARY_API_KEY=your-cloudinary-key
  CLOUDINARY_API_SECRET=your-cloudinary-secret
  ```

- [ ] Initialize Qdrant collection
  ```bash
  python init_qdrant.py
  ```
  ✅ Should see: "Qdrant collection initialized successfully!"

- [ ] Test backend startup
  ```bash
  uvicorn app.main:app --reload
  ```
  ✅ Should see: "Application startup complete"
  ✅ Visit http://localhost:8000 - should show JSON response
  ✅ Visit http://localhost:8000/docs - should show API documentation

- [ ] Stop backend (Ctrl+C) and go back to root
  ```bash
  cd ..
  ```

### Frontend Setup

- [ ] Install dependencies (already done if you ran setup script)
  ```bash
  bun install
  # or
  npm install
  ```

- [ ] Create .env.local file
  ```bash
  cp .env.local.example .env.local
  ```

- [ ] Verify .env.local content
  ```bash
  cat .env.local
  ```
  Should contain:
  ```env
  NEXT_PUBLIC_API_URL=http://localhost:8000/api
  ```

## First Run (5 minutes)

### Terminal 1: Start Backend

- [ ] Open first terminal
- [ ] Navigate to backend
  ```bash
  cd backend
  ```
- [ ] Activate venv
  ```bash
  source venv/bin/activate  # or venv\Scripts\activate on Windows
  ```
- [ ] Start server
  ```bash
  uvicorn app.main:app --reload
  ```
- [ ] Verify it's running
  ✅ See: "Uvicorn running on http://127.0.0.1:8000"
  ✅ No error messages

### Terminal 2: Start Frontend

- [ ] Open second terminal
- [ ] Navigate to project root (not backend)
- [ ] Start dev server
  ```bash
  bun run dev
  # or
  npm run dev
  ```
- [ ] Verify it's running
  ✅ See: "Local: http://localhost:3000"
  ✅ No compilation errors

### Test in Browser

- [ ] Open http://localhost:3000
- [ ] Verify page loads
  ✅ See: "AI Document Chat" sidebar
  ✅ See: Language selector
  ✅ See: File upload area
  ✅ No console errors (F12 → Console tab)

## Basic Testing (10 minutes)

### Test 1: Upload Document

- [ ] Prepare a test document (PDF, DOCX, or TXT)
- [ ] Drag and drop or click to upload
- [ ] Wait for "uploaded successfully" message
  ✅ Document appears in sidebar list
  ✅ Shows chunk count
  ✅ Backend terminal shows processing logs

### Test 2: Text Chat

- [ ] Type a question: "What is this document about?"
- [ ] Press Enter or click Send
- [ ] Wait for response (5-10 seconds)
  ✅ Response appears with blue background
  ✅ Sources listed below response
  ✅ No error messages

### Test 3: Language Switch

- [ ] Click language dropdown
- [ ] Select "Español" (Spanish)
  ✅ Language updated in session
- [ ] Ask: "Resume este documento"
- [ ] Wait for response
  ✅ Response is in Spanish

### Test 4: Voice Input (Optional)

- [ ] Click microphone button
  ✅ Browser asks for mic permission
- [ ] Allow microphone access
- [ ] Speak a question clearly
- [ ] Click microphone again to stop
  ✅ Transcription happens automatically
  ✅ Response is generated
  ✅ Audio plays (if TTS is enabled)

### Test 5: Document Management

- [ ] Upload another document
  ✅ Both documents show in list
- [ ] Click trash icon on first document
  ✅ Confirmation dialog appears
- [ ] Confirm deletion
  ✅ Document removed from list
  ✅ Can still chat with remaining document

## API Testing (Optional)

- [ ] Keep backend running
- [ ] Open new terminal
- [ ] Run test script
  ```bash
  cd backend
  python tests/test_api.py
  ```
  ✅ All tests pass
  ✅ See: "🎉 All tests passed!"

## Troubleshooting

### Backend Issues

**Error: "No module named 'app'"**
- [ ] Check you're in `backend` directory
- [ ] Check venv is activated (should see `(venv)` in prompt)
- [ ] Reinstall dependencies: `pip install -r requirements.txt`

**Error: "OPENAI_API_KEY not found"**
- [ ] Check `.env` file exists in `backend` folder
- [ ] Check `.env` has `OPENAI_API_KEY=sk-...`
- [ ] No spaces around `=` sign
- [ ] No quotes around the key

**Error: "Connection to Qdrant failed"**
- [ ] Check Qdrant URL is correct (should start with `https://`)
- [ ] Check Qdrant API key is correct
- [ ] Check your Qdrant cluster is active (login to cloud.qdrant.io)
- [ ] Run `python init_qdrant.py` again

**Error: "Cloudinary upload failed"**
- [ ] Check all three Cloudinary credentials are set
- [ ] Log into cloudinary.com and verify credentials
- [ ] Check your cloud name doesn't have spaces

### Frontend Issues

**Error: "ECONNREFUSED 127.0.0.1:8000"**
- [ ] Backend must be running first
- [ ] Check backend is on port 8000
- [ ] Check `.env.local` has correct `NEXT_PUBLIC_API_URL`

**Page shows but upload doesn't work**
- [ ] Open browser console (F12)
- [ ] Check for CORS errors
- [ ] Verify backend `.env` has `FRONTEND_URL=http://localhost:3000`
- [ ] Restart both backend and frontend

**Error: "Module not found: Can't resolve '@/components/...'"**
- [ ] Check you're in project root (not backend)
- [ ] Run `bun install` or `npm install` again
- [ ] Delete `.next` folder and restart: `rm -rf .next && bun run dev`

### Voice Issues

**Microphone doesn't work**
- [ ] Use Chrome or Edge browser (best compatibility)
- [ ] Check browser microphone permissions
- [ ] Test microphone in system settings first
- [ ] Try HTTPS instead of HTTP (for security)

**Audio playback issues**
- [ ] Check speakers/headphones are connected
- [ ] Check browser audio isn't muted
- [ ] Check OpenAI TTS is enabled in your account

## Next Steps

Once everything works:

- [ ] Read `AI_CHATBOT_README.md` for advanced features
- [ ] Customize styling in Tailwind
- [ ] Adjust chunk size for your document types
- [ ] Add more languages if needed
- [ ] Set up Redis for production sessions
- [ ] Deploy to production (see deployment guide)

## Production Deployment Checklist

When ready to deploy:

- [ ] Use production API keys (separate from testing)
- [ ] Set up Redis for session storage
- [ ] Configure production CORS origins
- [ ] Enable HTTPS only
- [ ] Set up monitoring (Sentry, LogRocket)
- [ ] Configure rate limiting
- [ ] Set up automated backups
- [ ] Add authentication (optional)
- [ ] Set up CI/CD pipeline
- [ ] Monitor API costs

## Support

If you're stuck:

1. [ ] Check error message carefully
2. [ ] Look in appropriate troubleshooting section above
3. [ ] Check `AI_CHATBOT_README.md` for detailed docs
4. [ ] Check backend logs (terminal 1)
5. [ ] Check frontend logs (browser console)
6. [ ] Run test script: `python backend/tests/test_api.py`
7. [ ] Check API documentation: http://localhost:8000/docs

## Completion

### You're done when:

✅ Backend starts without errors  
✅ Frontend loads at http://localhost:3000  
✅ Can upload a document  
✅ Can ask questions and get answers  
✅ Can switch languages  
✅ Sources are cited correctly  

**Congratulations! Your AI Document Chatbot is ready! 🎉**

---

**Time estimate**: 20-30 minutes for first-time setup

**Don't forget to**:
- Star the repo if you found it useful
- Keep your API keys secure
- Monitor your API usage to avoid surprise bills
- Have fun chatting with your documents!
