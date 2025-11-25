"""
Configuration settings for the Voice Assistant
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class Settings:
    """Application settings"""

    # Anthropic API settings
    ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY')
    CLAUDE_MODEL = os.getenv('CLAUDE_MODEL', 'claude-3-5-sonnet-20241022')

    # Speech Recognition settings
    ENERGY_THRESHOLD = 4000
    DYNAMIC_ENERGY_THRESHOLD = True
    PAUSE_THRESHOLD = 0.8
    LISTEN_TIMEOUT = 5
    PHRASE_TIME_LIMIT = 15

    # Text-to-Speech settings
    TTS_RATE = 175  # Words per minute
    TTS_VOLUME = 0.9  # 0.0 to 1.0

    # Claude API settings
    MAX_TOKENS = 1024

    @classmethod
    def validate(cls):
        """Validate required settings"""
        if not cls.ANTHROPIC_API_KEY:
            raise ValueError("ANTHROPIC_API_KEY is required")
        return True


# Export settings instance
settings = Settings()
