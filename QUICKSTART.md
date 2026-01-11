# Quick Start Guide - KFE Call Center

Get up and running in 5 minutes!

## 🚀 Fast Setup

### 1. Install System Dependencies

**Linux (Ubuntu/Debian):**
```bash
sudo apt-get update
sudo apt-get install python3 python3-pip python3-venv portaudio19-dev
```

**macOS:**
```bash
brew install python3 portaudio
```

**Windows:**
- Download Python 3.8+ from [python.org](https://www.python.org/downloads/)
- No additional system dependencies needed

### 2. Clone and Setup

```bash
# Clone repository
git clone https://github.com/LORDBurnItUp/KFE.git
cd KFE

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install Python packages
pip install -r requirements.txt
```

### 3. Get Your API Key

1. Go to [console.anthropic.com](https://console.anthropic.com/)
2. Sign up or log in
3. Create an API key
4. Copy the key

### 4. Configure Environment

```bash
# Copy example file
cp .env.example .env

# Edit .env with your favorite editor
nano .env  # or vim, code, notepad, etc.
```

Add your API key:
```
ANTHROPIC_API_KEY=sk-ant-api03-...your-actual-key-here...
```

### 5. Test Everything

```bash
python src/test_setup.py
```

You should see:
```
✅ All tests passed! System is ready.
```

### 6. Run It!

**For Call Center Mode:**
```bash
python src/call_center_assistant.py
```

**For Simple Voice Assistant:**
```bash
python src/voice_assistant.py
```

## 🎯 First Call Walkthrough

1. **Start the system** - Run call center assistant
2. **Press ENTER** - Simulate incoming call
3. **Greet customer** - System says "Thank you for calling..."
4. **Speak clearly** - Say something like "I need help with my account"
5. **Provide info** - When asked, give a name or ID
6. **Have conversation** - Chat naturally with the AI
7. **End call** - Say "goodbye" or "that's all"

## 🎤 Voice Tips

- Speak clearly and at normal volume
- Wait for "🎤 Listening..." indicator
- Pause briefly between thoughts
- Reduce background noise if possible
- If not understood, rephrase and try again

## 📊 View Analytics

After handling some calls:

```bash
python src/call_analytics.py report
```

## 🆘 Common Issues

### "PyAudio not found"
```bash
# Linux
sudo apt-get install python3-pyaudio portaudio19-dev
pip install pyaudio

# macOS
brew install portaudio
pip install pyaudio
```

### "Microphone not detected"
- Check microphone is plugged in
- Check default input device in system settings
- Grant microphone permissions to terminal/Python

### "API key not configured"
- Double-check `.env` file exists
- Verify API key is correct (starts with `sk-ant-`)
- No quotes around the key in `.env`

### "Speech recognition timeout"
- Check internet connection (Google Speech API needs it)
- Speak within 5 seconds of "Listening..." message
- Try speaking louder or closer to microphone

## 🎓 Next Steps

1. **Handle more calls** - Practice with different scenarios
2. **Check analytics** - Review call quality and metrics
3. **Customize settings** - Edit `config/settings.py`
4. **Read full docs** - See `README.md` for all features

## 💡 Pro Tips

- Use `./run_call_center.sh` (or `.bat` on Windows) for automatic setup
- Review call transcripts in `logs/calls/` directory
- Check customer database in `data/customers.json`
- Monitor sentiment scores to improve service
- Adjust TTS speed in settings if too fast/slow

## 📱 Usage Patterns

### Customer Support Scenario
```
Customer: "I need help with my order"
AI: Asks for order number
Customer: Provides details
AI: Helps resolve issue
Customer: "Thank you, goodbye"
```

### Technical Support Scenario
```
Customer: "My product isn't working"
AI: Asks for troubleshooting details
Customer: Describes problem
AI: Provides solution steps
AI: Escalates if needed
```

### Billing Inquiry Scenario
```
Customer: "Question about my bill"
AI: Identifies customer account
Customer: Asks specific question
AI: Provides billing information
AI: Escalates for refunds/disputes
```

## 🔗 Useful Links

- [Full Documentation](README.md)
- [Anthropic Console](https://console.anthropic.com/)
- [GitHub Issues](https://github.com/LORDBurnItUp/KFE/issues)
- [Claude API Docs](https://docs.anthropic.com/)

---

**Questions?** Run `python src/test_setup.py` for diagnostics or check the troubleshooting section.
