#!/bin/bash
# Run script for KFE Call Center

echo "🏢 KFE Call Center - Professional AI Assistant"
echo "=============================================="
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install/update dependencies
echo "📦 Checking dependencies..."
pip install -q -r requirements.txt

# Run setup test
echo ""
echo "🔧 Running system check..."
python src/test_setup.py

if [ $? -eq 0 ]; then
    echo ""
    echo "🚀 Launching Call Center..."
    echo ""
    python src/call_center_assistant.py
else
    echo ""
    echo "❌ Setup verification failed. Please fix the issues above."
    exit 1
fi
