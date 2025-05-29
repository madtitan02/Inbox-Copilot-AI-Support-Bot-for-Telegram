# Blaze Inbox Copilot

A Retrieval-Augmented Generation (RAG) system for answering questions about Blaze platform documentation. Built with FAISS vector search, sentence transformers, and Google Gemini AI.

# Video Tutorial


https://github.com/user-attachments/assets/64e21ddc-4529-407a-9ff6-01ddd7cacb13


**🆕 NEW: Telegram Bot Integration!** 
The copilot is now available as a Telegram bot at [@sybau_skrt_bot](https://t.me/sybau_skrt_bot)

## Architecture

```
blaze-inbox-copilot/
├── blaze_docs/
│   ├── scrape_blaze_docs.py      # Documentation scraper
│   ├── scraped_content/          # Scraped documentation storage
│   └── BlazeQuery/              # RAG implementation
│       ├── create_vector_db.py   # Vector database creation
│       ├── query_blaze.py        # Query engine
│       └── data/                 # FAISS indices and metadata
├── conversation_history.py       # Session management
├── blaze_copilot.py              # Main application
├── web_interface.py              # Flask web server
├── telegram_bot.py               # 🆕 Telegram bot interface
├── run_telegram_bot.py           # 🆕 Bot startup script
├── templates/                    # Web UI
└── requirements.txt              # Dependencies
```

## Technical Stack

- **Vector Database**: FAISS with sentence-transformers embeddings
- **LLM**: Google Gemini 1.5 Flash
- **Web Framework**: Flask
- **Telegram Bot**: python-telegram-bot
- **Document Processing**: BeautifulSoup, requests
- **Embedding Model**: sentence-transformers/all-MiniLM-L6-v2

## Installation

```bash
cd utkarsh/blaze-inbox-copilot

# Activate virtual environment
source .venv/bin/activate  # Linux/Mac
# or .venv\Scripts\activate  # Windows

# Install dependencies
uv pip install -r requirements.txt
# or pip install -r requirements.txt

# Setup environment variables
cp env_example.txt .env
# Edit .env with your API keys
```

## Setup

Initialize the system by scraping documentation and creating vector database:

```bash
python blaze_copilot.py --setup
```

This process:
1. Scrapes Blaze documentation from Gitbook and Intercom
2. Generates embeddings using sentence-transformers
3. Creates FAISS index for similarity search
4. Stores metadata for source attribution

## Usage

### 🤖 Telegram Bot (Recommended)

The easiest way to use Blaze Copilot is through Telegram:

1. **Start the bot**: https://t.me/sybau_skrt_bot
2. **Or run your own instance**:
   ```bash
   python run_telegram_bot.py
   ```

**Features:**
- Natural language queries
- Confidence scoring (0-100%)
- Source documentation links
- Conversation history
- Automatic escalation for complex queries
- Admin notifications

See [TELEGRAM_SETUP.md](TELEGRAM_SETUP.md) for detailed setup instructions.

### Command Line Interface

```bash
# Interactive mode
python blaze_copilot.py --interactive

# Single query
python blaze_copilot.py --query "How do I configure Discord analytics?"
```

### Web Interface

```bash
python web_interface.py
# Access at http://localhost:5000
```

### API Endpoints

- `POST /query` - Submit questions
- `GET /history` - Retrieve conversation history
- `POST /search_history` - Search previous interactions
- `GET /status` - System status

## RAG Implementation

### Document Processing
1. **Scraping**: Extracts content from Blaze documentation sources
2. **Chunking**: Splits documents into semantic chunks
3. **Embedding**: Generates vector representations using sentence-transformers
4. **Indexing**: Creates FAISS index for efficient similarity search

### Query Processing
1. **Embedding**: Convert user query to vector representation
2. **Retrieval**: Find top-k similar documents using cosine similarity
3. **Context Assembly**: Combine retrieved documents with query
4. **Generation**: Use Gemini to generate contextual response
5. **Confidence Scoring**: AI-generated confidence assessment

### Response Structure
```json
{
  "query": "user question",
  "answer": "generated response",
  "confidence": 85,
  "sources": [
    {
      "title": "source document title",
      "url": "documentation url",
      "score": 0.892,
      "category": "gitbook"
    }
  ]
}
```

## Configuration

### Environment Variables
```env
GOOGLE_API_KEY=your_google_api_key
```

### Customization Points
- **Embedding Model**: Modify in `create_vector_db.py`
- **Similarity Threshold**: Adjust in `query_blaze.py`
- **Chunk Size**: Configure in document processing
- **Top-k Results**: Set retrieval count

## Performance Metrics

- **Vector Search**: Sub-second similarity search on 1000+ documents
- **Response Generation**: 2-5 seconds end-to-end latency
- **Confidence Scoring**: 0-100 scale with calibrated thresholds
- **Source Attribution**: Links to original documentation

## Development

### Adding New Documentation Sources
1. Extend scraping logic in `scrape_blaze_docs.py`
2. Update categorization in vector database creation
3. Rebuild vector index with new content

### Improving Retrieval
- Implement query expansion techniques
- Add re-ranking algorithms
- Use larger embedding models
- Implement hybrid search (keyword + semantic)

### Evaluation Framework
- Create ground truth Q&A dataset
- Implement automated accuracy testing
- Add user feedback collection
- Monitor confidence score calibration

## System Requirements

- Python 3.8+
- 4GB RAM (for vector operations)
- Google API access
- Internet connection (for initial setup)

## Limitations

- **Context Window**: Limited by Gemini's context length
- **Real-time Updates**: Requires manual re-scraping for new documentation
- **Hallucination Risk**: AI may generate plausible but incorrect information
- **Language Support**: English-only documentation processing

## License

MIT License
