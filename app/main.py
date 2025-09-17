"""Точка входу Telegram-бота."""

from __future__ import annotations

import asyncio
import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.dispatcher.event.bases import ErrorEvent
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

from app.config import get_settings
from app.db.base import init_db
from app.handlers import register_handlers
from app.texts.ua import GENERIC_ERROR


async def main() -> None:
    """Запускає бот у режимі long polling."""

    settings = get_settings()

    log_path = Path(settings.log_file)
    log_path.parent.mkdir(parents=True, exist_ok=True)
    handlers = [logging.StreamHandler()]
    handlers.append(RotatingFileHandler(log_path, maxBytes=1_000_000, backupCount=5))
    logging.basicConfig(
        level=logging.INFO,
        handlers=handlers,
        format="[%(asctime)s] %(levelname)s:%(name)s:%(message)s",
    )

    bot = Bot(
        token=settings.bot_token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    dp = Dispatcher(storage=MemoryStorage())

    register_handlers(dp)

    @dp.errors()
    async def on_error(event: ErrorEvent) -> None:
        """Глобальний обробник помилок."""

        logging.exception("Помилка обробки апдейту", exc_info=event.exception)
        update = event.update
        message = None
        if update:
            message = getattr(update, "message", None)
            if message is None and getattr(update, "callback_query", None):
                message = update.callback_query.message
        if message:
            try:
                await message.answer(GENERIC_ERROR)
            except Exception:  # noqa: BLE001 - не хочемо падати повторно
                logging.getLogger(__name__).debug("Не вдалося надіслати повідомлення про помилку")

    await init_db()

    logging.getLogger(__name__).info("Стартуємо long polling…")
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.getLogger(__name__).info("Бот вимкнено")
