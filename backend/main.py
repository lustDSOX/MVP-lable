import logging
import os
from contextlib import asynccontextmanager
import asyncio
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import uvicorn
from dotenv import load_dotenv

from routers.users_router import router as user_public
from routers.users_router import protect_router as user_protect
from routers.users_router import admin_router as user_admin
from routers.releases_router import router as release_public
from routers.releases_router import protect_router as release_protect
from routers.tracks_router import router as tracks_router
from routers.moderation_router import router as moderation_router
from routers.links_router import router as links_router
from routers.contracts_router import router as contracts_router
from routers.cms_router import public_router as cms_public
from routers.cms_router import staff_router as cms_staff
from routers.chat_router import router as chat_router
from routers.notifications_router import router as notifications_router
from routers.files_router import router as files_router
from routers.royalties_router import router as royalties_router
from routers.ws_chat import router as ws_chat_router
from routers.platforms_router import router as platforms_router
from routers.scheduler_router import router as scheduler_router
from routers.stats_router import router as stats_router
from services.scheduler_loop import run_auto_publish_loop

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s[%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)

UPLOAD_DIR = Path(os.getenv("UPLOAD_DIR", "/tmp/label_uploads"))
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Запуск Label Service API...")
    stop = asyncio.Event()
    task = asyncio.create_task(run_auto_publish_loop(stop))
    yield
    stop.set()
    try:
        await asyncio.wait_for(task, timeout=5)
    except Exception:
        task.cancel()
    logger.info("Остановка Label Service API...")


app = FastAPI(
    title="Label Management API",
    description="MVP сервиса для музыкального лейбла",
    version="0.4.1",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
)

_cors = os.getenv(
    "CORS_ORIGINS",
    "http://localhost:5173,http://127.0.0.1:5173,https://lustdsox.github.io",
)
allow_origins = [o.strip() for o in _cors.split(",") if o.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allow_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if os.getenv("STORAGE_BACKEND", "local").lower() == "local":
    app.mount("/uploads", StaticFiles(directory=str(UPLOAD_DIR)), name="uploads")

app.include_router(user_public)
app.include_router(user_protect)
app.include_router(user_admin)
app.include_router(release_public)
app.include_router(release_protect)
app.include_router(tracks_router)
app.include_router(moderation_router)
app.include_router(links_router)
app.include_router(contracts_router)
app.include_router(cms_public)
app.include_router(cms_staff)
app.include_router(chat_router)
app.include_router(notifications_router)
app.include_router(files_router)
app.include_router(royalties_router)
app.include_router(ws_chat_router)
app.include_router(platforms_router)
app.include_router(scheduler_router)
app.include_router(stats_router)


@app.get("/health", tags=["System"])
async def health():
    return {
        "status": "OK",
        "service": "Label Management API MVP",
        "version": "0.4.1",
        "storage": os.getenv("STORAGE_BACKEND", "local"),
    }


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True, log_level="info")
