"""
Seed demo CMS + optional users. Run once after migrations:

  cd backend
  python -m scripts.seed_demo
"""

import asyncio
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import select
from db.database import AsyncSessionLocal
from db.models.cms import CmsStatus, EventItem, GuideItem, NewsItem
from db.models.users import User, UserRole
from auth import get_password_hash


NEWS = [
    {
        "title": "GRID_OPENING",
        "excerpt": "Лейбл открывает сезон",
        "body": "## Сезон открыт\n\nЛейбл запускает **новый цикл** релизов.",
        "date": "2026-03-01",
        "status": CmsStatus.PUBLISHED,
    },
    {
        "title": "NEON_DROP",
        "excerpt": "Новый релиз в сети",
        "body": "### NEON_DROP\n\nСтриминг со **всех площадок**.",
        "date": "2026-04-12",
        "status": CmsStatus.PUBLISHED,
    },
]

GUIDES = [
    {
        "title": "RELEASE_PIPELINE",
        "excerpt": "Как сдать релиз без отказов",
        "body": "# Release pipeline\n\n1. Метаданные\n2. Обложка 3000×3000\n3. Треки + тексты\n4. Договор",
        "category": "releases",
        "status": CmsStatus.PUBLISHED,
    },
    {
        "title": "CONTRACT_SIGN",
        "excerpt": "Подписание договора",
        "body": "## Договор\n\nОдин контракт на **весь релиз**.",
        "category": "legal",
        "status": CmsStatus.PUBLISHED,
    },
]

EVENTS = [
    {
        "title": "UNDERGROUND_NIGHT",
        "venue": "Club Void",
        "city": "Moscow",
        "date": "15 AUG",
        "time": "23:00",
        "description": "Live set · CLASS TICKETS night",
        "ticket_url": "/purchase",
        "price": "1500 RUB",
        "capacity": "400",
        "age_limit": "18+",
        "status": CmsStatus.PUBLISHED,
    },
]

DEMO_USERS = [
    ("admin", "System Overlord", "admin@label.ru", "admin123", UserRole.ADMIN),
    ("moderator", "Chief Editor", "moderator@label.ru", "mod123", UserRole.MODERATOR),
    ("demo", "DJ Neon", "demo@label.ru", "demo123", UserRole.ARTIST),
]


async def main():
    async with AsyncSessionLocal() as session:
        for username, artist, email, pwd, role in DEMO_USERS:
            exists = await session.scalar(select(User).where(User.email == email))
            if exists:
                continue
            session.add(
                User(
                    username=username,
                    artist_name=artist,
                    email=email,
                    hashed_password=get_password_hash(pwd),
                    role=role,
                    full_name=artist,
                )
            )
        await session.commit()

        n_count = await session.scalar(select(NewsItem.id).limit(1))
        if not n_count:
            for row in NEWS:
                session.add(NewsItem(**row))
            await session.commit()

        g_count = await session.scalar(select(GuideItem.id).limit(1))
        if not g_count:
            for row in GUIDES:
                session.add(GuideItem(**row))
            await session.commit()

        e_count = await session.scalar(select(EventItem.id).limit(1))
        if not e_count:
            for row in EVENTS:
                session.add(EventItem(**row))
            await session.commit()

        print("Seed OK")


if __name__ == "__main__":
    asyncio.run(main())
