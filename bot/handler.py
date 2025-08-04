"""Bot handlers."""
import logging
from telegram import Update
from telegram.ext import ContextTypes


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a welcome message.

    Args:
        update: Incoming update.
        context: Telegram context.
    """
    try:
        await update.message.reply_text("Willkommen beim KI Life Coach Bot!")
    except Exception as exc:
        logging.exception("Handler error: %s", exc)
        raise
