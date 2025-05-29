#!/usr/bin/env python3
"""
Demo Conversation Script

This script demonstrates how the Telegram bot would interact with users
by simulating a conversation flow.
"""

import time
from datetime import datetime

def print_message(sender, message, delay=1):
    """Print a message with sender and timestamp"""
    timestamp = datetime.now().strftime("%H:%M")
    print(f"[{timestamp}] {sender}: {message}")
    time.sleep(delay)

def print_bot_response(message, confidence=None, sources=None, delay=2):
    """Print a bot response with formatting"""
    timestamp = datetime.now().strftime("%H:%M")
    
    if confidence:
        if confidence >= 80:
            emoji = "🟢"
        elif confidence >= 50:
            emoji = "🟡"
        else:
            emoji = "🔴"
        
        print(f"[{timestamp}] 🤖 Blaze Bot: {emoji} Confidence: {confidence}%")
        print(f"                    {message}")
        
        if sources:
            print(f"                    📚 Sources:")
            for i, source in enumerate(sources, 1):
                print(f"                    {i}. {source}")
    else:
        print(f"[{timestamp}] 🤖 Blaze Bot: {message}")
    
    time.sleep(delay)

def demo_conversation():
    """Demonstrate a typical conversation with the bot"""
    print("🚀 Blaze Telegram Bot - Demo Conversation")
    print("=" * 50)
    print("This demo shows how users would interact with the bot")
    print()
    
    # User starts the bot
    print_message("👤 User", "/start")
    print_bot_response("""🚀 Welcome to Blaze Inbox Copilot!

Hi! I'm your AI assistant for all things Blaze. I can help you with:

• Product Questions: How to use Blaze features
• Setup & Configuration: Getting started with analytics
• Troubleshooting: Solving common issues
• Best Practices: Tips for optimal usage

How to use:
Just send me your question in plain text, and I'll provide detailed answers based on Blaze's documentation.

Try asking: "How do I set up Discord analytics?"
""")
    
    # User asks about Discord analytics
    print_message("👤 User", "How do I set up Discord analytics?")
    print_bot_response(
        """To set up Discord analytics in Blaze:

1. **Connect your Discord server**:
   - Go to Integrations in your Blaze dashboard
   - Click "Add Integration" and select Discord
   - Authorize Blaze to access your server

2. **Configure analytics settings**:
   - Select which channels to monitor
   - Set up Topic Definitions for categorizing messages
   - Enable sentiment analysis if needed

3. **Start monitoring**:
   - Analytics will begin collecting data immediately
   - View insights in the Analytics dashboard
   - Set up alerts for important metrics

The setup typically takes 5-10 minutes and data will start appearing within an hour.""",
        confidence=92,
        sources=[
            "Discord Integration Guide - docs.withblaze.app",
            "Analytics Setup Tutorial - support.blaze.com"
        ]
    )
    
    # User asks follow-up question
    print_message("👤 User", "What are Topic Definitions?")
    print_bot_response(
        """Topic Definitions are custom categories you create to automatically classify and organize your Discord messages.

**How they work**:
- You define keywords, phrases, or patterns
- Blaze automatically tags messages that match
- Creates organized analytics by topic

**Examples**:
- "Bug Reports": keywords like "bug", "error", "broken"
- "Feature Requests": phrases like "can we add", "would love to see"
- "Support Questions": patterns like "how do I", "help with"

**Benefits**:
- Automatic message categorization
- Topic-specific analytics and trends
- Better understanding of community discussions
- Easier content moderation

You can create unlimited Topic Definitions and modify them anytime in the Analytics settings.""",
        confidence=88,
        sources=[
            "Topic Definitions Guide - docs.withblaze.app",
            "Analytics Features - support.blaze.com"
        ]
    )
    
    # User asks about pricing
    print_message("👤 User", "What are the pricing plans?")
    print_bot_response(
        """I don't have the most current pricing information in my knowledge base. Pricing can change frequently and I want to make sure you get accurate, up-to-date information.

🤔 Not sure about this answer? Use /escalate to contact human support.

For the latest pricing details, I recommend:
• Visiting the Blaze website directly
• Contacting the sales team
• Checking your account dashboard

Would you like me to help you with anything else about Blaze features or setup?""",
        confidence=25,
        sources=[]
    )
    
    # User escalates
    print_message("👤 User", "/escalate")
    print_bot_response("""🆘 Escalation Request

Your request has been noted for human review. A Blaze team member will get back to you soon.

In the meantime, you can:
• Check our documentation: docs.withblaze.app
• Browse support articles: support.blaze.com
• Continue asking me other questions

For urgent issues:
Contact support directly through the Blaze dashboard or email.""")
    
    # User checks history
    print_message("👤 User", "/history discord")
    print_bot_response("""🔍 Found 2 previous interactions about 'discord':

1. 14:23
Q: How do I set up Discord analytics?
A: To set up Discord analytics in Blaze: 1. Connect your Discord server...
Confidence: 92%

2. 14:25
Q: What are Topic Definitions?
A: Topic Definitions are custom categories you create to automatically...
Confidence: 88%""")
    
    # User gets summary
    print_message("👤 User", "/summary")
    print_bot_response("""📊 Session Summary

Total Questions: 4
Average Confidence: 73%
Main Topics: discord, analytics, pricing, topic definitions

Keep asking questions to build your knowledge base!""")
    
    print()
    print("=" * 50)
    print("🎉 Demo completed!")
    print()
    print("Key features demonstrated:")
    print("• Natural language question answering")
    print("• Confidence scoring with visual indicators")
    print("• Source attribution and documentation links")
    print("• Automatic escalation for low-confidence responses")
    print("• Conversation history and search")
    print("• Session summaries and analytics")
    print("• Admin notifications for escalations")
    print()
    print("🚀 Ready to try the real bot? Run: python run_telegram_bot.py")
    print("📱 Or visit: https://t.me/sybau_skrt_bot")

if __name__ == "__main__":
    demo_conversation() 