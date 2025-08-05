"""Telegram bot command handlers for the KI Life Coach bot."""

from __future__ import annotations

import logging
from telegram import Update
from telegram.ext import ContextTypes

logger = logging.getLogger(__name__)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle the ``/start`` command.

    Sends a greeting and a short description of the project.
    """
    try:
        message = (
            "Willkommen beim KI Life Coach Bot!\n\n"
            "Ich unterstütze dich beim Mood-Tracking, GPT-Coaching "
            "und Habit-Tracking."
        )
        await update.message.reply_text(message)
    except Exception:
        logger.exception("Failed to handle /start command")
        raise


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle the ``/help`` command.

    Provides a brief overview of available bot commands.
    """
    try:
        message = (
            "Verfügbare Befehle:\n"
            "/start - Begrüßung und Projektüberblick\n"
            "/help - Zeigt diese Hilfe an"
        )
        await update.message.reply_text(message)
    except Exception:
        logger.exception("Failed to handle /help command")
        raise
