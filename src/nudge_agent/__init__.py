"""Minimal Telegram echo bot (first step towards nudge-agent)."""

import logging
import os
import sys

from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

logging.basicConfig(format="%(asctime)s %(levelname)s %(name)s: %(message)s", level=logging.INFO)
# httpx logs every request URL at INFO, and Telegram URLs contain the bot token.
logging.getLogger("httpx").setLevel(logging.WARNING)


# Handlers are "async def" coroutines. The library calls them for each update,
# and "await" pauses this handler while the network call runs, so the bot can
# keep serving other chats in the meantime instead of blocking.
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.effective_message.reply_text("Hi! Send me any text and I'll echo it back.")


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.effective_message.reply_text(update.effective_message.text)


def main() -> None:
    token = os.environ.get("TELEGRAM_BOT_TOKEN")
    if not token:
        sys.exit("Error: the TELEGRAM_BOT_TOKEN environment variable is not set.")

    app = Application.builder().token(token).build()
    app.add_handler(CommandHandler("start", start))
    # Plain text that isn't a /command gets echoed.
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    # run_polling() is a normal (blocking) call. It creates the asyncio event
    # loop, repeatedly asks Telegram for new updates, and runs our async
    # handlers on that loop until you press Ctrl+C.
    app.run_polling(allowed_updates=Update.ALL_TYPES)
