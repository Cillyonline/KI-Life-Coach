"""Telegram bot starter script for the KI Life Coach project.

This module loads the bot configuration, registers basic command handlers
and starts the polling loop. The Telegram token is read from the environment
or from a local ``.env`` file.
"""

from __future__ import annotations

import logging
import os
from pathlib import Path
from typing import Optional

from telegram.ext import Application, CommandHandler, ContextTypes

from handler import help_command, start

# Configure logging once for the whole application
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)


def _load_token() -> str:
    """Return the Telegram bot token from env or ``.env``.

    The function first checks the ``TELEGRAM_TOKEN`` environment variable.
    If it is not set, a ``.env`` file in the project root is parsed manually.

    Raises:
        RuntimeError: If no token can be found.
    """

    token: Optional[str] = os.getenv("TELEGRAM_TOKEN")
    if token:
        return token

    env_path = Path(__file__).resolve().parents[1] / ".env"
    if env_path.exists():
        for line in env_path.read_text().splitlines():
            if line.startswith("TELEGRAM_TOKEN="):
                token = line.split("=", 1)[1].strip()
                if token:
                    return token

    raise RuntimeError("TELEGRAM_TOKEN is not configured")


async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Log errors that occur within handler callbacks."""

    logger.error("Update %s caused error %s", update, context.error)


def main() -> None:
    """Start the Telegram bot."""

    token = _load_token()

    # Build the application and register command handlers
    application = Application.builder().token(token).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_error_handler(error_handler)

    logger.info("Bot is starting. Press Ctrl-C to stop.")
    application.run_polling()


if __name__ == "__main__":
    main()

