# Telegram Bot Setup Guide

This guide will help you set up and deploy the Blaze Inbox Copilot Telegram bot.

## 🚀 Quick Start

### 1. Prerequisites

- Python 3.8+
- Google API key (for Gemini AI)
- Telegram bot token (already provided)
- Virtual environment activated

### 2. Environment Setup

1. **Copy the environment template:**
   ```bash
   cp env_example.txt .env
   ```

2. **Edit the .env file with your credentials:**
   ```bash
   # Google API Key for Gemini AI
   GOOGLE_API_KEY=your_google_api_key_here
   
   # Telegram Bot Token (already provided)
   TELEGRAM_BOT_TOKEN=7899482489:AAFw1ZDLtaRTTxhDwl-tAGnS5Lj6b4weRNY
   
   # Optional: Admin Chat ID for escalation notifications
   ADMIN_CHAT_ID=your_admin_chat_id_here
   ```

3. **Install dependencies:**
   ```bash
   # Activate virtual environment
   source .venv/bin/activate  # On Linux/Mac
   # or
   .venv\Scripts\activate     # On Windows
   
   # Install packages using uv (recommended)
   uv pip install -r requirements.txt
   
   # Or use regular pip
   pip install -r requirements.txt
   ```

### 3. Initialize the System

Run the setup to scrape documentation and create the vector database:

```bash
python blaze_copilot.py --setup
```

This will:
- Scrape Blaze documentation from Gitbook and Intercom
- Create embeddings using sentence-transformers
- Build FAISS vector database for similarity search

### 4. Start the Telegram Bot

```bash
python run_telegram_bot.py
```

Or directly:
```bash
python telegram_bot.py
```

## 🤖 Bot Information

- **Bot Username:** @sybau_skrt_bot
- **Bot URL:** https://t.me/sybau_skrt_bot
- **Token:** `7899482489:AAFw1ZDLtaRTTxhDwl-tAGnS5Lj6b4weRNY`

## 📱 Bot Features

### Commands
- `/start` - Welcome message and introduction
- `/help` - Show help and usage instructions
- `/history <search_term>` - Search conversation history
- `/summary` - Get session summary
- `/escalate` - Contact human support

### Capabilities
- **Natural Language Processing**: Ask questions in plain text
- **Confidence Scoring**: 0-100% confidence ratings
- **Source Attribution**: Links to original documentation
- **Conversation Memory**: Remembers context within sessions
- **Escalation System**: Automatic escalation for low-confidence responses
- **Admin Notifications**: Alerts for escalations and low-confidence responses

### Response Features
- 🟢 High confidence (80%+)
- 🟡 Medium confidence (50-79%)
- 🔴 Low confidence (<50%)
- 📚 Source documentation links
- ⚠️ Low confidence warnings
- 🆘 Escalation suggestions

## 🔧 Configuration

### Confidence Thresholds
Edit `telegram_bot.py` to adjust:
```python
self.escalation_threshold = 30  # Confidence threshold for escalation
```

### Admin Notifications
To receive escalation notifications:
1. Get your Telegram chat ID by messaging @userinfobot
2. Add it to your .env file:
   ```
   ADMIN_CHAT_ID=123456789
   ```

## 🚀 Deployment Options

### Option 1: Local Development
```bash
python run_telegram_bot.py
```

### Option 2: Background Process (Linux/Mac)
```bash
nohup python telegram_bot.py > bot.log 2>&1 &
```

### Option 3: Systemd Service (Linux)
Create `/etc/systemd/system/blaze-telegram-bot.service`:
```ini
[Unit]
Description=Blaze Telegram Bot
After=network.target

[Service]
Type=simple
User=your_username
WorkingDirectory=/path/to/blaze-inbox-copilot
Environment=PATH=/path/to/blaze-inbox-copilot/.venv/bin
ExecStart=/path/to/blaze-inbox-copilot/.venv/bin/python telegram_bot.py
Restart=always

[Install]
WantedBy=multi-user.target
```

Then:
```bash
sudo systemctl enable blaze-telegram-bot
sudo systemctl start blaze-telegram-bot
```

### Option 4: Docker (Advanced)
Create `Dockerfile`:
```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
CMD ["python", "telegram_bot.py"]
```

## 📊 Monitoring & Analytics

### Logs
The bot logs important events:
- User interactions
- Confidence scores
- Escalations
- Errors

### Metrics to Track
- **Response Time**: Average time to respond
- **Confidence Distribution**: Percentage of high/medium/low confidence responses
- **Escalation Rate**: Percentage of queries escalated
- **User Engagement**: Active users, questions per session
- **Popular Topics**: Most asked questions

## 🛡️ Security & Best Practices

### Environment Variables
- Never commit `.env` files to version control
- Use strong, unique API keys
- Rotate tokens periodically

### Rate Limiting
Consider implementing rate limiting for production:
```python
from telegram.ext import BaseRateLimiter
# Add rate limiting configuration
```

### Error Handling
The bot includes comprehensive error handling:
- Network failures
- API rate limits
- Invalid queries
- System errors

## 🔍 Troubleshooting

### Common Issues

1. **Bot not responding**
   - Check internet connection
   - Verify bot token is correct
   - Ensure bot is not stopped by Telegram

2. **Low confidence responses**
   - Update documentation in vector database
   - Retrain with more examples
   - Adjust similarity thresholds

3. **Memory issues**
   - Monitor RAM usage
   - Consider using smaller embedding models
   - Implement conversation cleanup

4. **API rate limits**
   - Implement exponential backoff
   - Use multiple API keys if needed
   - Cache frequent responses

### Debug Mode
Enable debug logging:
```python
logging.basicConfig(level=logging.DEBUG)
```

## 📈 Improvements & Roadmap

### Immediate Improvements
1. **Enhanced Context**: Better conversation memory
2. **Multi-language**: Support for multiple languages
3. **Rich Media**: Images, videos in responses
4. **Analytics Dashboard**: Web interface for metrics

### Advanced Features
1. **Voice Messages**: Speech-to-text support
2. **Group Chat**: Multi-user conversations
3. **Integration**: CRM and ticketing system integration
4. **AI Training**: Continuous learning from interactions

### Success Metrics
- **Accuracy**: >85% user satisfaction
- **Response Time**: <3 seconds average
- **Escalation Rate**: <15% of queries
- **User Retention**: >70% return users

## 🆘 Support

For issues with the bot:
1. Check this documentation
2. Review logs for errors
3. Test with simple queries first
4. Contact the development team

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details. 