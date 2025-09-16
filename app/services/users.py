"""Сервіси для роботи з користувачами."""

from __future__ import annotations

from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import get_settings
from app.db.models import TransactionKind, User
from app.services import economy, referrals


async def get_by_tg_id(session: AsyncSession, tg_id: int) -> Optional[User]:
    """Повертає користувача за Telegram ID."""

    return await session.scalar(select(User).where(User.tg_id == tg_id))


async def ensure_user(
    session: AsyncSession,
    tg_id: int,
    username: str | None,
    referral_code: str | None = None,
) -> tuple[User, bool]:
    """Шукає користувача або створює нового."""

    user = await get_by_tg_id(session, tg_id)
    created = False

    if not user:
        user = User(tg_id=tg_id, username=username)
        user.ref_code = await referrals.generate_unique_ref_code(session)
        referrer = None
        if referral_code:
            referrer = await referrals.find_referrer(session, referral_code)
            if referrer and referrer.id != user.id:
                user.referrer_id = referrer.id
        session.add(user)
        await session.flush()
        created = True

        settings = get_settings()
        await economy.deposit(session, user, settings.start_bonus, TransactionKind.BONUS, meta={"source": "start"})

        if user.referrer_id and referrer is not None:
            await referrals.reward_referrer(session, referrer)

    if username and user.username != username:
        user.username = username

    return user, created
