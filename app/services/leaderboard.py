"""Рейтинги користувачів."""

from __future__ import annotations

from sqlalchemy import desc, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import User


async def top_by_vusd(session: AsyncSession, limit: int = 10) -> list[User]:
    """ТОП користувачів за балансом."""

    result = await session.execute(select(User).order_by(desc(User.vusd)).limit(limit))
    return result.scalars().all()


async def top_by_cp(session: AsyncSession, limit: int = 10) -> list[User]:
    """ТОП за Collector Points."""

    result = await session.execute(select(User).order_by(desc(User.cp)).limit(limit))
    return result.scalars().all()


async def top_by_mythics(session: AsyncSession, limit: int = 10) -> list[User]:
    """ТОП мисливців на міфіки."""

    result = await session.execute(select(User).order_by(desc(User.mythic_count)).limit(limit))
    return result.scalars().all()
