"""Операції з VUSD та Collector Points."""

from __future__ import annotations

from datetime import UTC, datetime, timedelta
from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import get_settings
from app.db.models import Transaction, TransactionKind, User


async def deposit(
    session: AsyncSession,
    user: User,
    amount: int,
    kind: TransactionKind,
    meta: dict[str, Any] | None = None,
) -> Transaction:
    """Зараховує суму на баланс користувача."""

    user.vusd += amount
    tx = Transaction(user_id=user.id, amount=amount, kind=kind, meta=meta)
    session.add(tx)
    await session.flush()
    return tx


async def withdraw(
    session: AsyncSession,
    user: User,
    amount: int,
    kind: TransactionKind,
    meta: dict[str, Any] | None = None,
) -> Transaction:
    """Списує суму з балансу, якщо вистачає коштів."""

    if user.vusd < amount:
        raise ValueError("Недостатньо коштів")
    user.vusd -= amount
    tx = Transaction(user_id=user.id, amount=-amount, kind=kind, meta=meta)
    session.add(tx)
    await session.flush()
    return tx


def split_commission(amount: int, commission_rate: float) -> tuple[int, int]:
    """Розбиває суму на нетто та комісію."""

    commission = int(amount * commission_rate)
    net = amount - commission
    return net, commission


async def grant_daily_bonus(session: AsyncSession, user: User) -> bool:
    """Видає щоденний бонус, якщо 24 години вже минули."""

    settings = get_settings()
    now = datetime.now(tz=UTC)
    if user.daily_claimed_at and now - user.daily_claimed_at < timedelta(hours=24):
        return False

    user.daily_claimed_at = now
    await deposit(session, user, settings.daily_bonus, TransactionKind.BONUS, meta={"source": "daily"})

    if user.referrer_id:
        await _apply_referral_bonus(session, user)

    return True


async def _apply_referral_bonus(session: AsyncSession, referred: User) -> None:
    """Нараховує бонус рефереру, якщо ще діє програма."""

    settings = get_settings()
    if referred.referrer_id is None:
        return

    stmt = select(User).where(User.id == referred.referrer_id)
    referrer = await session.scalar(stmt)
    if not referrer:
        return

    if referred.created_at is None:
        return

    days_since_join = (datetime.now(tz=UTC) - referred.created_at).days
    if days_since_join >= settings.referral_daily_days:
        return

    bonus = int(settings.daily_bonus * settings.referral_daily_percent)
    await deposit(session, referrer, bonus, TransactionKind.REFERRAL, meta={"from": referred.id})
