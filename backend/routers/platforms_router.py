"""Platform connect: OAuth popup flow + link artist id + sync public stats."""

from __future__ import annotations

import secrets
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, ConfigDict

from auth import Current_User_Dep, DB_Dep, get_current_user
from db.managers.platform_connection_manager import PlatformConnectionManager
from db.models.platform_connections import ConnectionStatus, PlatformKind
from services.platforms import apple, spotify, vk, yandex

router = APIRouter(prefix="/platforms", tags=["Platforms"])


def _oauth_done(platform: str) -> HTMLResponse:
    html = f"""<!doctype html><html><body style="font-family:sans-serif;padding:2rem">
    <h2>Connected: {platform}</h2>
    <p>You can close this window.</p>
    <script>
    try {{ window.opener && window.opener.postMessage({{type:'platform_connected', platform:'{platform}'}}, '*'); }} catch (e) {{}}
    setTimeout(function(){{ window.close(); }}, 800);
    </script>
    </body></html>"""
    return HTMLResponse(html)


_oauth_state: dict[str, int] = {}


async def get_pcm(db: DB_Dep) -> PlatformConnectionManager:
    return PlatformConnectionManager(db)


PCM = Annotated[PlatformConnectionManager, Depends(get_pcm)]


class ConnectionOut(BaseModel):
    platform: PlatformKind
    status: ConnectionStatus
    external_artist_id: str | None = None
    display_name: str | None = None
    last_synced_at: str | None = None
    meta: dict | None = None

    model_config = ConfigDict(from_attributes=True)


class LinkArtistBody(BaseModel):
    external_artist_id: str


class AuthStartOut(BaseModel):
    authorize_url: str
    state: str


@router.get("/", response_model=list[ConnectionOut], dependencies=[Depends(get_current_user)])
async def list_connections(pcm: PCM, user: Current_User_Dep):
    rows = await pcm.list_for_user(user.id)
    return [
        ConnectionOut(
            platform=r.platform,
            status=r.status,
            external_artist_id=r.external_artist_id,
            display_name=r.display_name,
            last_synced_at=r.last_synced_at.isoformat() if r.last_synced_at else None,
            meta=r.meta,
        )
        for r in rows
    ]


@router.get("/spotify/start", response_model=AuthStartOut)
async def spotify_start(user: Current_User_Dep):
    state = secrets.token_urlsafe(24)
    _oauth_state[state] = user.id
    return AuthStartOut(authorize_url=spotify.auth_url(state), state=state)


@router.get("/spotify/callback")
async def spotify_callback(
    db: DB_Dep,
    code: str = Query(...),
    state: str = Query(...),
):
    user_id = _oauth_state.pop(state, None)
    if not user_id:
        raise HTTPException(400, "Invalid state")
    tokens = await spotify.exchange_code(code)
    me = await spotify.get_me(tokens["access_token"])
    mgr = PlatformConnectionManager(db)
    await mgr.set_tokens(
        user_id,
        PlatformKind.SPOTIFY,
        access_token=tokens["access_token"],
        refresh_token=tokens.get("refresh_token"),
        expires_at=spotify.token_expiry(tokens),
        external_user_id=me.get("id"),
        display_name=me.get("display_name"),
        scopes=spotify.SCOPES,
    )
    return _oauth_done("spotify")


@router.post("/spotify/link-artist", response_model=ConnectionOut)
async def spotify_link_artist(
    body: LinkArtistBody, pcm: PCM, user: Current_User_Dep
):
    row = await pcm.set_artist_id(user.id, PlatformKind.SPOTIFY, body.external_artist_id)
    try:
        data = await spotify.get_artist_public(body.external_artist_id)
        meta = {
            "followers": data.get("followers", {}).get("total"),
            "popularity": data.get("popularity"),
            "name": data.get("name"),
        }
        await pcm.mark_synced(row, meta)
        row = await pcm.get(user.id, PlatformKind.SPOTIFY)
    except Exception as e:
        await pcm.mark_synced(row, {"error": str(e)})
    return ConnectionOut(
        platform=row.platform,
        status=row.status,
        external_artist_id=row.external_artist_id,
        display_name=row.display_name,
        last_synced_at=row.last_synced_at.isoformat() if row.last_synced_at else None,
        meta=row.meta,
    )


@router.post("/spotify/sync")
async def spotify_sync(pcm: PCM, user: Current_User_Dep, db: DB_Dep):
    row = await pcm.get(user.id, PlatformKind.SPOTIFY)
    if not row or not row.external_artist_id:
        raise HTTPException(400, "Link Spotify artist id first")
    data = await spotify.get_artist_public(row.external_artist_id)
    followers = data.get("followers", {}).get("total") or 0
    await pcm.mark_synced(
        row,
        {
            "followers": followers,
            "popularity": data.get("popularity"),
            "name": data.get("name"),
        },
    )
    return {"ok": True, "followers": followers}


@router.get("/yandex/start", response_model=AuthStartOut)
async def yandex_start(user: Current_User_Dep):
    state = secrets.token_urlsafe(24)
    _oauth_state[state] = user.id
    return AuthStartOut(authorize_url=yandex.auth_url(state), state=state)


@router.get("/yandex/callback")
async def yandex_callback(
    db: DB_Dep,
    code: str = Query(...),
    state: str = Query(...),
):
    user_id = _oauth_state.pop(state, None)
    if not user_id:
        raise HTTPException(400, "Invalid state")
    tokens = await yandex.exchange_code(code)
    info = await yandex.get_user_info(tokens["access_token"])
    mgr = PlatformConnectionManager(db)
    await mgr.set_tokens(
        user_id,
        PlatformKind.YANDEX,
        access_token=tokens["access_token"],
        refresh_token=tokens.get("refresh_token"),
        expires_at=None,
        external_user_id=str(info.get("id")),
        display_name=info.get("display_name") or info.get("real_name"),
        scopes=yandex.SCOPES,
    )
    return _oauth_done("yandex")


@router.post("/yandex/link-artist", response_model=ConnectionOut)
async def yandex_link_artist(body: LinkArtistBody, pcm: PCM, user: Current_User_Dep):
    row = await pcm.set_artist_id(user.id, PlatformKind.YANDEX, body.external_artist_id)
    return ConnectionOut(
        platform=row.platform,
        status=row.status,
        external_artist_id=row.external_artist_id,
        display_name=row.display_name,
        last_synced_at=None,
        meta=row.meta,
    )


@router.get("/vk/start", response_model=AuthStartOut)
async def vk_start(user: Current_User_Dep):
    state = secrets.token_urlsafe(24)
    _oauth_state[state] = user.id
    return AuthStartOut(authorize_url=vk.auth_url(state), state=state)


@router.get("/vk/callback")
async def vk_callback(
    db: DB_Dep,
    code: str = Query(...),
    state: str = Query(...),
):
    user_id = _oauth_state.pop(state, None)
    if not user_id:
        raise HTTPException(400, "Invalid state")
    tokens = await vk.exchange_code(code)
    if "error" in tokens:
        raise HTTPException(400, tokens.get("error_description", "VK error"))
    mgr = PlatformConnectionManager(db)
    await mgr.set_tokens(
        user_id,
        PlatformKind.VK,
        access_token=tokens["access_token"],
        refresh_token=None,
        expires_at=None,
        external_user_id=str(tokens.get("user_id")),
        display_name=None,
        scopes=vk.SCOPE,
    )
    return _oauth_done("vk")


@router.post("/vk/link-artist", response_model=ConnectionOut)
async def vk_link_artist(body: LinkArtistBody, pcm: PCM, user: Current_User_Dep):
    row = await pcm.set_artist_id(user.id, PlatformKind.VK, body.external_artist_id)
    return ConnectionOut(
        platform=row.platform,
        status=row.status,
        external_artist_id=row.external_artist_id,
        display_name=row.display_name,
        last_synced_at=None,
        meta=row.meta,
    )


@router.post("/apple/link-artist", response_model=ConnectionOut)
async def apple_link_artist(body: LinkArtistBody, pcm: PCM, user: Current_User_Dep):
    row = await pcm.upsert(
        user.id,
        PlatformKind.APPLE,
        status=ConnectionStatus.CONNECTED,
        external_artist_id=body.external_artist_id,
    )
    data = await apple.get_catalog_artist(body.external_artist_id)
    if data:
        attrs = (data.get("data") or [{}])[0].get("attributes") or {}
        await pcm.mark_synced(row, {"name": attrs.get("name")})
        row = await pcm.get(user.id, PlatformKind.APPLE)
    return ConnectionOut(
        platform=row.platform,
        status=row.status,
        external_artist_id=row.external_artist_id,
        display_name=row.display_name,
        last_synced_at=row.last_synced_at.isoformat() if row.last_synced_at else None,
        meta=row.meta,
    )


@router.delete("/{platform}")
async def disconnect(platform: PlatformKind, pcm: PCM, user: Current_User_Dep):
    await pcm.disconnect(user.id, platform)
    return {"ok": True}
