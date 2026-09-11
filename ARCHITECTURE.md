# Architecture

## Verified repository components

```text
User
 ├─ Telegram bot (`telegram_bot.py`)
 ├─ Flask web interface (`web_interface.py`)
 └─ CLI/application entry point (`blaze_copilot.py`)
                 │
                 ├─ conversation-history helpers
                 └─ retrieval interface imported from `blaze_docs`
```

`web_interface.py` exposes routes for the application home page, queries, history, history search, and status. The Telegram integration reads `TELEGRAM_BOT_TOKEN` and `ADMIN_CHAT_ID` from the local environment.

## Current boundary

The repository imports `blaze_docs.BlazeQuery.query_blaze`, but the `blaze_docs` package and its documentation/index artifacts are not checked in. This repository should therefore be treated as an integration layer rather than a self-contained runnable release until that dependency is supplied and documented.

## Operational guidance

Keep provider credentials in a local `.env` file, never in source control. Validate generated responses against source documentation before relying on them for support decisions.