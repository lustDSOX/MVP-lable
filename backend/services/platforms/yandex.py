"""Yandex Music OAuth."""

from __future__ import annotations

import os
from urllib.parse import urlencode

YANDEX_OAUTH = "https://oauth.yandex.ru"
CLIENT_ID = os.getenv("YANDEX_CLIENT_ID", "")
CLIENT_SECRET = os.getenv("YANDEX_CLIENT_SECRET", "")
REDIRECT_URI = os.getenv(
    "YANDEX_REDIRECT_URI", "http://localhost:8000/platforms/yandex/callback"
)
SCOPES = os.getenv("YANDEX_SCOPES", "login:info login:email")


def auth_url(state: str) -> str:
    q = urlencode(
        {
            "response_type": "code",
            "client_id": CLIENT_ID,
            "redirect_uri": REDIRECT_URI,
            "state": state,
            "force_confirm": "yes",
            "scope": SCOPES,
        }
    )
    return f"{YANDEX_OAUTH}/authorize?{q}"


async def exchange_code(code: str) -> dict:
    import httpx

    async with httpx.AsyncClient() as client:
        r = await client.post(
            f"{YANDEX_OAUTH}/token",
            data={
                "grant_type": "authorization_code",
                "code": code,
                "client_id": CLIENT_ID,
                "client_secret": CLIENT_SECRET,
            },
        )
        r.raise_for_status()
        return r.json()


async def get_user_info(access_token: str) -> dict:
    import httpx

    async with httpx.AsyncClient() as client:
        r = await client.get(
            "https://login.yandex.ru/info",
            headers={"Authorization": f"OAuth {access_token}"},
            params={"format": "json"},
        )
        r.raise_for_status()
        return r.json()
