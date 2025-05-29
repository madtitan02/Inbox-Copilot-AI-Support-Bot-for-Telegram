#!/usr/bin/env python3
"""
Startup script for Blaze Telegram Bot

This script provides an easy way to start the Telegram bot with proper
environment setup and error handling.
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

def check_requirements():
    """Check if all requirements are met"""
    print("🔍 Checking requirements...")
    
    # Check if .env file exists
    env_file = Path(".env")
    if not env_file.exists():
        print("❌ .env file not found!")
        print("📝 Please create a .env file with the following variables:")
        print("   GOOGLE_API_KEY=your_google_api_key")
        print("   TELEGRAM_BOT_TOKEN=your_telegram_bot_token")
        print("   ADMIN_CHAT_ID=your_admin_chat_id (optional)")
        print("\n💡 You can copy env_example.txt to .env and fill in your values")
        return False
    
    # Load environment variables
    load_dotenv()
    
    # Check required environment variables
    required_vars = ['GOOGLE_API_KEY', 'TELEGRAM_BOT_TOKEN']
    missing_vars = []
    
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print(f"❌ Missing required environment variables: {', '.join(missing_vars)}")
        print("📝 Please add them to your .env file")
        return False
    
    # Check if vector database exists
    vector_db_path = Path("blaze_docs/BlazeQuery/data")
    if not vector_db_path.exists() or not any(vector_db_path.iterdir()):
        print("❌ Vector database not found!")
        print("🔧 Please run setup first: python blaze_copilot.py --setup")
        return False
    
    print("✅ All requirements met!")
    return True

def main():
    """Main function"""
    print("🚀 Blaze Telegram Bot Startup")
    print("=" * 40)
    
    # Check requirements
    if not check_requirements():
        print("\n❌ Setup incomplete. Please fix the issues above and try again.")
        sys.exit(1)
    
    print("\n🤖 Starting Telegram bot...")
    print("📱 Your bot is available at: https://t.me/sybau_skrt_bot")
    print("🛑 Press Ctrl+C to stop the bot")
    print("=" * 40)
    
    # Import and run the bot
    try:
        from telegram_bot import TelegramBlazeBot
        bot = TelegramBlazeBot()
        bot.run()
    except KeyboardInterrupt:
        print("\n👋 Bot stopped by user. Goodbye!")
    except Exception as e:
        print(f"\n❌ Error starting bot: {e}")
        print("\n🔧 Troubleshooting:")
        print("1. Check your internet connection")
        print("2. Verify your TELEGRAM_BOT_TOKEN is correct")
        print("3. Ensure the bot token is valid and not revoked")
        print("4. Check that all dependencies are installed: pip install -r requirements.txt")

if __name__ == "__main__":
    main() 