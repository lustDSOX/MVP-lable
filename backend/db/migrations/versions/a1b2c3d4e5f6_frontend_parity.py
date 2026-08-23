"""Frontend parity: contracts, cms, chat, notifications, release fields, royalties, history kind

Revision ID: a1b2c3d4e5f6
Revises: b398182c07ac
Create Date: 2026-08-21

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision: str = "a1b2c3d4e5f6"
down_revision: Union[str, Sequence[str], None] = "b398182c07ac"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    releasetype = sa.Enum("single", "ep", "album", name="releasetype")
    releasetype.create(op.get_bind(), checkfirst=True)

    contractstatus = sa.Enum("unsigned", "signed", "void", "needs_resign", name="contractstatus")
    contractstatus.create(op.get_bind(), checkfirst=True)

    cmsstatus = sa.Enum("draft", "published", name="cmsstatus")
    cmsstatus.create(op.get_bind(), checkfirst=True)

    notiftype = sa.Enum(
        "release_pending",
        "moderation_decision",
        "change_request",
        "admin_message",
        "system",
        "chat_mention",
        name="notiftype",
    )
    notiftype.create(op.get_bind(), checkfirst=True)

    historykind = sa.Enum(
        "moderation", "artist_edit", "contract", "submit", "system", name="historykind"
    )
    historykind.create(op.get_bind(), checkfirst=True)

    op.execute("ALTER TYPE releasestatus ADD VALUE IF NOT EXISTS 'changes_requested'")

    op.add_column("users", sa.Column("phone", sa.String(), nullable=True))
    op.add_column("users", sa.Column("city", sa.String(), nullable=True))
    op.add_column("users", sa.Column("social_networks", sa.String(), nullable=True))
    op.add_column("users", sa.Column("full_name", sa.String(), nullable=True))

    op.add_column("releases", sa.Column("cover_note", sa.String(), nullable=True))
    op.add_column(
        "releases",
        sa.Column("type", releasetype, server_default="single", nullable=False),
    )
    op.add_column("releases", sa.Column("genre", sa.String(), nullable=True))
    op.add_column(
        "releases",
        sa.Column("genres", postgresql.ARRAY(sa.String()), nullable=True),
    )
    op.add_column("releases", sa.Column("reject_reason", sa.Text(), nullable=True))
    op.add_column("releases", sa.Column("change_request_note", sa.Text(), nullable=True))
    op.add_column(
        "releases",
        sa.Column("live_revision", sa.Boolean(), server_default="false", nullable=False),
    )
    op.add_column(
        "releases",
        sa.Column("updated_at", sa.DateTime(), server_default=sa.text("now()"), nullable=True),
    )

    op.add_column(
        "moderation_logs",
        sa.Column("kind", historykind, server_default="moderation", nullable=False),
    )

    op.create_table(
        "contracts",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column(
            "release_id",
            sa.Integer(),
            sa.ForeignKey("releases.id", ondelete="CASCADE"),
            nullable=False,
            unique=True,
        ),
        sa.Column("status", contractstatus, nullable=False, server_default="unsigned"),
        sa.Column("version", sa.String(), nullable=False, server_default="v0.3"),
        sa.Column("artist_full_name", sa.String(), nullable=True),
        sa.Column("file_url", sa.String(), nullable=True),
        sa.Column("signed_at", sa.DateTime(), nullable=True),
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("now()")),
        sa.Column("updated_at", sa.DateTime(), server_default=sa.text("now()")),
    )
    op.create_index("ix_contracts_id", "contracts", ["id"])

    op.create_table(
        "news",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("title", sa.String(), nullable=False),
        sa.Column("excerpt", sa.String(), nullable=True),
        sa.Column("body", sa.Text(), nullable=False),
        sa.Column("date", sa.String(), nullable=True),
        sa.Column("status", cmsstatus, nullable=False, server_default="draft"),
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("now()")),
        sa.Column("updated_at", sa.DateTime(), server_default=sa.text("now()")),
    )
    op.create_index("ix_news_id", "news", ["id"])

    op.create_table(
        "events",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("title", sa.String(), nullable=False),
        sa.Column("venue", sa.String(), nullable=True),
        sa.Column("city", sa.String(), nullable=True),
        sa.Column("date", sa.String(), nullable=True),
        sa.Column("time", sa.String(), nullable=True),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("ticket_url", sa.String(), nullable=True),
        sa.Column("price", sa.String(), nullable=True),
        sa.Column("capacity", sa.String(), nullable=True),
        sa.Column("age_limit", sa.String(), nullable=True),
        sa.Column("status", cmsstatus, nullable=False, server_default="draft"),
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("now()")),
        sa.Column("updated_at", sa.DateTime(), server_default=sa.text("now()")),
    )
    op.create_index("ix_events_id", "events", ["id"])

    op.create_table(
        "guides",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("title", sa.String(), nullable=False),
        sa.Column("excerpt", sa.String(), nullable=True),
        sa.Column("body", sa.Text(), nullable=False),
        sa.Column("category", sa.String(), nullable=False, server_default="general"),
        sa.Column("status", cmsstatus, nullable=False, server_default="draft"),
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("now()")),
        sa.Column("updated_at", sa.DateTime(), server_default=sa.text("now()")),
    )
    op.create_index("ix_guides_id", "guides", ["id"])

    op.create_table(
        "chat_messages",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column(
            "from_user_id",
            sa.Integer(),
            sa.ForeignKey("users.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column(
            "to_user_id",
            sa.Integer(),
            sa.ForeignKey("users.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("body", sa.Text(), nullable=False),
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("now()")),
    )
    op.create_index("ix_chat_messages_id", "chat_messages", ["id"])
    op.create_index("ix_chat_from_to", "chat_messages", ["from_user_id", "to_user_id"])

    op.create_table(
        "notifications",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column(
            "user_id",
            sa.Integer(),
            sa.ForeignKey("users.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("title", sa.String(), nullable=False),
        sa.Column("body", sa.Text(), nullable=False),
        sa.Column("type", notiftype, nullable=False, server_default="system"),
        sa.Column("read", sa.Boolean(), nullable=False, server_default="false"),
        sa.Column("meta", postgresql.JSONB(), nullable=True),
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("now()")),
    )
    op.create_index("ix_notifications_id", "notifications", ["id"])
    op.create_index("ix_notifications_user", "notifications", ["user_id"])

    op.create_table(
        "royalty_entries",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column(
            "release_id",
            sa.Integer(),
            sa.ForeignKey("releases.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("amount", sa.Float(), nullable=False, server_default="0"),
        sa.Column("currency", sa.String(), nullable=False, server_default="RUB"),
        sa.Column("period_start", sa.Date(), nullable=True),
        sa.Column("period_end", sa.Date(), nullable=True),
        sa.Column("note", sa.String(), nullable=True),
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("now()")),
    )
    op.create_index("ix_royalty_entries_id", "royalty_entries", ["id"])

    op.create_table(
        "platform_followers",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column(
            "release_id",
            sa.Integer(),
            sa.ForeignKey("releases.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("platform", sa.String(), nullable=False),
        sa.Column("followers", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("updated_at", sa.DateTime(), server_default=sa.text("now()")),
    )
    op.create_index("ix_platform_followers_id", "platform_followers", ["id"])

    platformkind = sa.Enum("spotify", "apple", "yandex", "vk", name="platformkind")
    platformkind.create(op.get_bind(), checkfirst=True)
    connectionstatus = sa.Enum(
        "pending", "connected", "expired", "revoked", "error", name="connectionstatus"
    )
    connectionstatus.create(op.get_bind(), checkfirst=True)

    op.create_table(
        "platform_connections",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("platform", platformkind, nullable=False),
        sa.Column("status", connectionstatus, nullable=False, server_default="pending"),
        sa.Column("external_artist_id", sa.String(), nullable=True),
        sa.Column("external_user_id", sa.String(), nullable=True),
        sa.Column("display_name", sa.String(), nullable=True),
        sa.Column("access_token", sa.Text(), nullable=True),
        sa.Column("refresh_token", sa.Text(), nullable=True),
        sa.Column("token_expires_at", sa.DateTime(), nullable=True),
        sa.Column("scopes", sa.String(), nullable=True),
        sa.Column("meta", postgresql.JSONB(), nullable=True),
        sa.Column("last_synced_at", sa.DateTime(), nullable=True),
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("now()")),
        sa.Column("updated_at", sa.DateTime(), server_default=sa.text("now()")),
    )
    op.create_index("ix_platform_connections_id", "platform_connections", ["id"])
    op.create_unique_constraint("uq_platform_user_platform", "platform_connections", ["user_id", "platform"])


def downgrade() -> None:
    op.drop_table("platform_connections")
    op.drop_table("platform_followers")
    op.drop_table("royalty_entries")
    op.drop_table("notifications")
    op.drop_table("chat_messages")
    op.drop_table("guides")
    op.drop_table("events")
    op.drop_table("news")
    op.drop_table("contracts")
    op.drop_column("moderation_logs", "kind")
    op.drop_column("releases", "updated_at")
    op.drop_column("releases", "live_revision")
    op.drop_column("releases", "change_request_note")
    op.drop_column("releases", "reject_reason")
    op.drop_column("releases", "genres")
    op.drop_column("releases", "genre")
    op.drop_column("releases", "type")
    op.drop_column("releases", "cover_note")
    op.drop_column("users", "full_name")
    op.drop_column("users", "social_networks")
    op.drop_column("users", "city")
    op.drop_column("users", "phone")
    sa.Enum(name="historykind").drop(op.get_bind(), checkfirst=True)
    sa.Enum(name="notiftype").drop(op.get_bind(), checkfirst=True)
    sa.Enum(name="cmsstatus").drop(op.get_bind(), checkfirst=True)
    sa.Enum(name="contractstatus").drop(op.get_bind(), checkfirst=True)
    sa.Enum(name="releasetype").drop(op.get_bind(), checkfirst=True)
