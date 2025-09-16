"""Зв’язок кейсу з предметами."""

from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import Float, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from app.db.models.case import Case
    from app.db.models.item import Item


class CaseItem(Base):
    """Предмет у конкретному кейсі зі своєю вагою."""

    __tablename__ = "case_items"

    id: Mapped[int] = mapped_column(primary_key=True)
    case_id: Mapped[int] = mapped_column(ForeignKey("cases.id", ondelete="CASCADE"))
    item_id: Mapped[int] = mapped_column(ForeignKey("items.id", ondelete="CASCADE"))
    weight: Mapped[float] = mapped_column(Float, default=1.0)

    case: Mapped["Case"] = relationship(back_populates="items")
    item: Mapped["Item"] = relationship(back_populates="cases")
