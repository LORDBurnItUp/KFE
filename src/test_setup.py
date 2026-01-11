#!/usr/bin/env python3
"""
Test and verify call center setup
"""

import sys
import os
from pathlib import Path


def test_imports():
    """Test that all required packages are installed"""
    print("Testing Python package imports...")
    errors = []

    packages = [
        ('anthropic', 'Anthropic'),
        ('speech_recognition', 'SpeechRecognition'),
        ('pyttsx3', 'pyttsx3'),
        ('dotenv', 'python-dotenv'),
    ]

    for module, package_name in packages:
        try:
            __import__(module)
            print(f"  ✅ {package_name}")
        except ImportError:
            print(f"  ❌ {package_name} - NOT INSTALLED")
            errors.append(package_name)

    # Test PyAudio separately with better error message
    try:
        import pyaudio
        print(f"  ✅ PyAudio")
    except ImportError:
        print(f"  ❌ PyAudio - NOT INSTALLED")
        print(f"     Note: PyAudio may require system libraries.")
        print(f"     Linux: sudo apt-get install python3-pyaudio portaudio19-dev")
        print(f"     macOS: brew install portaudio")
        errors.append("PyAudio")

    return errors


def test_env_file():
    """Test that .env file exists and has API key"""
    print("\nTesting environment configuration...")

    env_file = Path(".env")
    if not env_file.exists():
        print("  ❌ .env file not found")
        print("     Create one from .env.example: cp .env.example .env")
        return False

    print("  ✅ .env file exists")

    # Load and check for API key
    from dotenv import load_dotenv
    load_dotenv()

    api_key = os.getenv('ANTHROPIC_API_KEY')
    if not api_key or api_key == 'your_api_key_here':
        print("  ❌ ANTHROPIC_API_KEY not configured")
        print("     Edit .env and add your API key")
        return False

    print("  ✅ ANTHROPIC_API_KEY configured")
    return True


def test_audio_devices():
    """Test audio input/output devices"""
    print("\nTesting audio devices...")

    try:
        import pyaudio
        pa = pyaudio.PyAudio()

        # Check input devices
        input_devices = []
        output_devices = []

        for i in range(pa.get_device_count()):
            info = pa.get_device_info_by_index(i)
            if info['maxInputChannels'] > 0:
                input_devices.append(info['name'])
            if info['maxOutputChannels'] > 0:
                output_devices.append(info['name'])

        pa.terminate()

        print(f"  ✅ Found {len(input_devices)} input device(s)")
        if input_devices:
            print(f"     Default: {input_devices[0]}")

        print(f"  ✅ Found {len(output_devices)} output device(s)")
        if output_devices:
            print(f"     Default: {output_devices[0]}")

        if not input_devices:
            print("  ⚠️  No microphone detected")
            return False

        return True

    except Exception as e:
        print(f"  ❌ Audio device error: {e}")
        return False


def test_api_connection():
    """Test connection to Anthropic API"""
    print("\nTesting Anthropic API connection...")

    try:
        from anthropic import Anthropic
        from dotenv import load_dotenv

        load_dotenv()
        api_key = os.getenv('ANTHROPIC_API_KEY')

        if not api_key or api_key == 'your_api_key_here':
            print("  ⚠️  Skipping (API key not configured)")
            return False

        client = Anthropic(api_key=api_key)

        # Simple test message
        response = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=10,
            messages=[{"role": "user", "content": "Hi"}]
        )

        print("  ✅ API connection successful")
        return True

    except Exception as e:
        print(f"  ❌ API connection failed: {e}")
        return False


def test_directories():
    """Test that required directories exist or can be created"""
    print("\nTesting directory structure...")

    directories = ['logs/calls', 'data']

    for directory in directories:
        dir_path = Path(directory)
        try:
            dir_path.mkdir(parents=True, exist_ok=True)
            print(f"  ✅ {directory}/")
        except Exception as e:
            print(f"  ❌ {directory}/ - Error: {e}")
            return False

    return True


def main():
    """Run all tests"""
    print("="*80)
    print("🔧 KFE CALL CENTER - SETUP VERIFICATION")
    print("="*80 + "\n")

    results = {}

    # Run tests
    package_errors = test_imports()
    results['packages'] = len(package_errors) == 0

    results['env'] = test_env_file()
    results['audio'] = test_audio_devices()
    results['api'] = test_api_connection()
    results['directories'] = test_directories()

    # Summary
    print("\n" + "="*80)
    print("📋 SUMMARY")
    print("="*80)

    all_passed = all(results.values())

    for test_name, passed in results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{test_name.capitalize():20s}: {status}")

    print("="*80)

    if all_passed:
        print("\n✅ All tests passed! System is ready.")
        print("\nRun the call center with:")
        print("  python src/call_center_assistant.py")
        return 0
    else:
        print("\n⚠️  Some tests failed. Please fix the issues above.")

        if package_errors:
            print("\nInstall missing packages with:")
            print("  pip install -r requirements.txt")

        return 1


if __name__ == "__main__":
    sys.exit(main())
