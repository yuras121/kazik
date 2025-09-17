"""Модель фінансових транзакцій."""

from __future__ import annotations

from datetime import datetime
from enum import StrEnum
from typing import Any, TYPE_CHECKING

from sqlalchemy import JSON, DateTime, Enum, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from app.db.base import Base

if TYPE_CHECKING:
    from app.db.models.user import User


class TransactionKind(StrEnum):
    """Тип руху коштів."""

    BONUS = "bonus"
    CASE_PURCHASE = "case_purchase"
    CASE_REWARD = "case_reward"
    MARKET_SALE = "market_sale"
    MARKET_PURCHASE = "market_purchase"
    BOT_BUYOUT = "bot_buyout"
    REFERRAL = "referral"
    TRANSFER_OUT = "transfer_out"
    TRANSFER_IN = "transfer_in"
    QUEST_REWARD = "quest_reward"
    EVENT_REWARD = "event_reward"
    VIP_PURCHASE = "vip_purchase"
    AUCTION_SALE = "auction_sale"


class Transaction(Base):
    """Грошова транзакція користувача."""

    __tablename__ = "transactions"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    amount: Mapped[int] = mapped_column(Integer, nullable=False)
    kind: Mapped[TransactionKind] = mapped_column(Enum(TransactionKind, name="transaction_kind"))
    meta: Mapped[dict[str, Any] | None] = mapped_column(JSON, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    user: Mapped["User"] = relationship(back_populates="transactions")
