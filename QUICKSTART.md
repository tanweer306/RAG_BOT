# 🚀 Quick Start Guide

Get your AI Document Chatbot running in 5 minutes!

## Step 1: Get API Keys (5 minutes)

### OpenAI API Key
1. Go to https://platform.openai.com/api-keys
2. Click "Create new secret key"
3. Copy the key (starts with `sk-`)

### Qdrant (Free Vector Database)
1. Go to https://cloud.qdrant.io/
2. Sign up (free tier includes 1GB)
3. Create a cluster
4. Copy the cluster URL and API key

### Cloudinary (Free File Storage)
1. Go to https://cloudinary.com/
2. Sign up (free tier includes 25GB)
3. Copy Cloud Name, API Key, and API Secret from dashboard

## Step 2: Run Setup Script

### On Mac/Linux:
```bash
chmod +x setup.sh
./setup.sh
```

### On Windows:
```cmd
setup.bat
```

The script will:
- ✅ Check prerequisites
- ✅ Install dependencies
- ✅ Create config files
- ✅ Initialize database

When prompted, add your API keys to `backend/.env`

## Step 3: Start the Application

### Terminal 1 - Backend:
```bash
cd backend
source venv/Scripts/activate
uvicorn app.main:app --reload
```

### Terminal 2 - Frontend:
```bash
bun run dev  # or: npm run dev
```

## Step 4: Use the App

1. Open http://localhost:3000
2. Upload a document (PDF, DOCX, TXT, etc.)
3. Ask questions about your document
4. Try different languages
5. Use voice input (click microphone icon)

## Example Questions to Try

- "What is this document about?"
- "Summarize the main points"
- "What are the key findings?"
- "Extract all dates mentioned"
- "Who are the main people/entities?"

## Need Help?

- **Backend API Docs**: http://localhost:8000/docs
- **Test API**: `cd backend && python tests/test_api.py`
- **Full Documentation**: See `AI_CHATBOT_README.md`

## Common Issues

### "Connection refused"
- Make sure backend is running on port 8000
- Check `NEXT_PUBLIC_API_URL` in `.env.local`

### "Qdrant error"
- Verify Qdrant URL and API key
- Run `python backend/init_qdrant.py`

### "File upload failed"
- Check file size < 10MB
- Verify Cloudinary credentials
- Check supported formats: PDF, DOCX, TXT, XLSX, PPTX

### "Audio not working"
- Use Chrome or Edge browser
- Allow microphone permissions
- Verify OpenAI API key has access

---

**🎉 That's it! You're ready to chat with your documents.**

For advanced features, production deployment, and customization options, see the full `AI_CHATBOT_README.md`
