#!/usr/bin/env python3
"""
Telegram Bot Integration for Blaze Inbox Copilot

This module provides a Telegram bot interface for the Blaze Inbox Copilot,
allowing users to interact with the AI support system through Telegram.
"""

import os
import logging
import asyncio
from datetime import datetime
from typing import Dict, List, Optional
from dotenv import load_dotenv

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application, 
    CommandHandler, 
    MessageHandler, 
    CallbackQueryHandler,
    filters, 
    ContextTypes
)

from blaze_copilot import BlazeCopilot
from conversation_history import ConversationHistory

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

class TelegramBlazeBot:
    """
    Telegram bot for Blaze Inbox Copilot
    """
    
    def __init__(self):
        """Initialize the Telegram bot"""
        self.bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
        if not self.bot_token:
            raise ValueError("TELEGRAM_BOT_TOKEN environment variable is required")
        
        # Initialize Blaze Copilot
        try:
            self.copilot = BlazeCopilot()
            logger.info("Blaze Copilot initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize Blaze Copilot: {e}")
            raise
        
        # Store user sessions
        self.user_sessions: Dict[int, ConversationHistory] = {}
        
        # Escalation settings
        self.escalation_threshold = 30  # Confidence threshold for escalation
        self.admin_chat_id = os.getenv('ADMIN_CHAT_ID')  # Admin chat for escalations
        
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle /start command"""
        user = update.effective_user
        chat_id = update.effective_chat.id
        
        # Initialize user session
        if chat_id not in self.user_sessions:
            self.user_sessions[chat_id] = ConversationHistory()
        
        welcome_message = f"""
🚀 **Welcome to Blaze Inbox Copilot!**

Hi {user.first_name}! I'm your AI assistant for all things Blaze. I can help you with:

• **Product Questions**: How to use Blaze features
• **Setup & Configuration**: Getting started with analytics
• **Troubleshooting**: Solving common issues
• **Best Practices**: Tips for optimal usage

**How to use:**
Just send me your question in plain text, and I'll provide detailed answers based on Blaze's documentation.

**Commands:**
/help - Show this help message
/history - Search your conversation history
/summary - Get session summary
/escalate - Contact human support

Try asking: *"How do I set up Discord analytics?"*
        """
        
        keyboard = [
            [InlineKeyboardButton("📚 Documentation", url="https://docs.withblaze.app/blaze")],
            [InlineKeyboardButton("🆘 Support", url="https://intercom.help/blaze-3d9c6d1123fd/en/")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            welcome_message, 
            parse_mode='Markdown',
            reply_markup=reply_markup
        )
        
        logger.info(f"User {user.id} ({user.username}) started the bot")

    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle /help command"""
        help_text = """
🤖 **Blaze Copilot Help**

**Available Commands:**
/start - Welcome message and introduction
/help - Show this help message
/history <search_term> - Search your conversation history
/summary - Get summary of current session
/escalate - Contact human support for complex issues

**How to Ask Questions:**
Just type your question naturally! Examples:
• "How do I update Topic Definitions for Discord analytics?"
• "How can I start a Twitter DM campaign?"
• "What are the pricing plans?"
• "How do I integrate with my CRM?"

**Response Features:**
• ✅ Confidence scoring (0-100%)
• 📚 Source documentation links
• ⚠️ Low confidence warnings
• 🔄 Conversation memory

**Need Human Help?**
If my answer isn't helpful or you need personalized assistance, use /escalate to contact the Blaze team.
        """
        
        await update.message.reply_text(help_text, parse_mode='Markdown')

    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle regular text messages"""
        user = update.effective_user
        chat_id = update.effective_chat.id
        message_text = update.message.text
        
        # Initialize user session if needed
        if chat_id not in self.user_sessions:
            self.user_sessions[chat_id] = ConversationHistory()
        
        # Show typing indicator
        await context.bot.send_chat_action(chat_id=chat_id, action="typing")
        
        try:
            # Get response from Blaze Copilot
            response = self.copilot.ask(message_text, show_details=False)
            
            # Format response for Telegram
            formatted_response = self._format_response(response)
            
            # Check if escalation is needed
            if response['confidence'] < self.escalation_threshold:
                formatted_response += self._get_escalation_message()
                
                # Notify admin if configured
                if self.admin_chat_id:
                    await self._notify_admin_low_confidence(user, message_text, response)
            
            # Create inline keyboard with actions
            keyboard = self._create_response_keyboard(response)
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            await update.message.reply_text(
                formatted_response,
                reply_markup=reply_markup,
                disable_web_page_preview=True
            )
            
            logger.info(f"Responded to user {user.id} with confidence {response['confidence']}%")
            
        except Exception as e:
            logger.error(f"Error processing message from user {user.id}: {e}")
            error_message = """
❌ Sorry, I encountered an error processing your request.

This might be a temporary issue. Please try:
1. Rephrasing your question
2. Asking a more specific question
3. Using /escalate for human assistance

The error has been logged for investigation.
            """
            await update.message.reply_text(error_message)

    async def history_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle /history command"""
        chat_id = update.effective_chat.id
        
        if chat_id not in self.user_sessions:
            await update.message.reply_text("No conversation history found. Start by asking a question!")
            return
        
        # Get search term from command arguments
        search_term = ' '.join(context.args) if context.args else None
        
        if not search_term:
            await update.message.reply_text(
                "Please provide a search term.\nExample: `/history discord analytics`",
                parse_mode='Markdown'
            )
            return
        
        # Search history
        matches = self.user_sessions[chat_id].search_history(search_term)
        
        if not matches:
            await update.message.reply_text(f"No previous conversations found about '{search_term}'")
            return
        
        # Format history results
        history_text = f"🔍 **Found {len(matches)} previous interactions about '{search_term}':**\n\n"
        
        for i, match in enumerate(matches[:5], 1):  # Limit to 5 results
            timestamp = match['timestamp']
            query = match['query'][:100] + "..." if len(match['query']) > 100 else match['query']
            answer = match['response']['ai_response']['answer'][:150] + "..." if len(match['response']['ai_response']['answer']) > 150 else match['response']['ai_response']['answer']
            confidence = match['confidence']
            
            history_text += f"**{i}.** {timestamp}\n"
            history_text += f"**Q:** {query}\n"
            history_text += f"**A:** {answer}\n"
            history_text += f"**Confidence:** {confidence}%\n\n"
        
        await update.message.reply_text(history_text, parse_mode='Markdown')

    async def summary_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle /summary command"""
        chat_id = update.effective_chat.id
        
        if chat_id not in self.user_sessions:
            await update.message.reply_text("No conversation history found. Start by asking a question!")
            return
        
        summary = self.user_sessions[chat_id].get_session_summary()
        
        summary_text = f"""
📊 **Session Summary**

**Total Questions:** {summary['total_queries']}
**Average Confidence:** {summary['avg_confidence']}%
**Main Topics:** {', '.join(summary['topics']) if summary['topics'] else 'None yet'}

Keep asking questions to build your knowledge base!
        """
        
        await update.message.reply_text(summary_text, parse_mode='Markdown')

    async def escalate_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle /escalate command"""
        user = update.effective_user
        escalation_message = f"""
🆘 **Escalation Request**

Your request has been noted for human review. A Blaze team member will get back to you soon.

**In the meantime, you can:**
• Check our [documentation](https://docs.withblaze.app/blaze)
• Browse [support articles](https://intercom.help/blaze-3d9c6d1123fd/en/)
• Continue asking me other questions

**For urgent issues:**
Contact support directly through the Blaze dashboard or email.
        """
        
        await update.message.reply_text(escalation_message, parse_mode='Markdown')
        
        # Notify admin if configured
        if self.admin_chat_id:
            admin_message = f"""
🚨 **Escalation Request**

**User:** {user.first_name} {user.last_name} (@{user.username})
**User ID:** {user.id}
**Time:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

User requested human assistance.
            """
            try:
                await context.bot.send_message(
                    chat_id=self.admin_chat_id,
                    text=admin_message,
                    parse_mode='Markdown'
                )
            except Exception as e:
                logger.error(f"Failed to notify admin: {e}")

    async def handle_callback_query(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle inline keyboard button presses"""
        query = update.callback_query
        await query.answer()
        
        data = query.data
        
        if data == "helpful_yes":
            await query.edit_message_text("✅ Great! Glad I could help!")
        elif data == "helpful_no":
            await query.edit_message_text(
                "❌ Sorry the answer wasn't helpful. Try rephrasing your question or use /escalate for human assistance."
            )
        elif data == "escalate":
            await self.escalate_command(update, context)

    def _format_response(self, response: dict) -> str:
        """Format the copilot response for Telegram"""
        confidence = response['confidence']
        answer = response['answer']
        sources = response['sources']
        
        # Clean the answer text to remove problematic formatting
        clean_answer = self._clean_text_for_telegram(answer)
        
        # Confidence indicator
        if confidence >= 80:
            confidence_emoji = "🟢"
        elif confidence >= 50:
            confidence_emoji = "🟡"
        else:
            confidence_emoji = "🔴"
        
        formatted_text = f"{confidence_emoji} Confidence: {confidence}%\n\n"
        formatted_text += f"{clean_answer}\n\n"
        
        # Add sources if available
        if sources:
            formatted_text += "📚 Sources:\n"
            for i, source in enumerate(sources[:3], 1):
                title = source['title'][:50] + "..." if len(source['title']) > 50 else source['title']
                formatted_text += f"{i}. {title}\n"
        
        # Add warning for low confidence
        if confidence < 50:
            formatted_text += "\n⚠️ Low confidence warning: This answer might not be accurate. Consider asking for clarification or checking the documentation directly."
        
        return formatted_text

    def _clean_text_for_telegram(self, text: str) -> str:
        """Clean text to avoid Telegram Markdown parsing issues"""
        if not text:
            return text
        
        # Remove problematic markdown formatting
        text = text.replace('**', '')  # Remove bold markdown
        text = text.replace('***', '')  # Remove bold+italic
        text = text.replace('****', '')  # Remove any quadruple asterisks
        
        # Clean up any remaining formatting issues
        text = text.replace('_', '')  # Remove italic markdown
        text = text.replace('`', '')  # Remove code markdown
        
        return text

    def _create_response_keyboard(self, response: dict) -> List[List[InlineKeyboardButton]]:
        """Create inline keyboard for response actions"""
        keyboard = [
            [
                InlineKeyboardButton("👍 Helpful", callback_data="helpful_yes"),
                InlineKeyboardButton("👎 Not Helpful", callback_data="helpful_no")
            ]
        ]
        
        # Add escalation button for low confidence responses
        if response['confidence'] < self.escalation_threshold:
            keyboard.append([InlineKeyboardButton("🆘 Contact Human Support", callback_data="escalate")])
        
        return keyboard

    def _get_escalation_message(self) -> str:
        """Get escalation message for low confidence responses"""
        return "\n\n🤔 **Not sure about this answer?** Use /escalate to contact human support."

    async def _notify_admin_low_confidence(self, user, query: str, response: dict) -> None:
        """Notify admin about low confidence response"""
        if not self.admin_chat_id:
            return
        
        admin_message = f"""
⚠️ **Low Confidence Response Alert**

**User:** {user.first_name} {user.last_name} (@{user.username})
**User ID:** {user.id}
**Query:** {query}
**Confidence:** {response['confidence']}%
**Time:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

**Bot Response:** {response['answer'][:200]}...

Consider reaching out to provide better assistance.
        """
        
        try:
            await self.application.bot.send_message(
                chat_id=self.admin_chat_id,
                text=admin_message,
                parse_mode='Markdown'
            )
        except Exception as e:
            logger.error(f"Failed to notify admin about low confidence: {e}")

    def run(self) -> None:
        """Run the Telegram bot"""
        # Create application
        self.application = Application.builder().token(self.bot_token).build()
        
        # Add handlers
        self.application.add_handler(CommandHandler("start", self.start_command))
        self.application.add_handler(CommandHandler("help", self.help_command))
        self.application.add_handler(CommandHandler("history", self.history_command))
        self.application.add_handler(CommandHandler("summary", self.summary_command))
        self.application.add_handler(CommandHandler("escalate", self.escalate_command))
        self.application.add_handler(CallbackQueryHandler(self.handle_callback_query))
        self.application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message))
        
        # Start the bot
        logger.info("Starting Blaze Telegram Bot...")
        self.application.run_polling(allowed_updates=Update.ALL_TYPES)


def main():
    """Main function to run the Telegram bot"""
    try:
        bot = TelegramBlazeBot()
        bot.run()
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
    except Exception as e:
        logger.error(f"Bot failed to start: {e}")
        print(f"Error: {e}")
        print("\nMake sure you have:")
        print("1. Set TELEGRAM_BOT_TOKEN in your .env file")
        print("2. Set GOOGLE_API_KEY in your .env file")
        print("3. Run the setup: python blaze_copilot.py --setup")
        print("4. Optionally set ADMIN_CHAT_ID for escalation notifications")


if __name__ == "__main__":
    main() 