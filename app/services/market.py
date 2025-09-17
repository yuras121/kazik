"""Логіка маркетплейсу та миттєвого викупу."""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Collection, Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.db.models import (
    Item,
    ItemRarity,
    ItemType,
    ListingStatus,
    MarketListing,
    TransactionKind,
    User,
    UserItem,
)
from app.services import economy
from app.services.pricing import calculate_buyout_price

COMMISSION_RATE = 0.05


async def list_item(session: AsyncSession, user: User, user_item: UserItem, price: int) -> MarketListing:
    """Створює лістинг на маркеті."""

    if user_item.user_id != user.id:
        raise ValueError("Це не твій предмет")
    if user_item.listing is not None:
        raise ValueError("Предмет вже на маркеті")
    if price <= 0:
        raise ValueError("Ціна має бути додатною")

    listing = MarketListing(seller_id=user.id, user_item_id=user_item.id, price=price, status=ListingStatus.ACTIVE)
    session.add(listing)
    user_item.locked_for_cp = False
    await session.flush()
    return listing


async def cancel_listing(session: AsyncSession, listing: MarketListing, by_user: User) -> None:
    """Знімає лістинг із маркету."""

    if listing.seller_id != by_user.id:
        raise ValueError("Не можна скасувати чужий лот")
    if listing.status is not ListingStatus.ACTIVE:
        return

    listing.status = ListingStatus.CANCELLED
    listing.closed_at = datetime.now(tz=UTC)
    listing.user_item.locked_for_cp = True
    await session.flush()


async def buy_listing(session: AsyncSession, buyer: User, listing: MarketListing) -> MarketListing:
    """Купівля лоту на маркетплейсі."""

    if listing.status is not ListingStatus.ACTIVE:
        raise ValueError("Лот недоступний")
    if listing.seller_id == buyer.id:
        raise ValueError("Неможливо купити власний лот")

    await economy.withdraw(session, buyer, listing.price, TransactionKind.MARKET_PURCHASE, meta={"listing": listing.id})

    seller = listing.seller
    net, commission = economy.split_commission(listing.price, COMMISSION_RATE)
    await economy.deposit(
        session, seller, net, TransactionKind.MARKET_SALE, meta={"listing": listing.id, "commission": commission}
    )

    if listing.user_item.item.rarity is ItemRarity.MYTHICAL:
        seller.mythic_count = max(0, seller.mythic_count - 1)
        buyer.mythic_count += 1

    listing.status = ListingStatus.SOLD
    listing.buyer_id = buyer.id
    listing.closed_at = datetime.now(tz=UTC)

    owned_item = listing.user_item
    owned_item.user_id = buyer.id
    owned_item.locked_for_cp = True

    await session.flush()
    return listing


async def sell_to_bot(session: AsyncSession, user: User, user_item: UserItem) -> int:
    """Миттєвий викуп предмета ботом."""

    if user_item.user_id != user.id:
        raise ValueError("Це не твій предмет")

    price = calculate_buyout_price(user_item.item)
    await economy.deposit(session, user, price, TransactionKind.BOT_BUYOUT, meta={"item": user_item.item_id})

    if user_item.item.rarity is ItemRarity.MYTHICAL:
        user.mythic_count = max(0, user.mythic_count - 1)

    await session.delete(user_item)
    await session.flush()
    return price


async def load_active_listings(
    session: AsyncSession,
    limit: int = 10,
    offset: int = 0,
    *,
    rarities: Collection[ItemRarity] | None = None,
    item_types: Collection[ItemType] | None = None,
) -> Sequence[MarketListing]:
    """Завантажує активні лоти для відображення."""

    stmt = (
        select(MarketListing)
        .options(
            selectinload(MarketListing.user_item).selectinload(UserItem.item),
            selectinload(MarketListing.seller),
        )
        .where(MarketListing.status == ListingStatus.ACTIVE)
        .order_by(MarketListing.created_at.desc())
        .limit(limit)
        .offset(offset)
    )

    if (rarities and len(rarities) > 0) or (item_types and len(item_types) > 0):
        stmt = stmt.join(MarketListing.user_item).join(UserItem.item)
        if rarities:
            stmt = stmt.where(Item.rarity.in_(list(rarities)))
        if item_types:
            stmt = stmt.where(Item.type.in_(list(item_types)))

    result = await session.execute(stmt)
    return result.scalars().all()
