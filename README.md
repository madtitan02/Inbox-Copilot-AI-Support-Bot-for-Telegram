# Blaze Inbox Copilot

A Python prototype for answering questions about Blaze documentation through a retrieval-augmented workflow. The repository includes a command-line entry point, a Flask web interface, and a Telegram bot integration.

## Video tutorial

https://github.com/user-attachments/assets/64e21ddc-4529-407a-9ff6-01ddd7cacb13

> Current repository status: this checkout imports a `blaze_docs` package that is not included here. The retrieval pipeline therefore needs that package (and its configured documentation/index data) before the application can run end to end.

## Included components

- `blaze_copilot.py` — application entry point
- `conversation_history.py` — conversation-history helpers
- `web_interface.py` — Flask interface with `/`, `/query`, `/history`, `/search_history`, and `/status` routes
- `telegram_bot.py` and `run_telegram_bot.py` — Telegram bot integration
- `quick_start.py` and `demo_conversation.py` — local helper/demo scripts
- `TELEGRAM_SETUP.md` — Telegram-specific setup notes

## Technology

The checked-in Python dependencies include Flask, FAISS, sentence-transformers, Google Generative AI tooling, and `python-telegram-bot`. See `requirements.txt` and `pyproject.toml` for the authoritative dependency list.

## Setup

1. Create and activate a virtual environment.
2. Install the dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Copy `.env.example` to `.env` and supply the values required for the integrations you enable.
4. Provide the missing `blaze_docs` package and any documentation/index data required by its retrieval implementation.
5. Choose an interface:

   ```bash
   python blaze_copilot.py
   python web_interface.py
   python run_telegram_bot.py
   ```

The exact supported commands and prerequisites remain defined by the source files and `TELEGRAM_SETUP.md`.

## Environment variables

Never commit `.env` files or credentials. The repository currently references these Telegram integration variables:

- `TELEGRAM_BOT_TOKEN`
- `ADMIN_CHAT_ID`

`.env.example` intentionally contains placeholders only. Other provider configuration should be documented alongside the missing retrieval package rather than guessed here.

## Architecture

See [ARCHITECTURE.md](ARCHITECTURE.md) for the verified component boundaries and the current missing dependency.

## Demo

A video attachment is available in this repository’s GitHub README history. The public Telegram handle previously referenced here is not presented as a guaranteed live deployment; run your own instance when testing.

## Limitations

- This checkout is not self-contained because `blaze_docs` is absent.
- Documentation/index refresh behavior depends on the missing retrieval package.
- Generated answers require validation against the linked source documentation.
- No performance, accuracy, or latency claims are made without a reproducible evaluation.

## License

No license file is currently included. Choose and add a license before inviting reuse or external contributions.