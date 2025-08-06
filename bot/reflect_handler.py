"""Handler for the ``/reflect`` command."""

from __future__ import annotations

import logging
from typing import List

from telegram import Update
from telegram.ext import ContextTypes

from services import mood_service
from services.gpt_service import GPTService

logger = logging.getLogger(__name__)

_gpt_service = GPTService()


async def reflect(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle the ``/reflect`` command.

    Args:
        update: Incoming Telegram update.
        context: Callback context from ``python-telegram-bot``.
    """
    user_id = update.effective_user.id
    try:
        style, user_text = _parse_args(context.args)
        last_mood = mood_service.get_last_mood(user_id)
        mood_text = last_mood[1] if last_mood else "unbekannt"
        prompt = f"Stimmung: {mood_text}. Nutzertext: {user_text}"
        reflection = _gpt_service.generate_reflection(prompt, user_id, style)
        message = f"{reflection}"
        if user_text:
            message += f"\n\n(Prompt: {user_text})"
        await update.message.reply_text(message)
    except RuntimeError as exc:
        await update.message.reply_text(str(exc))
    except Exception:
        logger.exception("Failed to handle /reflect command")
        await update.message.reply_text("Es ist ein unerwarteter Fehler aufgetreten.")


def _parse_args(args: List[str]) -> tuple[str, str]:
    """Return style and remaining text from command arguments.

    Args:
        args: List of arguments supplied with the ``/reflect`` command.

    Returns:
        Tuple consisting of the style and the user-provided text.
    """
    styles = {"motivierend", "analytisch", "humorvoll"}
    if args and args[0].lower() in styles:
        return args[0].lower(), " ".join(args[1:]).strip()
    return "motivierend", " ".join(args).strip()
