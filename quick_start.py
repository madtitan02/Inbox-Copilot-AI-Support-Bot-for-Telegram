#!/usr/bin/env python3
"""
Quick Start Script for Blaze Telegram Bot

This script guides users through the complete setup process
for the Blaze Inbox Copilot Telegram bot.
"""

import os
import sys
import subprocess
from pathlib import Path

def print_header():
    """Print welcome header"""
    print("🚀 Blaze Inbox Copilot - Telegram Bot Quick Start")
    print("=" * 55)
    print("This script will help you set up the Telegram bot integration.")
    print()

def check_python_version():
    """Check if Python version is compatible"""
    print("🔍 Checking Python version...")
    
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ is required")
        print(f"   Current version: {sys.version}")
        return False
    
    print(f"✅ Python {sys.version.split()[0]} is compatible")
    return True

def check_virtual_environment():
    """Check if virtual environment is activated"""
    print("🔍 Checking virtual environment...")
    
    if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        print("✅ Virtual environment is activated")
        return True
    else:
        print("⚠️  Virtual environment not detected")
        print("💡 It's recommended to use a virtual environment")
        
        response = input("Continue anyway? (y/N): ").strip().lower()
        return response in ['y', 'yes']

def install_dependencies():
    """Install required dependencies"""
    print("📦 Installing dependencies...")
    
    try:
        # Try uv first
        result = subprocess.run(['uv', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print("Using uv package manager...")
            subprocess.run(['uv', 'pip', 'install', '-r', 'requirements.txt'], check=True)
        else:
            print("Using pip...")
            subprocess.run([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'], check=True)
        
        print("✅ Dependencies installed successfully")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False
    except FileNotFoundError:
        print("❌ Package manager not found")
        print("💡 Please install pip or uv")
        return False

def setup_environment():
    """Set up environment variables"""
    print("🔧 Setting up environment variables...")
    
    env_file = Path('.env')
    env_example = Path('env_example.txt')
    
    if env_file.exists():
        print("✅ .env file already exists")
        return True
    
    if not env_example.exists():
        print("❌ env_example.txt not found")
        return False
    
    # Copy example to .env
    with open(env_example, 'r') as src, open(env_file, 'w') as dst:
        content = src.read()
        dst.write(content)
    
    print("✅ Created .env file from template")
    print("📝 Please edit .env file with your API keys:")
    print("   - GOOGLE_API_KEY: Get from Google AI Studio")
    print("   - TELEGRAM_BOT_TOKEN: Already provided")
    print("   - ADMIN_CHAT_ID: Optional, for escalation notifications")
    
    input("\nPress Enter when you've updated the .env file...")
    return True

def verify_environment():
    """Verify environment variables are set"""
    print("🔍 Verifying environment variables...")
    
    from dotenv import load_dotenv
    load_dotenv()
    
    required_vars = ['GOOGLE_API_KEY', 'TELEGRAM_BOT_TOKEN']
    missing_vars = []
    
    for var in required_vars:
        value = os.getenv(var)
        if not value or value == f'your_{var.lower()}_here':
            missing_vars.append(var)
    
    if missing_vars:
        print(f"❌ Missing or placeholder values for: {', '.join(missing_vars)}")
        print("📝 Please update your .env file with real values")
        return False
    
    print("✅ Environment variables configured")
    return True

def run_setup():
    """Run the Blaze Copilot setup"""
    print("🔧 Running Blaze Copilot setup...")
    print("This will scrape documentation and create the vector database...")
    
    try:
        subprocess.run([sys.executable, 'blaze_copilot.py', '--setup'], check=True)
        print("✅ Setup completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Setup failed: {e}")
        print("💡 Make sure your GOOGLE_API_KEY is valid")
        return False

def run_tests():
    """Run integration tests"""
    print("🧪 Running integration tests...")
    
    try:
        result = subprocess.run([sys.executable, 'test_telegram_integration.py'], 
                              capture_output=True, text=True)
        
        print(result.stdout)
        if result.stderr:
            print(result.stderr)
        
        if result.returncode == 0:
            print("✅ All tests passed")
            return True
        else:
            print("❌ Some tests failed")
            return False
            
    except FileNotFoundError:
        print("⚠️  Test script not found, skipping tests")
        return True

def start_bot():
    """Start the Telegram bot"""
    print("🤖 Starting Telegram bot...")
    print("Bot URL: https://t.me/sybau_skrt_bot")
    print("Press Ctrl+C to stop the bot")
    print("=" * 55)
    
    try:
        subprocess.run([sys.executable, 'run_telegram_bot.py'])
    except KeyboardInterrupt:
        print("\n👋 Bot stopped by user")
    except Exception as e:
        print(f"❌ Error starting bot: {e}")

def main():
    """Main setup flow"""
    print_header()
    
    steps = [
        ("Checking Python version", check_python_version),
        ("Checking virtual environment", check_virtual_environment),
        ("Installing dependencies", install_dependencies),
        ("Setting up environment", setup_environment),
        ("Verifying environment", verify_environment),
        ("Running setup", run_setup),
        ("Running tests", run_tests),
    ]
    
    for step_name, step_func in steps:
        print(f"\n📋 Step: {step_name}")
        if not step_func():
            print(f"\n❌ Setup failed at: {step_name}")
            print("Please fix the issues above and try again.")
            sys.exit(1)
    
    print("\n🎉 Setup completed successfully!")
    print("Your Blaze Telegram bot is ready to use!")
    
    response = input("\nStart the bot now? (Y/n): ").strip().lower()
    if response in ['', 'y', 'yes']:
        start_bot()
    else:
        print("\n🚀 To start the bot later, run: python run_telegram_bot.py")
        print("📱 Bot URL: https://t.me/sybau_skrt_bot")

if __name__ == "__main__":
    main() 