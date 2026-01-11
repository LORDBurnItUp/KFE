# KFE - Professional Call Center AI Assistant

A production-ready call center voice assistant powered by Claude AI with advanced features including call logging, customer tracking, sentiment analysis, IVR menus, and comprehensive analytics.

## 🌟 Features

### Core Capabilities
- 🎤 **Advanced Speech Recognition**: Natural voice input with ambient noise adjustment
- 🤖 **Claude AI Integration**: Powered by Anthropic's Claude for intelligent, context-aware responses
- 🔊 **Professional TTS**: Clear, natural text-to-speech output optimized for call centers
- 💬 **Conversation Memory**: Full context retention throughout calls

### Call Center Features
- 📞 **IVR Menu System**: Professional interactive voice response for call routing
- 📋 **Call Logging**: Automatic transcription and recording of all calls
- 👥 **Customer Database**: Track customer information and call history
- 😊 **Sentiment Analysis**: Real-time customer satisfaction monitoring
- 📊 **Call Analytics**: Comprehensive reporting and performance metrics
- ⚠️ **Smart Escalation**: Automatic detection when human intervention is needed
- 🔄 **Call Queue Management**: Handle multiple calls with proper routing

### Analytics & Reporting
- Average call duration and volume metrics
- Customer sentiment tracking (1-5 scale)
- Resolution rate and first-call resolution (FCR)
- Escalation rate monitoring
- Peak hour analysis
- Repeat caller identification
- Detailed call transcripts with timestamps

## 📋 Prerequisites

- Python 3.8 or higher
- Microphone for voice input
- Internet connection for speech recognition and Claude API
- Anthropic API key ([Get one here](https://console.anthropic.com/))

### System Requirements

#### Linux
```bash
sudo apt-get install python3-pyaudio portaudio19-dev
```

#### macOS
```bash
brew install portaudio
```

#### Windows
PyAudio will be installed via pip (pre-compiled binaries available)

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/LORDBurnItUp/KFE.git
cd KFE
```

### 2. Setup Environment

```bash
# Create virtual environment
python -m venv venv

# Activate (Linux/macOS)
source venv/bin/activate

# Activate (Windows)
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Configure API Key

```bash
# Copy example environment file
cp .env.example .env

# Edit .env and add your API key
# ANTHROPIC_API_KEY=your_actual_api_key_here
```

### 4. Test Setup

```bash
# Verify everything is configured correctly
python src/test_setup.py
```

### 5. Run the Call Center

**Option A: Use convenience scripts**
```bash
# Linux/macOS
./run_call_center.sh

# Windows
run_call_center.bat
```

**Option B: Run directly**
```bash
# Professional call center mode (recommended)
python src/call_center_assistant.py

# Simple voice assistant mode
python src/voice_assistant.py
```

## 📖 Usage Guide

### Call Center Mode

When you run the call center assistant:

1. **Press ENTER** to simulate an incoming call
2. System greets the customer professionally
3. **IVR Menu** asks for the reason for calling
4. **Customer Identification** collects customer information
5. **AI-Powered Conversation** handles the inquiry
6. **Automatic Logging** records everything
7. **Smart Escalation** transfers to humans when needed

### Voice Commands During Calls

- **"supervisor"**, **"manager"**, **"human agent"** - Request escalation
- **"goodbye"**, **"that's all"** - End the call
- Speak naturally for all other interactions

### Analytics & Reporting

View call center performance:

```bash
# Generate analytics report
python src/call_analytics.py report

# Report for last 7 days only
python src/call_analytics.py report 7

# View specific call details
python src/call_analytics.py call <call_id>

# Export detailed report to JSON
python src/call_analytics.py export report.json
```

### Claude Code Commands

If using Claude Code, you can use these slash commands:

```bash
# Run the call center assistant
/run-assistant

# Test and verify setup
/test-setup

# Analyze call logs
/analyze-calls
```

## 🏗️ Project Structure

```
KFE/
├── .claude/                      # Claude Code configuration
│   ├── commands/                 # Custom slash commands
│   │   ├── run-assistant.md
│   │   ├── test-setup.md
│   │   └── analyze-calls.md
│   └── hooks/                    # Custom hooks (future)
│
├── src/                          # Source code
│   ├── voice_assistant.py        # Simple voice assistant
│   ├── call_center_assistant.py  # Professional call center (main)
│   ├── call_analytics.py         # Analytics and reporting
│   └── test_setup.py             # Setup verification
│
├── config/                       # Configuration
│   └── settings.py               # Application settings
│
├── logs/                         # Generated logs
│   └── calls/                    # Call transcripts (JSON)
│
├── data/                         # Generated data
│   └── customers.json            # Customer database
│
├── .env.example                  # Environment template
├── .gitignore                    # Git ignore rules
├── requirements.txt              # Python dependencies
├── run.sh / run.bat              # Simple assistant launchers
├── run_call_center.sh/.bat       # Call center launchers
└── README.md                     # This file
```

## ⚙️ Configuration

### Environment Variables

Edit `.env` to configure:

```bash
# Required: Your Anthropic API key
ANTHROPIC_API_KEY=your_key_here

# Optional: Claude model selection
CLAUDE_MODEL=claude-3-5-sonnet-20241022
```

### Advanced Settings

Edit `config/settings.py` to adjust:

- Speech recognition sensitivity
- Text-to-speech speed and volume
- API token limits
- Timeout values
- Energy thresholds

## 📊 Call Analytics Report Example

```
📊 CALL CENTER ANALYTICS REPORT
================================================================================

📈 OVERALL STATISTICS
────────────────────────────────────────────────────────────────────────────────
Total Calls: 45
Average Call Duration: 245.3 seconds
Shortest Call: 42.1 seconds
Longest Call: 612.8 seconds

📋 RESOLUTION BREAKDOWN
────────────────────────────────────────────────────────────────────────────────
resolved                      : 32  ( 71.1%)
escalated_to_human           : 8   ( 17.8%)
customer_disconnected        : 5   ( 11.1%)

⚠️ ESCALATION RATE
────────────────────────────────────────────────────────────────────────────────
Escalated Calls: 8 (17.8%)

😊 CUSTOMER SENTIMENT
────────────────────────────────────────────────────────────────────────────────
Average Sentiment: 3.85/5.0

Sentiment Distribution:
  😡 Very Negative (1-2):   2 calls
  😞 Negative (2-3):        5 calls
  😐 Neutral (3-3.5):       8 calls
  😊 Positive (3.5-4.5):    22 calls
  😄 Very Positive (4.5-5): 8 calls
```

## 🔧 Troubleshooting

### Microphone Not Working

1. Check microphone is connected and set as default device
2. Grant microphone permissions to your terminal/Python
3. Run `python src/test_setup.py` to verify audio devices
4. Adjust `ENERGY_THRESHOLD` in `config/settings.py` if too sensitive

### Speech Recognition Errors

- Ensure stable internet connection (Google Speech API requires it)
- Speak clearly at a moderate pace
- Reduce background noise
- Adjust `PAUSE_THRESHOLD` if words are being cut off
- Check `python src/test_setup.py` for audio device issues

### API Errors

- Verify `ANTHROPIC_API_KEY` is correct in `.env`
- Check API quota/limits at [console.anthropic.com](https://console.anthropic.com/)
- Ensure internet connectivity
- Run `python src/test_setup.py` to verify API connection

### Python Package Issues

**PyAudio Installation Problems:**

**Linux:**
```bash
sudo apt-get install portaudio19-dev python3-pyaudio
pip install pyaudio
```

**macOS:**
```bash
brew install portaudio
pip install pyaudio
```

**Windows:**
- PyAudio typically installs via pip without issues
- If problems occur, download pre-compiled wheel from [here](https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio)

## 🎯 Best Practices for Production

### For Call Centers:

1. **Monitor Sentiment**: Track customer satisfaction in real-time
2. **Review Escalations**: Analyze why calls are escalated to improve AI responses
3. **Check Analytics Daily**: Use reporting to identify trends and issues
4. **Update Customer DB**: Keep customer information current
5. **Archive Call Logs**: Implement log rotation for long-term storage
6. **Test Regularly**: Run `test_setup.py` before production use

### Performance Optimization:

- Use faster Claude models (Haiku) for simple queries to reduce latency
- Implement call queuing for high-volume periods
- Cache common responses
- Regular model fine-tuning based on call analytics

## 🔐 Security Considerations

- **Never commit `.env`** file with real API keys
- Store customer data securely (currently uses local JSON - upgrade for production)
- Implement proper authentication for customer identification
- Review call transcripts for PII/sensitive information
- Use HTTPS for any API communications
- Regular security audits of call logs

## 📈 Roadmap

- [ ] Multi-language support
- [ ] Real-time call monitoring dashboard
- [ ] Integration with CRM systems (Salesforce, HubSpot)
- [ ] Voice biometrics for customer authentication
- [ ] Advanced NLP for intent classification
- [ ] Webhook support for external integrations
- [ ] Cloud deployment guides (AWS, Azure, GCP)
- [ ] Call recording playback
- [ ] Live agent handoff protocols

## 🤝 Contributing

Contributions are welcome! Areas for improvement:

- Additional language support
- Better sentiment analysis models
- CRM integrations
- Performance optimizations
- Documentation improvements

## 📄 License

MIT License - free to use for commercial and personal projects.

## 💬 Support

For issues or questions:
- Open an issue on [GitHub](https://github.com/LORDBurnItUp/KFE/issues)
- Check the troubleshooting section above
- Review [Anthropic's API documentation](https://docs.anthropic.com/)
- Run `python src/test_setup.py` for diagnostics

## 🙏 Acknowledgments

- Powered by [Anthropic's Claude](https://www.anthropic.com/)
- Speech recognition by [Google Cloud Speech-to-Text](https://cloud.google.com/speech-to-text)
- Text-to-speech by [pyttsx3](https://github.com/nateshmbhat/pyttsx3)
- Built with Python ❤️

---

**Production Ready**: This system is designed for real call center deployments with comprehensive logging, analytics, and error handling. Test thoroughly before production use.
