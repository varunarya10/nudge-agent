# nudge-agent

Telegram bot that sends family members reminders, re-asks politely until they acknowledge, and understands natural replies ("done", "later", "skip today").

This is a public portfolio repo. Never add real names, phone numbers, chat IDs or message history; use synthetic examples only. It is unrelated to any other project, so don't reference code or details from other repos.

## Stack
- Python 3.13, managed with uv. Add packages with `uv add`, never pip.

## Rules
- Propose every change as a diff for me to review before it's applied.
- No secrets in the repo. Tokens live in `.env` (gitignored) and are read from environment variables.
- Commit small: one logical change per commit, with a clear message. Don't commit or push unless I ask.
- I'm catching up on modern Python, so briefly explain why, not just what.