"""Команда /refer."""

from __future__ import annotations

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from app.db.base import get_session
from app.services import referrals, users
from app.texts.ua import REFERRAL_MESSAGE

router = Router()


@router.message(Command("refer"))
async def cmd_refer(message: Message) -> None:
    """Надає персональне реферальне посилання."""

    if message.from_user is None:
        return

    async with get_session() as session:
        user, _ = await users.ensure_user(
            session, tg_id=message.from_user.id, username=message.from_user.username
        )
        await session.commit()

    bot_info = await message.bot.get_me()
    link = referrals.build_ref_link(bot_info.username or "", user.ref_code)
    await message.answer(REFERRAL_MESSAGE.format(link=link))
