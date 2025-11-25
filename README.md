# KFE - AI Voice Assistant

A powerful voice assistant powered by Claude AI that listens to your voice commands, processes them using advanced AI, and speaks back responses naturally.

## Features

- 🎤 **Voice Input**: Natural speech recognition using Google's speech-to-text
- 🤖 **Claude AI Integration**: Powered by Anthropic's Claude for intelligent responses
- 🔊 **Voice Output**: Text-to-speech responses for natural conversation
- 💬 **Conversation Memory**: Maintains context throughout the conversation
- ⚙️ **Configurable**: Easy configuration via environment variables

## Prerequisites

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

## Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/LORDBurnItUp/KFE.git
cd KFE
```

### 2. Create Virtual Environment

```bash
python -m venv venv

# On Linux/macOS
source venv/bin/activate

# On Windows
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure API Key

Copy the example environment file and add your Anthropic API key:

```bash
cp .env.example .env
```

Edit `.env` and add your API key:
```
ANTHROPIC_API_KEY=your_actual_api_key_here
```

### 5. Run the Assistant

```bash
python src/voice_assistant.py
```

## Usage

Once running, the voice assistant will:

1. Greet you and wait for your voice input
2. Listen when you speak (indicated by "🎤 Listening...")
3. Process your speech and send it to Claude
4. Speak the response back to you

### Voice Commands

- **"exit"**, **"quit"**, or **"goodbye"** - Stop the assistant
- **"clear history"** - Reset the conversation context
- Any other speech - Have a natural conversation!

## Configuration

### Environment Variables

Edit `.env` to configure:

- `ANTHROPIC_API_KEY` - Your Anthropic API key (required)
- `CLAUDE_MODEL` - Which Claude model to use (default: claude-3-5-sonnet-20241022)

### Advanced Settings

Edit `config/settings.py` to adjust:

- Speech recognition sensitivity
- Text-to-speech speed and volume
- API token limits
- Timeout values

## Troubleshooting

### Microphone Not Working

1. Check your microphone is connected and set as default
2. Grant microphone permissions to your terminal/Python
3. Try adjusting `ENERGY_THRESHOLD` in `config/settings.py`

### Speech Recognition Errors

- Ensure you have a stable internet connection
- Speak clearly and at a moderate pace
- Reduce background noise
- Adjust `PAUSE_THRESHOLD` if words are being cut off

### API Errors

- Verify your `ANTHROPIC_API_KEY` is correct
- Check your API quota/limits at console.anthropic.com
- Ensure you have internet connectivity

### Python Package Issues

If PyAudio installation fails:

**Windows**: Download pre-compiled wheel from [here](https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio)
```bash
pip install PyAudio‑0.2.11‑cp3x‑cp3x‑win_amd64.whl
```

**Linux**: Install portaudio development files first
```bash
sudo apt-get install portaudio19-dev python3-pyaudio
pip install pyaudio
```

## Project Structure

```
KFE/
├── src/
│   └── voice_assistant.py    # Main voice assistant application
├── config/
│   └── settings.py            # Configuration settings
├── .env.example               # Example environment variables
├── .gitignore                 # Git ignore rules
├── requirements.txt           # Python dependencies
└── README.md                  # This file
```

## Development

### Adding New Features

The codebase is modular and easy to extend:

- `VoiceAssistant.listen()` - Modify speech input processing
- `VoiceAssistant.speak()` - Customize voice output
- `VoiceAssistant.chat_with_claude()` - Adjust AI interaction
- `config/settings.py` - Add new configuration options

### Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

## License

MIT License - feel free to use this project for any purpose.

## Support

For issues or questions:
- Open an issue on GitHub
- Check the troubleshooting section above
- Review Anthropic's [API documentation](https://docs.anthropic.com/)

## Acknowledgments

- Powered by [Anthropic's Claude](https://www.anthropic.com/)
- Speech recognition by Google
- Built with Python ❤️

---

**Note**: This voice assistant requires an active internet connection for both speech recognition and Claude AI processing. Ensure you have a valid Anthropic API key before running.
