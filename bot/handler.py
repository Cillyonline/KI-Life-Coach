"""Telegram bot command handlers for the KI Life Coach bot."""

from __future__ import annotations

import logging
from telegram import Update
from telegram.ext import ContextTypes
from datetime import date, datetime, timedelta
from collections import Counter
import sqlite3

from services import mood_service

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
            "/help - Zeigt diese Hilfe an\n"
            "/mood <stimmung> - Speichert deine heutige Stimmung\n"
            "/moodstats - Zeigt Statistiken der letzten 7 Tage"
        )
        await update.message.reply_text(message)
    except Exception:
        logger.exception("Failed to handle /help command")
        raise


async def mood(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle the ``/mood`` command.

    Records the user's mood and replies with the last entry and a weekly summary.
    """
    user_id = update.effective_user.id
    if not context.args:
        await update.message.reply_text(
            "Bitte gib deine Stimmung an, z.B. /mood 😊 oder /mood gut"
        )
        return

    mood_text = " ".join(context.args)
    try:
        previous = mood_service.get_last_mood(user_id)
        mood_service.save_mood(user_id, mood_text, datetime.utcnow())

        start = date.today() - timedelta(days=6)
        week_entries = mood_service.get_moods(user_id, start, date.today())
        chart = "".join(m for _, m in week_entries)
        counts = Counter(m for _, m in week_entries)
        stats = ", ".join(f"{m}: {c}" for m, c in counts.items())

        response = [f"Stimmung gespeichert: {mood_text}"]
        if previous:
            prev_ts, prev_mood = previous
            response.append(
                f"Letzte Stimmung: {prev_mood} am {prev_ts:%d.%m.%Y}"
            )
        if chart:
            response.append(f"Letzte Woche: {chart}\n{stats}")
        await update.message.reply_text("\n".join(response))
    except ValueError:
        await update.message.reply_text(
            "Du hast heute bereits eine Stimmung eingetragen."
        )
    except sqlite3.Error:
        logger.exception("Database error while saving mood")
        await update.message.reply_text(
            "Beim Speichern deiner Stimmung ist ein Fehler aufgetreten."
        )
    except Exception:
        logger.exception("Failed to handle /mood command")
        await update.message.reply_text(
            "Es ist ein unerwarteter Fehler aufgetreten."
        )


async def moodstats(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle the ``/moodstats`` command.

    Sends a summary of mood counts over the last seven days.
    """
    user_id = update.effective_user.id
    try:
        start = date.today() - timedelta(days=6)
        week_entries = mood_service.get_moods(user_id, start, date.today())
        if not week_entries:
            await update.message.reply_text("Keine Einträge für die letzte Woche.")
            return
        counts = Counter(m for _, m in week_entries)
        stats = "\n".join(f"{m}: {c}" for m, c in counts.items())
        await update.message.reply_text(
            f"Stimmungsübersicht der letzten 7 Tage:\n{stats}"
        )
    except sqlite3.Error:
        logger.exception("Database error while fetching mood stats")
        await update.message.reply_text(
            "Beim Abrufen der Statistik ist ein Fehler aufgetreten."
        )
    except Exception:
        logger.exception("Failed to handle /moodstats command")
        await update.message.reply_text(
            "Es ist ein unerwarteter Fehler aufgetreten."
        )
