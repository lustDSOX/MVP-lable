"""Cron-friendly endpoints for background jobs."""

from fastapi import APIRouter, Header, HTTPException
from pydantic import BaseModel

from auth import DB_Dep, AdminDep
from services.auto_publish import publish_due_releases
import os

router = APIRouter(prefix="/jobs", tags=["Jobs"])

CRON_SECRET = os.getenv("CRON_SECRET", "")


class JobResult(BaseModel):
    ok: bool
    published: int = 0


def _check_cron(x_cron_secret: str | None):
    if CRON_SECRET and x_cron_secret != CRON_SECRET:
        raise HTTPException(401, "Invalid cron secret")


@router.post("/auto-publish", response_model=JobResult)
async def job_auto_publish(
    db: DB_Dep,
    x_cron_secret: str | None = Header(default=None),
):
    _check_cron(x_cron_secret)
    n = await publish_due_releases(db)
    return JobResult(ok=True, published=n)


@router.post("/auto-publish/manual", response_model=JobResult)
async def job_auto_publish_manual(db: DB_Dep, _: AdminDep):
    n = await publish_due_releases(db)
    return JobResult(ok=True, published=n)
