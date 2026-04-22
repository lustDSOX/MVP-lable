from typing import Sequence
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from db.models.tracks import Track

class TrackManager:
    def __init__(self, session: AsyncSession):
        self.session = session

# ---------- CRUD --------------------

    async def create_track(
        self,
        release_id: int,
        title: str,
        order: int,
        master_file: str,
        preview_file: str,
        lyrics: str,
        is_explicit: bool = False
    ) -> Track:

        new_track = Track(
            release_id=release_id,
            title=title,
            order=order,
            master_file=master_file,
            preview_file=preview_file,
            lyrics=lyrics,
            is_explicit=is_explicit
        )
        
        self.session.add(new_track)
        await self.session.commit()
        await self.session.refresh(new_track)
        return new_track

    async def get_track_by_id(self, track_id: int, load_contributors: bool = False) -> Track | None:
        stmt = select(Track).where(Track.id == track_id)
        
        if load_contributors:
            stmt = stmt.options(selectinload(Track.contributors))
            
        return await self.session.scalar(stmt)

    async def get_tracks_for_release(self, release_id: int) -> Sequence[Track]:
        stmt = (
            select(Track)
            .where(Track.release_id == release_id)
            .order_by(Track.order.asc())
        )
        result = await self.session.scalars(stmt)
        return result.all()

    async def update_track_info(
        self,
        track: Track,
        title: str | None = None,
        lyrics: str | None = None,
        is_explicit: bool | None = None,
        order: int | None = None
    ) -> Track:

        if title is not None:
            track.title = title
        if lyrics is not None:
            track.lyrics = lyrics
        if is_explicit is not None:
            track.is_explicit = is_explicit
        if order is not None:
            track.order = order

        await self.session.commit()
        await self.session.refresh(track)
        return track

    async def delete_track(self, track: Track) -> None:
        await self.session.delete(track)
        await self.session.commit()