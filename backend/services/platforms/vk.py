"""VK OAuth + group stats."""

from __future__ import annotations

import os
from urllib.parse import urlencode

VK_AUTH = "https://oauth.vk.com/authorize"
VK_TOKEN = "https://oauth.vk.com/access_token"
API = "https://api.vk.com/method"
CLIENT_ID = os.getenv("VK_CLIENT_ID", "")
CLIENT_SECRET = os.getenv("VK_CLIENT_SECRET", "")
REDIRECT_URI = os.getenv("VK_REDIRECT_URI", "http://localhost:8000/platforms/vk/callback")
SCOPE = "groups,offline,stats"
API_VERSION = "5.199"


def auth_url(state: str) -> str:
    q = urlencode(
        {
            "client_id": CLIENT_ID,
            "display": "page",
            "redirect_uri": REDIRECT_URI,
            "scope": SCOPE,
            "response_type": "code",
            "state": state,
            "v": API_VERSION,
        }
    )
    return f"{VK_AUTH}?{q}"


async def exchange_code(code: str) -> dict:
    import httpx

    async with httpx.AsyncClient() as client:
        r = await client.get(
            VK_TOKEN,
            params={
                "client_id": CLIENT_ID,
                "client_secret": CLIENT_SECRET,
                "redirect_uri": REDIRECT_URI,
                "code": code,
            },
        )
        r.raise_for_status()
        return r.json()


async def get_group_stats(access_token: str, group_id: int) -> dict | None:
    import httpx

    async with httpx.AsyncClient() as client:
        r = await client.get(
            f"{API}/stats.get",
            params={
                "group_id": abs(group_id),
                "access_token": access_token,
                "v": API_VERSION,
            },
        )
        data = r.json()
        if "error" in data:
            return None
        return data.get("response")
