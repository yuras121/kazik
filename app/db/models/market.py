"""Модель маркетплейсу."""

from __future__ import annotations

from datetime import datetime
from enum import StrEnum
from typing import TYPE_CHECKING, Optional

from sqlalchemy import DateTime, Enum, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from app.db.base import Base

if TYPE_CHECKING:
    from app.db.models.user import User
    from app.db.models.user_item import UserItem


class ListingStatus(StrEnum):
    """Статуси лоту."""

    ACTIVE = "active"
    SOLD = "sold"
    CANCELLED = "cancelled"


class MarketListing(Base):
    """Оголошення на маркетплейсі."""

    __tablename__ = "market_listings"

    id: Mapped[int] = mapped_column(primary_key=True)
    seller_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    buyer_id: Mapped[int | None] = mapped_column(ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    user_item_id: Mapped[int] = mapped_column(ForeignKey("user_items.id", ondelete="CASCADE"), unique=True)
    price: Mapped[int] = mapped_column(Integer, nullable=False)
    status: Mapped[ListingStatus] = mapped_column(
        Enum(ListingStatus, name="listing_status"), default=ListingStatus.ACTIVE
    )
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    closed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    seller: Mapped["User"] = relationship(foreign_keys=[seller_id])
    buyer: Mapped["Optional[User]"] = relationship(foreign_keys=[buyer_id])
    user_item: Mapped["UserItem"] = relationship(back_populates="listing")
