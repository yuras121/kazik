"""Модель кейсів."""

from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import Integer, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from app.db.models.case_item import CaseItem


class Case(Base):
    """Колекційний кейс."""

    __tablename__ = "cases"

    id: Mapped[int] = mapped_column(primary_key=True)
    code: Mapped[str] = mapped_column(String(32), unique=True, index=True)
    name: Mapped[str] = mapped_column(String(128))
    price: Mapped[int] = mapped_column(Integer, nullable=False)
    pity_step: Mapped[float] = mapped_column(Numeric(scale=2), default=1.0)
    pity_threshold: Mapped[int] = mapped_column(Integer, default=10)
    cp_requirement: Mapped[int | None] = mapped_column(Integer, nullable=True)
    cover_image: Mapped[str | None] = mapped_column(String(256), nullable=True)

    items: Mapped[list["CaseItem"]] = relationship(back_populates="case", cascade="all, delete-orphan")
