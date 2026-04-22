from fastapi import FastAPI
from routers.users_router import router as user_public
from routers.users_router import protect_router as user_protect
from routers.releases_router import router as release_public
from routers.releases_router import protect_router as release_protect


app = FastAPI()

app.include_router(user_protect)
app.include_router(user_public)
app.include_router(release_protect)
app.include_router(release_public)

@app.get("/health")
async def health():
    return {"status": "OK"}