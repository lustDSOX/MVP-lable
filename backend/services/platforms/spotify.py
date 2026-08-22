"""Spotify OAuth + public artist metrics."""

from __future__ import annotations

import os
from datetime import datetime, timedelta, timezone
from urllib.parse import urlencode

import httpx

SPOTIFY_AUTH = "https://accounts.spotify.com"
SPOTIFY_API = "https://api.spotify.com/v1"

CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID", "")
CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET", "")
REDIRECT_URI = os.getenv(
    "SPOTIFY_REDIRECT_URI", "http://localhost:8000/platforms/spotify/callback"
)
SCOPES = "user-read-email user-read-private"


def auth_url(state: str) -> str:
    q = urlencode(
        {
            "client_id": CLIENT_ID,
            "response_type": "code",
            "redirect_uri": REDIRECT_URI,
            "scope": SCOPES,
            "state": state,
            "show_dialog": "true",
        }
    )
    return f"{SPOTIFY_AUTH}/authorize?{q}"


async def exchange_code(code: str) -> dict:
    async with httpx.AsyncClient() as client:
        r = await client.post(
            f"{SPOTIFY_AUTH}/api/token",
            data={
                "grant_type": "authorization_code",
                "code": code,
                "redirect_uri": REDIRECT_URI,
            },
            auth=(CLIENT_ID, CLIENT_SECRET),
        )
        r.raise_for_status()
        return r.json()


async def refresh_access_token(refresh_token: str) -> dict:
    async with httpx.AsyncClient() as client:
        r = await client.post(
            f"{SPOTIFY_AUTH}/api/token",
            data={
                "grant_type": "refresh_token",
                "refresh_token": refresh_token,
            },
            auth=(CLIENT_ID, CLIENT_SECRET),
        )
        r.raise_for_status()
        return r.json()


async def get_me(access_token: str) -> dict:
    async with httpx.AsyncClient() as client:
        r = await client.get(
            f"{SPOTIFY_API}/me",
            headers={"Authorization": f"Bearer {access_token}"},
        )
        r.raise_for_status()
        return r.json()


async def client_credentials_token() -> str:
    async with httpx.AsyncClient() as client:
        r = await client.post(
            f"{SPOTIFY_AUTH}/api/token",
            data={"grant_type": "client_credentials"},
            auth=(CLIENT_ID, CLIENT_SECRET),
        )
        r.raise_for_status()
        return r.json()["access_token"]


async def get_artist_public(artist_id: str) -> dict:
    token = await client_credentials_token()
    async with httpx.AsyncClient() as client:
        r = await client.get(
            f"{SPOTIFY_API}/artists/{artist_id}",
            headers={"Authorization": f"Bearer {token}"},
        )
        r.raise_for_status()
        return r.json()


def token_expiry(data: dict) -> datetime:
    return datetime.now(timezone.utc) + timedelta(seconds=int(data.get("expires_in", 3600)))
