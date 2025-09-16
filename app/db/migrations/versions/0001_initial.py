"""Початкова схема БД"""

from __future__ import annotations

from alembic import op
import sqlalchemy as sa

revision = "0001_initial"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    item_rarity = sa.Enum("common", "rare", "epic", "legendary", "mythic", name="item_rarity")
    item_type = sa.Enum("card", "gif", "artifact", name="item_type")
    item_color = sa.Enum("standard", "silver", "gold", "rainbow", name="item_color")
    listing_status = sa.Enum("active", "sold", "cancelled", name="listing_status")
    transaction_kind = sa.Enum(
        "bonus",
        "case_purchase",
        "case_reward",
        "market_sale",
        "market_purchase",
        "bot_buyout",
        "referral",
        name="transaction_kind",
    )

    item_rarity.create(op.get_bind(), checkfirst=True)
    item_type.create(op.get_bind(), checkfirst=True)
    item_color.create(op.get_bind(), checkfirst=True)
    listing_status.create(op.get_bind(), checkfirst=True)
    transaction_kind.create(op.get_bind(), checkfirst=True)

    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("tg_id", sa.BigInteger(), nullable=False),
        sa.Column("username", sa.String(length=64), nullable=True),
        sa.Column("vusd", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("cp", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("mythic_count", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("ref_code", sa.String(length=16), nullable=False),
        sa.Column("referrer_id", sa.Integer(), nullable=True),
        sa.Column("daily_claimed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("pity_counter", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.ForeignKeyConstraint(["referrer_id"], ["users.id"], ondelete="SET NULL"),
        sa.UniqueConstraint("ref_code"),
        sa.UniqueConstraint("tg_id"),
    )
    op.create_index("ix_users_tg_id", "users", ["tg_id"], unique=True)

    op.create_table(
        "items",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("key", sa.String(length=64), nullable=False),
        sa.Column("name", sa.String(length=128), nullable=False),
        sa.Column("rarity", item_rarity, nullable=False),
        sa.Column("type", item_type, nullable=False),
        sa.Column("color", item_color, nullable=False),
        sa.Column("serial_no", sa.Integer(), nullable=True),
        sa.Column("cp_value", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("base_buy_price", sa.Integer(), nullable=False),
        sa.Column("image_url", sa.String(length=256), nullable=True),
        sa.UniqueConstraint("key"),
    )
    op.create_index("ix_items_key", "items", ["key"], unique=True)

    op.create_table(
        "cases",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("code", sa.String(length=32), nullable=False),
        sa.Column("name", sa.String(length=128), nullable=False),
        sa.Column("price", sa.Integer(), nullable=False),
        sa.Column("pity_step", sa.Numeric(scale=2), nullable=False, server_default="1"),
        sa.Column("pity_threshold", sa.Integer(), nullable=False, server_default="10"),
        sa.Column("cp_requirement", sa.Integer(), nullable=True),
        sa.UniqueConstraint("code"),
    )
    op.create_index("ix_cases_code", "cases", ["code"], unique=True)

    op.create_table(
        "user_items",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("item_id", sa.Integer(), nullable=False),
        sa.Column("serial_no", sa.String(), nullable=False, server_default="0000"),
        sa.Column("acquired_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("locked_for_cp", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["item_id"], ["items.id"], ondelete="CASCADE"),
    )
    op.create_index("ix_user_items_user_id", "user_items", ["user_id"], unique=False)

    op.create_table(
        "case_items",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("case_id", sa.Integer(), nullable=False),
        sa.Column("item_id", sa.Integer(), nullable=False),
        sa.Column("weight", sa.Float(), nullable=False, server_default="1.0"),
        sa.ForeignKeyConstraint(["case_id"], ["cases.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["item_id"], ["items.id"], ondelete="CASCADE"),
    )

    op.create_table(
        "market_listings",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("seller_id", sa.Integer(), nullable=False),
        sa.Column("buyer_id", sa.Integer(), nullable=True),
        sa.Column("user_item_id", sa.Integer(), nullable=False),
        sa.Column("price", sa.Integer(), nullable=False),
        sa.Column("status", listing_status, nullable=False, server_default="active"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("closed_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["seller_id"], ["users.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["buyer_id"], ["users.id"], ondelete="SET NULL"),
        sa.ForeignKeyConstraint(["user_item_id"], ["user_items.id"], ondelete="CASCADE"),
        sa.UniqueConstraint("user_item_id"),
    )

    op.create_table(
        "transactions",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("amount", sa.Integer(), nullable=False),
        sa.Column("kind", transaction_kind, nullable=False),
        sa.Column("meta", sa.JSON(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
    )
    op.create_index("ix_transactions_user_id", "transactions", ["user_id"], unique=False)


def downgrade() -> None:
    op.drop_index("ix_transactions_user_id", table_name="transactions")
    op.drop_table("transactions")
    op.drop_table("market_listings")
    op.drop_table("case_items")
    op.drop_index("ix_user_items_user_id", table_name="user_items")
    op.drop_table("user_items")
    op.drop_index("ix_cases_code", table_name="cases")
    op.drop_table("cases")
    op.drop_index("ix_items_key", table_name="items")
    op.drop_table("items")
    op.drop_index("ix_users_tg_id", table_name="users")
    op.drop_table("users")

    sa.Enum(name="transaction_kind").drop(op.get_bind(), checkfirst=True)
    sa.Enum(name="listing_status").drop(op.get_bind(), checkfirst=True)
    sa.Enum(name="item_color").drop(op.get_bind(), checkfirst=True)
    sa.Enum(name="item_type").drop(op.get_bind(), checkfirst=True)
    sa.Enum(name="item_rarity").drop(op.get_bind(), checkfirst=True)
