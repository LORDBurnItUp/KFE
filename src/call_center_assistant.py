#!/usr/bin/env python3
"""
Professional Call Center Voice Assistant powered by Claude AI
Features: Call logging, customer tracking, sentiment analysis, IVR, escalation
"""

import os
import sys
import time
import json
import uuid
from datetime import datetime
from pathlib import Path
import speech_recognition as sr
import pyttsx3
from anthropic import Anthropic
from dotenv import load_dotenv


class CallLogger:
    """Handles call logging and transcript storage"""

    def __init__(self, log_dir="logs/calls"):
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(parents=True, exist_ok=True)
        self.current_call = None

    def start_call(self, call_id=None):
        """Start a new call session"""
        self.current_call = {
            "call_id": call_id or str(uuid.uuid4()),
            "start_time": datetime.now().isoformat(),
            "transcript": [],
            "customer_info": {},
            "sentiment_scores": [],
            "topics": [],
            "escalated": False,
            "resolution": None
        }
        return self.current_call["call_id"]

    def log_exchange(self, speaker, text, sentiment=None):
        """Log a conversation exchange"""
        if not self.current_call:
            return

        entry = {
            "timestamp": datetime.now().isoformat(),
            "speaker": speaker,
            "text": text
        }

        if sentiment:
            entry["sentiment"] = sentiment
            self.current_call["sentiment_scores"].append(sentiment)

        self.current_call["transcript"].append(entry)

    def end_call(self, resolution="completed"):
        """End the call and save transcript"""
        if not self.current_call:
            return

        self.current_call["end_time"] = datetime.now().isoformat()
        self.current_call["resolution"] = resolution

        # Calculate call duration
        start = datetime.fromisoformat(self.current_call["start_time"])
        end = datetime.fromisoformat(self.current_call["end_time"])
        self.current_call["duration_seconds"] = (end - start).total_seconds()

        # Calculate average sentiment
        if self.current_call["sentiment_scores"]:
            avg_sentiment = sum(self.current_call["sentiment_scores"]) / len(self.current_call["sentiment_scores"])
            self.current_call["average_sentiment"] = avg_sentiment

        # Save to file
        filename = f"{self.current_call['call_id']}.json"
        filepath = self.log_dir / filename

        with open(filepath, 'w') as f:
            json.dump(self.current_call, f, indent=2)

        print(f"\n📋 Call transcript saved: {filepath}")
        return self.current_call


class CustomerDatabase:
    """Simple customer information database"""

    def __init__(self, db_file="data/customers.json"):
        self.db_file = Path(db_file)
        self.db_file.parent.mkdir(parents=True, exist_ok=True)
        self.customers = self._load()

    def _load(self):
        """Load customer database"""
        if self.db_file.exists():
            with open(self.db_file, 'r') as f:
                return json.load(f)
        return {}

    def _save(self):
        """Save customer database"""
        with open(self.db_file, 'w') as f:
            json.dump(self.customers, f, indent=2)

    def get_customer(self, customer_id):
        """Retrieve customer information"""
        return self.customers.get(customer_id)

    def update_customer(self, customer_id, info):
        """Update customer information"""
        if customer_id not in self.customers:
            self.customers[customer_id] = {
                "created": datetime.now().isoformat(),
                "call_history": []
            }

        self.customers[customer_id].update(info)
        self.customers[customer_id]["last_updated"] = datetime.now().isoformat()
        self._save()

    def add_call_history(self, customer_id, call_id):
        """Add call to customer history"""
        if customer_id in self.customers:
            self.customers[customer_id]["call_history"].append({
                "call_id": call_id,
                "timestamp": datetime.now().isoformat()
            })
            self._save()


class CallCenterAssistant:
    """Professional Call Center Voice Assistant"""

    def __init__(self):
        """Initialize the call center assistant"""
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

        # Initialize call center components
        self.call_logger = CallLogger()
        self.customer_db = CustomerDatabase()

        # Call state
        self.current_call_id = None
        self.customer_id = None
        self.conversation_history = []
        self.call_reason = None

        # Configure recognizer
        self.recognizer.energy_threshold = 4000
        self.recognizer.dynamic_energy_threshold = True
        self.recognizer.pause_threshold = 0.8

        # System prompt for call center operations
        self.system_context = """You are a professional call center AI assistant. Your role is to:
- Greet customers warmly and professionally
- Identify the reason for their call
- Provide accurate and helpful information
- Show empathy and understanding
- Resolve issues efficiently
- Escalate to human agents when necessary
- Maintain a positive and professional tone

Always be concise but thorough. Ask clarifying questions when needed.
If you cannot help with something, politely offer to transfer to a specialist."""

        print("✅ Call Center Assistant initialized successfully!")

    def _configure_tts(self):
        """Configure text-to-speech for professional sound"""
        self.tts_engine.setProperty('rate', 165)  # Slightly slower for clarity
        self.tts_engine.setProperty('volume', 0.95)

        voices = self.tts_engine.getProperty('voices')
        if voices:
            # Prefer professional-sounding voice
            voice_index = 1 if len(voices) > 1 else 0
            self.tts_engine.setProperty('voice', voices[voice_index].id)

    def listen(self, timeout=10):
        """Listen to microphone and convert speech to text"""
        print("\n🎤 Listening...")

        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=0.5)

            try:
                audio = self.recognizer.listen(source, timeout=timeout, phrase_time_limit=20)
                print("🔄 Processing speech...")

                text = self.recognizer.recognize_google(audio)
                print(f"📝 Customer: {text}")

                # Log the customer input
                self.call_logger.log_exchange("customer", text)

                return text

            except sr.WaitTimeoutError:
                print("⏱️  No response detected.")
                return None
            except sr.UnknownValueError:
                print("❌ Could not understand audio.")
                return None
            except sr.RequestError as e:
                print(f"❌ Speech recognition error: {e}")
                return None

    def speak(self, text):
        """Convert text to speech with logging"""
        print(f"\n🤖 Assistant: {text}")

        # Log the assistant response
        self.call_logger.log_exchange("assistant", text)

        try:
            self.tts_engine.say(text)
            self.tts_engine.runAndWait()
        except Exception as e:
            print(f"❌ TTS error: {e}")

    def analyze_sentiment(self, text):
        """Analyze customer sentiment (1-5 scale)"""
        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=50,
                messages=[{
                    "role": "user",
                    "content": f"""Analyze the sentiment of this customer message on a scale of 1-5:
1 = Very Negative
2 = Negative
3 = Neutral
4 = Positive
5 = Very Positive

Message: "{text}"

Respond with ONLY a number 1-5."""
                }]
            )

            sentiment = float(response.content[0].text.strip())
            return max(1, min(5, sentiment))  # Ensure 1-5 range

        except Exception as e:
            print(f"⚠️  Sentiment analysis error: {e}")
            return 3  # Default to neutral

    def chat_with_claude(self, user_message, analyze_sentiment_flag=True):
        """Send message to Claude and get response"""
        try:
            # Analyze sentiment
            sentiment = None
            if analyze_sentiment_flag:
                sentiment = self.analyze_sentiment(user_message)
                if sentiment <= 2:
                    print(f"⚠️  Negative sentiment detected ({sentiment}/5)")

            # Add user message to history
            self.conversation_history.append({
                "role": "user",
                "content": user_message
            })

            print("🤔 Analyzing...")

            # Create message with system context
            messages = [
                {
                    "role": "user",
                    "content": self.system_context
                },
                {
                    "role": "assistant",
                    "content": "I understand. I will act as a professional call center assistant."
                }
            ] + self.conversation_history

            # Get response from Claude
            response = self.client.messages.create(
                model=self.model,
                max_tokens=2048,
                messages=messages
            )

            assistant_message = response.content[0].text

            # Add to history
            self.conversation_history.append({
                "role": "assistant",
                "content": assistant_message
            })

            # Check for escalation keywords
            escalation_keywords = ['transfer', 'supervisor', 'manager', 'escalate', 'human agent']
            if any(keyword in assistant_message.lower() for keyword in escalation_keywords):
                print("⚠️  Escalation detected")
                self.call_logger.current_call["escalated"] = True

            return assistant_message

        except Exception as e:
            error_msg = f"Error communicating with Claude: {e}"
            print(f"❌ {error_msg}")
            return "I apologize for the technical difficulty. Let me transfer you to a specialist who can assist you better."

    def ivr_menu(self):
        """Interactive Voice Response menu"""
        self.speak("Welcome to KFE Call Center. To help you better, please tell me the reason for your call.")

        reason = self.listen(timeout=15)

        if reason:
            self.call_reason = reason
            self.call_logger.current_call["call_reason"] = reason
            return True

        return False

    def collect_customer_info(self):
        """Collect or verify customer information"""
        self.speak("May I have your customer ID or name to pull up your account?")

        response = self.listen()

        if response:
            # Simple customer ID extraction (in production, use proper validation)
            self.customer_id = response.strip()

            # Check if customer exists
            customer = self.customer_db.get_customer(self.customer_id)

            if customer:
                self.speak(f"Thank you. I have your account pulled up. How can I help you today?")
                self.call_logger.current_call["customer_info"] = customer
            else:
                self.speak("I'll create a new profile for you. How can I assist you today?")
                self.customer_db.update_customer(self.customer_id, {
                    "name": self.customer_id
                })

            # Link call to customer
            self.customer_db.add_call_history(self.customer_id, self.current_call_id)
            return True

        return False

    def handle_call(self):
        """Handle a complete customer call"""
        print("\n" + "="*70)
        print("📞 INCOMING CALL - KFE Call Center")
        print("="*70 + "\n")

        # Start call logging
        self.current_call_id = self.call_logger.start_call()
        print(f"📋 Call ID: {self.current_call_id}\n")

        # Opening greeting
        greeting = "Thank you for calling KFE Support. My name is Claude, your AI assistant. I'm here to help you today."
        self.speak(greeting)

        # IVR Menu
        if not self.ivr_menu():
            self.speak("I didn't catch that. Let me transfer you to an agent.")
            self.call_logger.end_call(resolution="transferred_no_input")
            return

        # Customer identification
        self.collect_customer_info()

        # Main conversation loop
        try:
            while True:
                # Listen for customer input
                user_input = self.listen()

                if user_input is None:
                    self.speak("Are you still there?")
                    user_input = self.listen(timeout=5)
                    if user_input is None:
                        self.speak("I'll end this call now. Thank you for contacting us.")
                        self.call_logger.end_call(resolution="customer_disconnected")
                        break
                    continue

                # Check for call end
                lower_input = user_input.lower()
                if any(word in lower_input for word in ['goodbye', 'bye', 'thank you bye', 'that\'s all']):
                    self.speak("Thank you for calling KFE Support. Is there anything else I can help you with today?")

                    confirm = self.listen(timeout=5)
                    if confirm and 'no' in confirm.lower():
                        self.speak("Great! Thank you for calling. Have a wonderful day!")
                        self.call_logger.end_call(resolution="resolved")
                        break
                    elif confirm is None:
                        self.speak("Thank you for calling. Goodbye!")
                        self.call_logger.end_call(resolution="resolved")
                        break

                # Check for escalation request
                if any(word in lower_input for word in ['supervisor', 'manager', 'human', 'real person', 'agent']):
                    self.speak("I understand you'd like to speak with a human agent. Let me transfer you now. Please hold.")
                    self.call_logger.end_call(resolution="escalated_to_human")
                    break

                # Get AI response
                response = self.chat_with_claude(user_input)

                # Speak response
                self.speak(response)

                # Check for auto-escalation
                if self.call_logger.current_call.get("escalated"):
                    time.sleep(1)
                    self.speak("I'm going to transfer you to a specialist now. Please hold.")
                    self.call_logger.end_call(resolution="escalated_by_ai")
                    break

        except KeyboardInterrupt:
            print("\n\n⚠️  Call interrupted")
            self.speak("I apologize for the interruption. Goodbye.")
            self.call_logger.end_call(resolution="system_interrupted")
        except Exception as e:
            print(f"\n❌ Call error: {e}")
            self.speak("I'm experiencing technical difficulties. Let me transfer you to an agent.")
            self.call_logger.end_call(resolution="system_error")

        # Call summary
        print("\n" + "="*70)
        print("📊 CALL SUMMARY")
        print("="*70)
        call_data = self.call_logger.current_call
        if call_data:
            print(f"Call ID: {call_data['call_id']}")
            print(f"Duration: {call_data.get('duration_seconds', 0):.1f} seconds")
            print(f"Resolution: {call_data.get('resolution', 'unknown')}")
            if 'average_sentiment' in call_data:
                print(f"Average Sentiment: {call_data['average_sentiment']:.1f}/5.0")
            print(f"Escalated: {'Yes' if call_data.get('escalated') else 'No'}")
        print("="*70 + "\n")

    def run(self):
        """Main loop for handling calls"""
        print("\n" + "="*70)
        print("🏢 KFE CALL CENTER SYSTEM - AI Assistant")
        print("="*70)
        print("\nStatus: Ready to receive calls")
        print("Press Ctrl+C at any time to exit\n")
        print("="*70 + "\n")

        try:
            while True:
                input("Press ENTER to simulate incoming call (or Ctrl+C to exit)...\n")

                # Handle the call
                self.handle_call()

                # Reset for next call
                self.conversation_history = []
                self.customer_id = None
                self.call_reason = None

                print("\n✅ Ready for next call...\n")

        except KeyboardInterrupt:
            print("\n\n👋 Shutting down call center system...")
            print("Goodbye!")


def main():
    """Main entry point"""
    try:
        assistant = CallCenterAssistant()
        assistant.run()
    except ValueError as e:
        print(f"\n❌ Configuration Error: {e}")
        print("\nPlease ensure you have set up your .env file with ANTHROPIC_API_KEY")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Fatal Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
