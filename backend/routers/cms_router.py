from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, ConfigDict

from auth import AdminDep, DB_Dep, ModeratorDep, get_current_user
from db.managers.cms_manager import CmsManager
from db.models.cms import CmsStatus


# ── schemas ──────────────────────────────────────────────
class NewsBase(BaseModel):
    title: str
    excerpt: str | None = None
    body: str
    date: str | None = None
    status: CmsStatus = CmsStatus.DRAFT


class NewsUpdate(BaseModel):
    title: str | None = None
    excerpt: str | None = None
    body: str | None = None
    date: str | None = None
    status: CmsStatus | None = None


class NewsResponse(NewsBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


class EventBase(BaseModel):
    title: str
    venue: str | None = None
    city: str | None = None
    date: str | None = None
    time: str | None = None
    description: str | None = None
    ticket_url: str | None = None
    price: str | None = None
    capacity: str | None = None
    age_limit: str | None = None
    status: CmsStatus = CmsStatus.DRAFT


class EventUpdate(BaseModel):
    title: str | None = None
    venue: str | None = None
    city: str | None = None
    date: str | None = None
    time: str | None = None
    description: str | None = None
    ticket_url: str | None = None
    price: str | None = None
    capacity: str | None = None
    age_limit: str | None = None
    status: CmsStatus | None = None


class EventResponse(EventBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


class GuideBase(BaseModel):
    title: str
    excerpt: str | None = None
    body: str
    category: str = "general"
    status: CmsStatus = CmsStatus.DRAFT


class GuideUpdate(BaseModel):
    title: str | None = None
    excerpt: str | None = None
    body: str | None = None
    category: str | None = None
    status: CmsStatus | None = None


class GuideResponse(GuideBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


async def get_cms_manager(db: DB_Dep) -> CmsManager:
    return CmsManager(db)


Mgr = Annotated[CmsManager, Depends(get_cms_manager)]

# public read
public_router = APIRouter(prefix="/cms", tags=["CMS"])

# staff write
staff_router = APIRouter(
    prefix="/cms",
    tags=["CMS Staff"],
    dependencies=[Depends(get_current_user)],
)


# ── public ───────────────────────────────────────────────
@public_router.get("/news", response_model=list[NewsResponse])
async def list_published_news(mgr: Mgr, limit: int = 50, offset: int = 0):
    return await mgr.list_news(status=CmsStatus.PUBLISHED, limit=limit, offset=offset)


@public_router.get("/news/{item_id}", response_model=NewsResponse)
async def get_news(item_id: int, mgr: Mgr):
    item = await mgr.get_news(item_id)
    if not item or item.status != CmsStatus.PUBLISHED:
        raise HTTPException(404, "Not found")
    return item


@public_router.get("/events", response_model=list[EventResponse])
async def list_published_events(mgr: Mgr, limit: int = 50, offset: int = 0):
    return await mgr.list_events(status=CmsStatus.PUBLISHED, limit=limit, offset=offset)


@public_router.get("/events/{item_id}", response_model=EventResponse)
async def get_event(item_id: int, mgr: Mgr):
    item = await mgr.get_event(item_id)
    if not item or item.status != CmsStatus.PUBLISHED:
        raise HTTPException(404, "Not found")
    return item


@public_router.get("/guides", response_model=list[GuideResponse])
async def list_published_guides(mgr: Mgr, limit: int = 50, offset: int = 0):
    return await mgr.list_guides(status=CmsStatus.PUBLISHED, limit=limit, offset=offset)


@public_router.get("/guides/{item_id}", response_model=GuideResponse)
async def get_guide(item_id: int, mgr: Mgr):
    item = await mgr.get_guide(item_id)
    if not item or item.status != CmsStatus.PUBLISHED:
        raise HTTPException(404, "Not found")
    return item


# ── staff ────────────────────────────────────────────────
@staff_router.get("/news/all", response_model=list[NewsResponse])
async def list_all_news(mgr: Mgr, _: ModeratorDep, limit: int = 100, offset: int = 0):
    return await mgr.list_news(limit=limit, offset=offset)


@staff_router.post("/news", response_model=NewsResponse, status_code=201)
async def create_news(data: NewsBase, mgr: Mgr, _: ModeratorDep):
    return await mgr.create_news(**data.model_dump())


@staff_router.patch("/news/{item_id}", response_model=NewsResponse)
async def update_news(item_id: int, data: NewsUpdate, mgr: Mgr, _: ModeratorDep):
    item = await mgr.get_news(item_id)
    if not item:
        raise HTTPException(404, "Not found")
    return await mgr.update_news(item, **data.model_dump(exclude_unset=True))


@staff_router.delete("/news/{item_id}", status_code=204)
async def delete_news(item_id: int, mgr: Mgr, _: AdminDep):
    item = await mgr.get_news(item_id)
    if not item:
        raise HTTPException(404, "Not found")
    await mgr.delete_news(item)


@staff_router.get("/events/all", response_model=list[EventResponse])
async def list_all_events(mgr: Mgr, _: ModeratorDep, limit: int = 100, offset: int = 0):
    return await mgr.list_events(limit=limit, offset=offset)


@staff_router.post("/events", response_model=EventResponse, status_code=201)
async def create_event(data: EventBase, mgr: Mgr, _: ModeratorDep):
    return await mgr.create_event(**data.model_dump())


@staff_router.patch("/events/{item_id}", response_model=EventResponse)
async def update_event(item_id: int, data: EventUpdate, mgr: Mgr, _: ModeratorDep):
    item = await mgr.get_event(item_id)
    if not item:
        raise HTTPException(404, "Not found")
    return await mgr.update_event(item, **data.model_dump(exclude_unset=True))


@staff_router.delete("/events/{item_id}", status_code=204)
async def delete_event(item_id: int, mgr: Mgr, _: AdminDep):
    item = await mgr.get_event(item_id)
    if not item:
        raise HTTPException(404, "Not found")
    await mgr.delete_event(item)


@staff_router.get("/guides/all", response_model=list[GuideResponse])
async def list_all_guides(mgr: Mgr, _: ModeratorDep, limit: int = 100, offset: int = 0):
    return await mgr.list_guides(limit=limit, offset=offset)


@staff_router.post("/guides", response_model=GuideResponse, status_code=201)
async def create_guide(data: GuideBase, mgr: Mgr, _: ModeratorDep):
    return await mgr.create_guide(**data.model_dump())


@staff_router.patch("/guides/{item_id}", response_model=GuideResponse)
async def update_guide(item_id: int, data: GuideUpdate, mgr: Mgr, _: ModeratorDep):
    item = await mgr.get_guide(item_id)
    if not item:
        raise HTTPException(404, "Not found")
    return await mgr.update_guide(item, **data.model_dump(exclude_unset=True))


@staff_router.delete("/guides/{item_id}", status_code=204)
async def delete_guide(item_id: int, mgr: Mgr, _: AdminDep):
    item = await mgr.get_guide(item_id)
    if not item:
        raise HTTPException(404, "Not found")
    await mgr.delete_guide(item)
