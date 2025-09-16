"""Модель предметів колекції."""

from __future__ import annotations

from enum import StrEnum
from typing import TYPE_CHECKING

from sqlalchemy import Enum, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from app.db.models.case_item import CaseItem
    from app.db.models.user_item import UserItem


class ItemRarity(StrEnum):
    """Рідкість предмета."""

    COMMON = "common"
    RARE = "rare"
    EPIC = "epic"
    LEGENDARY = "legendary"
    MYTHIC = "mythic"


class ItemType(StrEnum):
    """Тип носія."""

    CARD = "card"
    GIF = "gif"
    ARTIFACT = "artifact"


class ItemColor(StrEnum):
    """Колірне оформлення предмета."""

    STANDARD = "standard"
    SILVER = "silver"
    GOLD = "gold"
    RAINBOW = "rainbow"


class Item(Base):
    """Базова одиниця каталогу."""

    __tablename__ = "items"

    id: Mapped[int] = mapped_column(primary_key=True)
    key: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    name: Mapped[str] = mapped_column(String(128))
    rarity: Mapped[ItemRarity] = mapped_column(Enum(ItemRarity, name="item_rarity"))
    type: Mapped[ItemType] = mapped_column(Enum(ItemType, name="item_type"))
    color: Mapped[ItemColor] = mapped_column(Enum(ItemColor, name="item_color"))
    serial_no: Mapped[int | None] = mapped_column(Integer, nullable=True)
    cp_value: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    base_buy_price: Mapped[int] = mapped_column(Integer, nullable=False)
    image_url: Mapped[str | None] = mapped_column(String(256), nullable=True)

    cases: Mapped[list["CaseItem"]] = relationship(back_populates="item")
    owners: Mapped[list["UserItem"]] = relationship(back_populates="item")
