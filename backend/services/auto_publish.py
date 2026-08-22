"""Publish approved releases when release_date <= now (UTC date)."""

from __future__ import annotations

import logging
from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from db.managers.moderation_logs_manager import ModerationLogManager
from db.managers.notification_manager import NotificationManager
from db.models.moderation_logs import HistoryKind
from db.models.notifications import NotifType
from db.models.releases import Release, ReleaseStatus

logger = logging.getLogger(__name__)


async def publish_due_releases(session: AsyncSession) -> int:
    now = datetime.now(timezone.utc)
    stmt = select(Release).where(
        Release.status == ReleaseStatus.APPROVED,
        Release.release_date <= now,
    )
    releases = list((await session.scalars(stmt)).all())
    if not releases:
        return 0

    log_mgr = ModerationLogManager(session)
    notif = NotificationManager(session)
    count = 0
    for rel in releases:
        rel.status = ReleaseStatus.PUBLISHED
        rel.live_revision = False
        await log_mgr.create_log(
            release_id=rel.id,
            moderator_id=None,
            action="published",
            comment="auto-publish on release_date",
            kind=HistoryKind.SYSTEM,
            commit=False,
        )
        await notif.create(
            user_id=rel.owner_id,
            title="Release published",
            body=f"«{rel.title}» is live",
            type=NotifType.SYSTEM,
            meta={"release_id": str(rel.id)},
            commit=False,
        )
        count += 1
        logger.info("auto-published release id=%s title=%s", rel.id, rel.title)

    await session.commit()
    return count
