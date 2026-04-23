import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

# Импорт роутеров
from routers.users_router import router as user_public
from routers.users_router import protect_router as user_protect
from routers.releases_router import router as release_public
from routers.releases_router import protect_router as release_protect


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
    version="0.0.1",
    lifespan=lifespan,
    docs_url="/docs",  
    redoc_url="/redoc" 
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],       # Разрешенные домены (для продакшена заменить на реальный домен)
    allow_credentials=True,      # Разрешить передачу куки/токенов
    allow_methods=["*"],         # Разрешить все методы (GET, POST, PUT, PATCH, DELETE)
    allow_headers=["*"],         # Разрешить все заголовки
)


# API Users
app.include_router(user_public)
app.include_router(user_protect)
# API Releases
app.include_router(release_public)
app.include_router(release_protect)


@app.get("/health", tags=["System"])
async def health():
    return {
        "status": "OK",
        "service": "Label Management API MVP"
    }



if __name__ == "__main__":
    logger.info("Инициализация Uvicorn сервера...")
    uvicorn.run(
        "main:app", 
        host="0.0.0.0", 
        port=8000, 
        reload=True,
        log_level="info"
    )