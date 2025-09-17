"""Модель трейдов між гравцями."""

from __future__ import annotations

from datetime import datetime
from enum import StrEnum

from sqlalchemy import DateTime, Enum, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from app.db.base import Base


class TradeStatus(StrEnum):
    """Статус трейд-запиту."""

    OPEN = "open"
    CANCELLED = "cancelled"
    COMPLETED = "completed"


class TradeOffer(Base):
    """Запис про запит трейду між двома користувачами."""

    __tablename__ = "trade_offers"

    id: Mapped[int] = mapped_column(primary_key=True)
    creator_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    target_username: Mapped[str] = mapped_column(String(64))
    offer_item: Mapped[str] = mapped_column(String(128))
    request_item: Mapped[str] = mapped_column(String(128))
    note: Mapped[str | None] = mapped_column(String(256), nullable=True)
    status: Mapped[TradeStatus] = mapped_column(
        Enum(TradeStatus, name="trade_status"), default=TradeStatus.OPEN
    )
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    creator: Mapped["User"] = relationship(backref="trade_offers")
