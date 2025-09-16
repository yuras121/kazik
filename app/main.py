"""Точка входу Telegram-бота."""

from __future__ import annotations

import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage

from app.config import get_settings
from app.db.base import init_db
from app.handlers import register_handlers


async def main() -> None:
    """Запускає бот у режимі long polling."""

    settings = get_settings()
    logging.basicConfig(
        level=logging.INFO,
        format="[%(asctime)s] %(levelname)s:%(name)s:%(message)s"
    )

    # ✅ Новий спосіб створення бота (aiogram >= 3.7)
    bot = Bot(
        token=settings.bot_token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    dp = Dispatcher(storage=MemoryStorage())

    register_handlers(dp)

    await init_db()

    logging.getLogger(__name__).info("Стартуємо long polling…")
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.getLogger(__name__).info("Бот вимкнено")
