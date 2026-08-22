"""Apple Music catalog token + artist lookup."""

from __future__ import annotations

import os
import time

TEAM_ID = os.getenv("APPLE_TEAM_ID", "")
KEY_ID = os.getenv("APPLE_KEY_ID", "")
PRIVATE_KEY_PATH = os.getenv("APPLE_PRIVATE_KEY_PATH", "")
PRIVATE_KEY_PEM = os.getenv("APPLE_PRIVATE_KEY_PEM", "")


def developer_token(ttl_seconds: int = 3600 * 12) -> str | None:
    if not TEAM_ID or not KEY_ID:
        return None
    pem = PRIVATE_KEY_PEM
    if not pem and PRIVATE_KEY_PATH:
        with open(PRIVATE_KEY_PATH) as f:
            pem = f.read()
    if not pem:
        return None
    try:
        import jwt
    except ImportError:
        return None
    now = int(time.time())
    payload = {"iss": TEAM_ID, "iat": now, "exp": now + ttl_seconds}
    headers = {"alg": "ES256", "kid": KEY_ID}
    return jwt.encode(payload, pem, algorithm="ES256", headers=headers)


async def get_catalog_artist(artist_id: str, storefront: str = "ru") -> dict | None:
    import httpx

    token = developer_token()
    if not token:
        return None
    async with httpx.AsyncClient() as client:
        r = await client.get(
            f"https://api.music.apple.com/v1/catalog/{storefront}/artists/{artist_id}",
            headers={"Authorization": f"Bearer {token}"},
        )
        if r.status_code != 200:
            return None
        return r.json()
