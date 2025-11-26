#!/bin/bash

# AI Document Chatbot Setup Script
# This script helps you set up the entire application

echo "🚀 AI Document Chatbot - Setup Script"
echo "======================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.11 or higher."
    exit 1
fi

echo "✅ Python found: $(python3 --version)"

# Check if Node/Bun is installed
if command -v bun &> /dev/null; then
    echo "✅ Bun found: $(bun --version)"
    PACKAGE_MANAGER="bun"
elif command -v node &> /dev/null; then
    echo "✅ Node found: $(node --version)"
    PACKAGE_MANAGER="npm"
else
    echo "❌ Neither Bun nor Node.js is installed. Please install one of them."
    exit 1
fi

echo ""
echo "📦 Setting up Backend..."
echo "========================"

cd backend

# Create virtual environment
if [ ! -d "venv" ]; then
    echo "Creating Python virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate || . venv/Scripts/activate

# Install Python dependencies
echo "Installing Python dependencies..."
pip install -r requirements.txt

# Create .env if it doesn't exist
if [ ! -f ".env" ]; then
    echo "Creating .env file from example..."
    cp .env.example .env
    echo ""
    echo "⚠️  IMPORTANT: Edit backend/.env and add your API keys:"
    echo "   - OPENAI_API_KEY"
    echo "   - QDRANT_URL and QDRANT_API_KEY"
    echo "   - CLOUDINARY credentials"
    echo ""
    read -p "Press enter to continue after updating .env file..."
fi

echo ""
echo "🎯 Initializing Qdrant collection..."
python init_qdrant.py

cd ..

echo ""
echo "📦 Setting up Frontend..."
echo "========================"

# Create .env.local if it doesn't exist
if [ ! -f ".env.local" ]; then
    echo "Creating .env.local file..."
    echo "NEXT_PUBLIC_API_URL=http://localhost:8000/api" > .env.local
fi

# Install frontend dependencies
echo "Installing frontend dependencies..."
if [ "$PACKAGE_MANAGER" = "bun" ]; then
    bun install
else
    npm install
fi

echo ""
echo "✅ Setup Complete!"
echo "=================="
echo ""
echo "🎯 Next Steps:"
echo ""
echo "1. Start the backend (in one terminal):"
echo "   cd backend"
echo "   source venv/bin/activate  # On Windows: venv\\Scripts\\activate"
echo "   uvicorn app.main:app --reload"
echo ""
echo "2. Start the frontend (in another terminal):"
if [ "$PACKAGE_MANAGER" = "bun" ]; then
    echo "   bun run dev"
else
    echo "   npm run dev"
fi
echo ""
echo "3. Open your browser:"
echo "   Frontend: http://localhost:3000"
echo "   Backend API: http://localhost:8000/docs"
echo ""
echo "4. Test the application:"
echo "   - Upload a document (PDF, DOCX, TXT, etc.)"
echo "   - Ask questions about your document"
echo "   - Try different languages"
echo "   - Test voice input/output"
echo ""
echo "📚 See AI_CHATBOT_README.md for detailed documentation"
echo ""
