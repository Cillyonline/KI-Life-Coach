"""Entry point for the Telegram bot."""
import logging
from telegram.ext import Application


async def start_bot(token: str) -> None:
    """Start the Telegram bot.

    Args:
        token: Telegram bot token.
    """
    try:
        application = Application.builder().token(token).build()
        await application.initialize()
        await application.start()
        await application.updater.start_polling()
    except Exception as exc:
        logging.exception("Failed to start bot: %s", exc)
        raise


def main() -> None:
    """Load configuration and launch the bot."""
    logging.basicConfig(level=logging.INFO)
    token = "YOUR_TELEGRAM_BOT_TOKEN"
    import asyncio

    asyncio.run(start_bot(token))


if __name__ == "__main__":
    main()
