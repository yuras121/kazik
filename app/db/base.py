"""Базова інфраструктура SQLAlchemy."""

from __future__ import annotations

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.sql import text

from app.config import get_settings


class Base(DeclarativeBase):
    """Базовий клас для всіх моделей."""

    pass


_settings = get_settings()
engine: AsyncEngine = create_async_engine(_settings.database_dsn, echo=False, future=True)
async_session_factory = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


@asynccontextmanager
async def get_session() -> AsyncIterator[AsyncSession]:
    """Повертає сесію бази даних як async context manager."""

    async with async_session_factory() as session:
        yield session


async def init_db() -> None:
    """Перевіряє з’єднання з базою даних."""

    async with engine.begin() as conn:
        await conn.execute(text("SELECT 1"))
