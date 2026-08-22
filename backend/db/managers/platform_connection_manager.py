from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from db.models.platform_connections import (
    ConnectionStatus,
    PlatformConnection,
    PlatformKind,
)


class PlatformConnectionManager:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get(self, user_id: int, platform: PlatformKind) -> PlatformConnection | None:
        stmt = select(PlatformConnection).where(
            PlatformConnection.user_id == user_id,
            PlatformConnection.platform == platform,
        )
        return await self.session.scalar(stmt)

    async def list_for_user(self, user_id: int) -> list[PlatformConnection]:
        stmt = select(PlatformConnection).where(PlatformConnection.user_id == user_id)
        return list((await self.session.scalars(stmt)).all())

    async def upsert(
        self,
        user_id: int,
        platform: PlatformKind,
        **fields,
    ) -> PlatformConnection:
        row = await self.get(user_id, platform)
        if not row:
            row = PlatformConnection(user_id=user_id, platform=platform)
            self.session.add(row)
        for k, v in fields.items():
            if hasattr(row, k) and v is not None:
                setattr(row, k, v)
        await self.session.commit()
        await self.session.refresh(row)
        return row

    async def set_tokens(
        self,
        user_id: int,
        platform: PlatformKind,
        access_token: str,
        refresh_token: str | None,
        expires_at: datetime | None,
        external_user_id: str | None = None,
        display_name: str | None = None,
        scopes: str | None = None,
    ) -> PlatformConnection:
        return await self.upsert(
            user_id,
            platform,
            status=ConnectionStatus.CONNECTED,
            access_token=access_token,
            refresh_token=refresh_token,
            token_expires_at=expires_at,
            external_user_id=external_user_id,
            display_name=display_name,
            scopes=scopes,
        )

    async def set_artist_id(
        self, user_id: int, platform: PlatformKind, external_artist_id: str
    ) -> PlatformConnection:
        return await self.upsert(
            user_id, platform, external_artist_id=external_artist_id
        )

    async def mark_synced(self, conn: PlatformConnection, meta: dict | None = None) -> None:
        conn.last_synced_at = datetime.now(timezone.utc)
        if meta is not None:
            conn.meta = {**(conn.meta or {}), **meta}
        await self.session.commit()

    async def disconnect(self, user_id: int, platform: PlatformKind) -> None:
        row = await self.get(user_id, platform)
        if row:
            row.status = ConnectionStatus.REVOKED
            row.access_token = None
            row.refresh_token = None
            await self.session.commit()
