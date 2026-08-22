"""Optional in-process loop for auto-publish (no external cron needed)."""

from __future__ import annotations

import asyncio
import logging
import os

from db.database import AsyncSessionLocal
from services.auto_publish import publish_due_releases

logger = logging.getLogger(__name__)

INTERVAL_SEC = int(os.getenv("AUTO_PUBLISH_INTERVAL_SEC", "900"))
ENABLED = os.getenv("AUTO_PUBLISH_LOOP", "1") not in ("0", "false", "False")


async def run_auto_publish_loop(stop: asyncio.Event) -> None:
    if not ENABLED:
        logger.info("auto-publish loop disabled")
        return
    logger.info("auto-publish loop every %ss", INTERVAL_SEC)
    while not stop.is_set():
        try:
            async with AsyncSessionLocal() as session:
                n = await publish_due_releases(session)
                if n:
                    logger.info("auto-published %s release(s)", n)
        except Exception:
            logger.exception("auto-publish tick failed")
        try:
            await asyncio.wait_for(stop.wait(), timeout=INTERVAL_SEC)
        except asyncio.TimeoutError:
            pass
