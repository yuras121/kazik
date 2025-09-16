"""Модель користувача."""

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Optional

from sqlalchemy import BigInteger, DateTime, ForeignKey, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from app.db.models.tx import Transaction
    from app.db.models.user_item import UserItem


class User(Base):
    """Telegram-користувач у грі."""

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id: Mapped[int] = mapped_column(BigInteger, unique=True, index=True)
    username: Mapped[str | None] = mapped_column(String(64), nullable=True)

    vusd: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    cp: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    mythic_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    ref_code: Mapped[str] = mapped_column(String(16), unique=True)
    referrer_id: Mapped[int | None] = mapped_column(ForeignKey("users.id", ondelete="SET NULL"), nullable=True)

    daily_claimed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    pity_counter: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    referrer: Mapped["Optional[User]"] = relationship(remote_side="User.id", backref="referrals", lazy="joined")
    inventory: Mapped[list["UserItem"]] = relationship(back_populates="user", cascade="all, delete-orphan")
    transactions: Mapped[list["Transaction"]] = relationship(back_populates="user", cascade="all, delete-orphan")
