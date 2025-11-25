@echo off
REM Simple script to run the voice assistant on Windows

echo Starting KFE Voice Assistant...
echo.

REM Check if virtual environment exists
if not exist "venv\" (
    echo Virtual environment not found. Creating one...
    python -m venv venv
)

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Check if requirements are installed
python -c "import anthropic" 2>nul
if errorlevel 1 (
    echo Installing dependencies...
    pip install -r requirements.txt
)

REM Check if .env file exists
if not exist ".env" (
    echo Error: .env file not found!
    echo Please copy .env.example to .env and add your ANTHROPIC_API_KEY
    echo.
    echo Run: copy .env.example .env
    echo Then edit .env with your API key
    pause
    exit /b 1
)

REM Run the assistant
python src\voice_assistant.py

pause
