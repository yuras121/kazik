"""Робота з реферальною програмою."""

from __future__ import annotations

from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import get_settings
from app.db.models import TransactionKind, User
from app.services import economy
from app.utils.rng import generate_ref_code


async def generate_unique_ref_code(session: AsyncSession) -> str:
    """Підбирає унікальний реферальний код."""

    while True:
        candidate = generate_ref_code()
        exists = await session.scalar(select(User).where(User.ref_code == candidate))
        if not exists:
            return candidate


async def find_referrer(session: AsyncSession, code: str) -> Optional[User]:
    """Шукає користувача за реферальним кодом."""

    return await session.scalar(select(User).where(User.ref_code == code))


async def reward_referrer(session: AsyncSession, referrer: User) -> None:
    """Видає разовий бонус за нового друга."""

    settings = get_settings()
    await economy.deposit(session, referrer, settings.referral_bonus, TransactionKind.REFERRAL, meta={"type": "invite"})


def build_ref_link(bot_username: str, code: str) -> str:
    """Формує посилання з параметром start."""

    return f"https://t.me/{bot_username}?start={code}"
