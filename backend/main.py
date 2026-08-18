import logging
import os
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from dotenv import load_dotenv

from routers.users_router import router as user_public
from routers.users_router import protect_router as user_protect
from routers.users_router import admin_router as user_admin
from routers.releases_router import router as release_public
from routers.releases_router import protect_router as release_protect

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s[%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Запуск Label Service API...")
    yield
    logger.info("Остановка Label Service API...")


app = FastAPI(
    title="Label Management API",
    description="MVP сервиса для музыкального лейбла",
    version="0.0.2",
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

app.include_router(user_public)
app.include_router(user_protect)
app.include_router(user_admin)
app.include_router(release_public)
app.include_router(release_protect)


@app.get("/health", tags=["System"])
async def health():
    return {"status": "OK", "service": "Label Management API MVP", "version": "0.0.2"}


if __name__ == "__main__":
    logger.info("Инициализация Uvicorn сервера...")
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info",
    )
