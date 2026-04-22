from sqlalchemy import  exists, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy.exc import IntegrityError

from db.models.releases import Release
from db.models.users import User, UserRole


class UserManager:

    def __init__(self, session:AsyncSession):
        self.session = session

    async def create_user(self, username:str, artist_name:str, email:str, hashed_password:str, role:str = UserRole.ARTIST) -> User:
        new_user = User(
            username=username,
            artist_name = artist_name,
            role = role,
            email=email,
            hashed_password=hashed_password,
        )

        try:
            self.session.add(new_user)
            await self.session.commit()
            await self.session.refresh(new_user)
            return new_user
        except IntegrityError:
            await self.session.rollback()
            raise ValueError("this user is a already exists")


# --------------------- SET methods -------------------------
    async def set_email(self, user:User, email:str) -> None:
        stmt = select(
            exists()
            .where(User.email == email, User.id != user.id)
        )
        email_taken = await self.session.scalar(stmt)
        if email_taken:
            raise ValueError("email is busy")
        
        user.email = email
        await self.session.commit()
        await self.session.refresh(user)

    async def set_artistName(self, user:User, artist_name:str) -> None:
        stmt = select(
            exists()
            .where(User.artist_name == artist_name, User.id != user.id)
        )
        artist_name_taken = await self.session.scalar(stmt)
        if artist_name_taken:
            raise ValueError("artist name is busy")
        
        user.artist_name = artist_name
        await self.session.commit()
        await self.session.refresh(user)

    async def set_password(self, user: User, new_hashed_password: str) -> None:
        user.hashed_password = new_hashed_password
        await self.session.commit()



# --------------------- GET methods --------------------------
    async def get_user_by_email(self, email:str) -> User|None:
        stmt = select(User).where(User.email == email)
        return await self.session.scalar(stmt)
        
    async def get_user_by_username(self, username:str) -> User|None:
        stmt = select(User).where(User.username == username)
        return await self.session.scalar(stmt)
    
    async def get_users_by_artistName(self, artist_name:str) -> list[User]:
        artist_name = f"%{artist_name}%"
        stmt = select(User).where(User.artist_name.ilike(artist_name))
        result =  await self.session.scalars(stmt)
        return result.all()
    
    async def get_user_by_id(self, user_id: int) -> User | None:
        stmt = select(User).where(User.id == user_id)
        return await self.session.scalar(stmt)

    async def get_user_releases(self, user:User, limit:int = 10, offset:int = 0) -> list[Release]:
        stmt = (
            select(Release)
            .where(Release.owner_id == user.id)
            .order_by(Release.created_at.desc())
            .limit(limit)
            .offset(offset)
        )

        result = await self.session.scalars(stmt)
        return result.all()
    
    async def get_user_with_relations(self, user_id: int) -> User | None:
        stmt = (
            select(User)
            .where(User.id == user_id)
            .options(
                selectinload(User.releases),
                selectinload(User.contributions)
            )
        )
        return await self.session.scalar(stmt)
    

# ---------- other -------------------

    async def delete_user(self, user: User) -> None:
        await self.session.delete(user)
        await self.session.commit()