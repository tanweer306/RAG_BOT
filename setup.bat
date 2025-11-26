@echo off
REM AI Document Chatbot Setup Script for Windows

echo ========================================
echo AI Document Chatbot - Setup Script
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo X Python 3 is not installed. Please install Python 3.11 or higher.
    pause
    exit /b 1
)

echo [OK] Python found
python --version

REM Check if Node/Bun is installed
where bun >nul 2>&1
if %errorlevel% equ 0 (
    echo [OK] Bun found
    set PACKAGE_MANAGER=bun
) else (
    where node >nul 2>&1
    if errorlevel 1 (
        echo X Neither Bun nor Node.js is installed. Please install one.
        pause
        exit /b 1
    )
    echo [OK] Node found
    set PACKAGE_MANAGER=npm
)

echo.
echo Setting up Backend...
echo ========================
cd backend

REM Create virtual environment
if not exist "venv" (
    echo Creating Python virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install Python dependencies
echo Installing Python dependencies...
pip install -r requirements.txt

REM Create .env if it doesn't exist
if not exist ".env" (
    echo Creating .env file from example...
    copy .env.example .env
    echo.
    echo WARNING: Edit backend\.env and add your API keys:
    echo    - OPENAI_API_KEY
    echo    - QDRANT_URL and QDRANT_API_KEY
    echo    - CLOUDINARY credentials
    echo.
    pause
)

echo.
echo Initializing Qdrant collection...
python init_qdrant.py

cd ..

echo.
echo Setting up Frontend...
echo ========================

REM Create .env.local if it doesn't exist
if not exist ".env.local" (
    echo Creating .env.local file...
    echo NEXT_PUBLIC_API_URL=http://localhost:8000/api > .env.local
)

REM Install frontend dependencies
echo Installing frontend dependencies...
if "%PACKAGE_MANAGER%"=="bun" (
    bun install
) else (
    npm install
)

echo.
echo ========================================
echo Setup Complete!
echo ========================================
echo.
echo Next Steps:
echo.
echo 1. Start the backend (in one terminal):
echo    cd backend
echo    venv\Scripts\activate
echo    uvicorn app.main:app --reload
echo.
echo 2. Start the frontend (in another terminal):
if "%PACKAGE_MANAGER%"=="bun" (
    echo    bun run dev
) else (
    echo    npm run dev
)
echo.
echo 3. Open your browser:
echo    Frontend: http://localhost:3000
echo    Backend API: http://localhost:8000/docs
echo.
echo See AI_CHATBOT_README.md for detailed documentation
echo.
pause
