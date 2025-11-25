#!/bin/bash
# Simple script to run the voice assistant

echo "🚀 Starting KFE Voice Assistant..."
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "⚠️  Virtual environment not found. Creating one..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Check if requirements are installed
if ! python -c "import anthropic" 2>/dev/null; then
    echo "📦 Installing dependencies..."
    pip install -r requirements.txt
fi

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "❌ Error: .env file not found!"
    echo "Please copy .env.example to .env and add your ANTHROPIC_API_KEY"
    echo ""
    echo "Run: cp .env.example .env"
    echo "Then edit .env with your API key"
    exit 1
fi

# Run the assistant
python src/voice_assistant.py
