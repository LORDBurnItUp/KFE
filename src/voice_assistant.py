#!/usr/bin/env python3
"""
Voice Assistant powered by Claude AI
Listens to voice input, processes with Claude, and speaks responses
"""

import os
import sys
import time
import speech_recognition as sr
import pyttsx3
from anthropic import Anthropic
from dotenv import load_dotenv


class VoiceAssistant:
    """Main Voice Assistant class integrating speech recognition and Claude AI"""

    def __init__(self):
        """Initialize the voice assistant with necessary components"""
        # Load environment variables
        load_dotenv()

        # Initialize Anthropic client
        api_key = os.getenv('ANTHROPIC_API_KEY')
        if not api_key:
            raise ValueError("ANTHROPIC_API_KEY not found in environment variables")

        self.client = Anthropic(api_key=api_key)
        self.model = os.getenv('CLAUDE_MODEL', 'claude-3-5-sonnet-20241022')

        # Initialize speech recognition
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()

        # Initialize text-to-speech
        self.tts_engine = pyttsx3.init()
        self._configure_tts()

        # Conversation history
        self.conversation_history = []

        # Configure recognizer for better performance
        self.recognizer.energy_threshold = 4000
        self.recognizer.dynamic_energy_threshold = True
        self.recognizer.pause_threshold = 0.8

        print("Voice Assistant initialized successfully!")

    def _configure_tts(self):
        """Configure text-to-speech engine settings"""
        # Set properties
        self.tts_engine.setProperty('rate', 175)  # Speed of speech
        self.tts_engine.setProperty('volume', 0.9)  # Volume (0.0 to 1.0)

        # Try to set a pleasant voice
        voices = self.tts_engine.getProperty('voices')
        if voices:
            # Prefer female voice if available (usually index 1)
            voice_index = 1 if len(voices) > 1 else 0
            self.tts_engine.setProperty('voice', voices[voice_index].id)

    def listen(self):
        """Listen to microphone and convert speech to text"""
        print("\n🎤 Listening... (speak now)")

        with self.microphone as source:
            # Adjust for ambient noise
            self.recognizer.adjust_for_ambient_noise(source, duration=0.5)

            try:
                # Listen for audio
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=15)

                print("🔄 Processing speech...")

                # Convert speech to text using Google Speech Recognition
                text = self.recognizer.recognize_google(audio)
                print(f"📝 You said: {text}")

                return text

            except sr.WaitTimeoutError:
                print("⏱️  No speech detected. Try again.")
                return None
            except sr.UnknownValueError:
                print("❌ Could not understand audio. Please speak clearly.")
                return None
            except sr.RequestError as e:
                print(f"❌ Speech recognition error: {e}")
                return None

    def speak(self, text):
        """Convert text to speech and play it"""
        print(f"\n🤖 Assistant: {text}")

        try:
            self.tts_engine.say(text)
            self.tts_engine.runAndWait()
        except Exception as e:
            print(f"❌ Text-to-speech error: {e}")

    def chat_with_claude(self, user_message):
        """Send message to Claude and get response"""
        try:
            # Add user message to history
            self.conversation_history.append({
                "role": "user",
                "content": user_message
            })

            print("🤔 Thinking...")

            # Create message with Claude
            response = self.client.messages.create(
                model=self.model,
                max_tokens=1024,
                messages=self.conversation_history
            )

            # Extract response text
            assistant_message = response.content[0].text

            # Add assistant response to history
            self.conversation_history.append({
                "role": "assistant",
                "content": assistant_message
            })

            return assistant_message

        except Exception as e:
            error_msg = f"Error communicating with Claude: {e}"
            print(f"❌ {error_msg}")
            return "I apologize, but I encountered an error. Please try again."

    def run(self):
        """Main loop for the voice assistant"""
        print("\n" + "="*60)
        print("🎙️  VOICE ASSISTANT powered by Claude AI")
        print("="*60)
        print("\nCommands:")
        print("  - Say 'exit', 'quit', or 'goodbye' to stop")
        print("  - Say 'clear history' to reset conversation")
        print("  - Just speak naturally for anything else!")
        print("\n" + "="*60 + "\n")

        self.speak("Hello! I'm your AI voice assistant. How can I help you today?")

        while True:
            try:
                # Listen for user input
                user_input = self.listen()

                if user_input is None:
                    continue

                # Check for exit commands
                if user_input.lower() in ['exit', 'quit', 'goodbye', 'bye']:
                    self.speak("Goodbye! Have a great day!")
                    break

                # Check for clear history command
                if 'clear history' in user_input.lower():
                    self.conversation_history = []
                    self.speak("Conversation history cleared.")
                    continue

                # Get response from Claude
                response = self.chat_with_claude(user_input)

                # Speak the response
                self.speak(response)

            except KeyboardInterrupt:
                print("\n\n👋 Interrupted by user")
                self.speak("Goodbye!")
                break
            except Exception as e:
                print(f"\n❌ Unexpected error: {e}")
                self.speak("I encountered an unexpected error. Let's try again.")


def main():
    """Main entry point"""
    try:
        assistant = VoiceAssistant()
        assistant.run()
    except ValueError as e:
        print(f"\n❌ Configuration Error: {e}")
        print("\nPlease ensure you have set up your .env file with ANTHROPIC_API_KEY")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Fatal Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
