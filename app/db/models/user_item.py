"""Модель предметів користувача."""

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Optional

from sqlalchemy import Boolean, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from app.db.base import Base

if TYPE_CHECKING:
    from app.db.models.item import Item
    from app.db.models.market import MarketListing
    from app.db.models.user import User


class UserItem(Base):
    """Конкретний предмет у власності користувача."""

    __tablename__ = "user_items"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    item_id: Mapped[int] = mapped_column(ForeignKey("items.id", ondelete="CASCADE"))
    serial_no: Mapped[str] = mapped_column(default="0000")
    acquired_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    locked_for_cp: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    user: Mapped["User"] = relationship(back_populates="inventory")
    item: Mapped["Item"] = relationship(back_populates="owners")
    listing: Mapped["Optional[MarketListing]"] = relationship(back_populates="user_item", uselist=False)
