from io import BytesIO
from pathlib import Path

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from pydantic import BaseModel

from auth import Current_User_Dep, get_current_user
from services.storage import get_storage, make_key

ALLOWED_AUDIO = {".wav", ".mp3", ".flac", ".aiff"}
ALLOWED_IMAGE = {".jpg", ".jpeg", ".png", ".webp"}
ALLOWED_DOC = {".pdf"}
MAX_AUDIO_MB = 200
MAX_IMAGE_MB = 20
MAX_DOC_MB = 10

router = APIRouter(
    prefix="/files",
    tags=["Files"],
    dependencies=[Depends(get_current_user)],
)


class UploadResponse(BaseModel):
    url: str
    filename: str
    size: int
    content_type: str | None = None
    key: str


def _upload(file: UploadFile, subdir: str, allowed: set[str], max_mb: int) -> UploadResponse:
    if not file.filename:
        raise HTTPException(400, "No filename")
    ext = Path(file.filename).suffix.lower()
    if ext not in allowed:
        raise HTTPException(400, f"Allowed: {', '.join(sorted(allowed))}")

    raw = file.file.read()
    size = len(raw)
    if size > max_mb * 1024 * 1024:
        raise HTTPException(400, f"Max {max_mb} MB")

    key = make_key(subdir, file.filename)
    storage = get_storage()
    url = storage.save(BytesIO(raw), key, content_type=file.content_type)
    return UploadResponse(
        url=url,
        filename=file.filename,
        size=size,
        content_type=file.content_type,
        key=key,
    )


@router.post("/audio", response_model=UploadResponse)
async def upload_audio(current_user: Current_User_Dep, file: UploadFile = File(...)):
    return _upload(file, "audio", ALLOWED_AUDIO, MAX_AUDIO_MB)


@router.post("/cover", response_model=UploadResponse)
async def upload_cover(current_user: Current_User_Dep, file: UploadFile = File(...)):
    return _upload(file, "covers", ALLOWED_IMAGE, MAX_IMAGE_MB)


@router.post("/document", response_model=UploadResponse)
async def upload_document(current_user: Current_User_Dep, file: UploadFile = File(...)):
    return _upload(file, "docs", ALLOWED_DOC, MAX_DOC_MB)
