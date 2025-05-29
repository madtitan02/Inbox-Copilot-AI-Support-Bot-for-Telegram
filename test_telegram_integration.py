#!/usr/bin/env python3
"""
Test script for Telegram Bot Integration

This script tests the core functionality of the Telegram bot
without actually connecting to Telegram servers.
"""

import os
import sys
from unittest.mock import Mock, patch
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_environment_setup():
    """Test if environment variables are properly set"""
    print("🔍 Testing environment setup...")
    
    required_vars = ['GOOGLE_API_KEY', 'TELEGRAM_BOT_TOKEN']
    missing_vars = []
    
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print(f"❌ Missing environment variables: {', '.join(missing_vars)}")
        return False
    
    print("✅ Environment variables configured")
    return True

def test_blaze_copilot_import():
    """Test if BlazeCopilot can be imported and initialized"""
    print("🔍 Testing BlazeCopilot import...")
    
    try:
        from blaze_copilot import BlazeCopilot
        print("✅ BlazeCopilot imported successfully")
        return True
    except Exception as e:
        print(f"❌ Failed to import BlazeCopilot: {e}")
        return False

def test_telegram_bot_import():
    """Test if Telegram bot modules can be imported"""
    print("🔍 Testing Telegram bot imports...")
    
    try:
        from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
        from telegram.ext import Application, CommandHandler, MessageHandler
        print("✅ Telegram modules imported successfully")
        return True
    except Exception as e:
        print(f"❌ Failed to import Telegram modules: {e}")
        print("💡 Try: pip install python-telegram-bot")
        return False

def test_telegram_bot_class():
    """Test if TelegramBlazeBot class can be imported"""
    print("🔍 Testing TelegramBlazeBot class...")
    
    try:
        from telegram_bot import TelegramBlazeBot
        print("✅ TelegramBlazeBot class imported successfully")
        return True
    except Exception as e:
        print(f"❌ Failed to import TelegramBlazeBot: {e}")
        return False

def test_mock_bot_initialization():
    """Test bot initialization with mocked dependencies"""
    print("🔍 Testing bot initialization (mocked)...")
    
    try:
        # Mock the BlazeCopilot to avoid requiring full setup
        with patch('telegram_bot.BlazeCopilot') as mock_copilot:
            mock_copilot.return_value = Mock()
            
            from telegram_bot import TelegramBlazeBot
            
            # This should work even without full setup
            bot = TelegramBlazeBot()
            print("✅ TelegramBlazeBot initialized successfully (mocked)")
            return True
            
    except Exception as e:
        print(f"❌ Failed to initialize TelegramBlazeBot: {e}")
        return False

def test_response_formatting():
    """Test response formatting functionality"""
    print("🔍 Testing response formatting...")
    
    try:
        with patch('telegram_bot.BlazeCopilot') as mock_copilot:
            mock_copilot.return_value = Mock()
            
            from telegram_bot import TelegramBlazeBot
            bot = TelegramBlazeBot()
            
            # Test response formatting
            test_response = {
                'confidence': 85,
                'answer': 'This is a test answer about Blaze features.',
                'sources': [
                    {
                        'title': 'Test Documentation',
                        'url': 'https://docs.withblaze.app/test',
                        'score': 0.95
                    }
                ]
            }
            
            formatted = bot._format_response(test_response)
            
            # Check if formatting includes key elements
            assert '85%' in formatted
            assert 'This is a test answer' in formatted
            assert 'Test Documentation' in formatted
            assert '🟢' in formatted  # High confidence emoji
            
            print("✅ Response formatting works correctly")
            return True
            
    except Exception as e:
        print(f"❌ Response formatting test failed: {e}")
        return False

def test_keyboard_creation():
    """Test inline keyboard creation"""
    print("🔍 Testing keyboard creation...")
    
    try:
        with patch('telegram_bot.BlazeCopilot') as mock_copilot:
            mock_copilot.return_value = Mock()
            
            from telegram_bot import TelegramBlazeBot
            bot = TelegramBlazeBot()
            
            # Test keyboard creation for high confidence
            high_conf_response = {'confidence': 90}
            keyboard = bot._create_response_keyboard(high_conf_response)
            
            # Should have helpful/not helpful buttons
            assert len(keyboard) >= 1
            assert len(keyboard[0]) == 2  # Two buttons in first row
            
            # Test keyboard creation for low confidence
            low_conf_response = {'confidence': 20}
            keyboard = bot._create_response_keyboard(low_conf_response)
            
            # Should have escalation button too
            assert len(keyboard) >= 2
            
            print("✅ Keyboard creation works correctly")
            return True
            
    except Exception as e:
        print(f"❌ Keyboard creation test failed: {e}")
        return False

def run_all_tests():
    """Run all tests and report results"""
    print("🚀 Running Telegram Bot Integration Tests")
    print("=" * 50)
    
    tests = [
        test_environment_setup,
        test_blaze_copilot_import,
        test_telegram_bot_import,
        test_telegram_bot_class,
        test_mock_bot_initialization,
        test_response_formatting,
        test_keyboard_creation
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
            print()
        except Exception as e:
            print(f"❌ Test {test.__name__} crashed: {e}")
            print()
    
    print("=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Telegram bot integration is ready.")
        print("🚀 You can now run: python run_telegram_bot.py")
    else:
        print("⚠️  Some tests failed. Please check the issues above.")
        print("💡 Make sure you have:")
        print("   1. Set up environment variables (.env file)")
        print("   2. Installed all dependencies (pip install -r requirements.txt)")
        print("   3. Run the setup (python blaze_copilot.py --setup)")
    
    return passed == total

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1) 