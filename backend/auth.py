from datetime import datetime, timedelta, timezone
import os
from typing import Annotated, Callable

from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
from passlib.context import CryptContext
import jwt
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import AsyncSession

from db.database import get_db_session
from db.managers.user_manager import UserManager
from db.models.users import User, UserRole

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY", "dev-only-change-me")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
# Must match actual login path for Swagger Authorize
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login")

DB_Dep = Annotated[AsyncSession, Depends(get_db_session)]


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (
        expires_delta
        if expires_delta
        else timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db_session),
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Failed to verify credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str | None = payload.get("sub")
        if not username:
            raise credentials_exception
    except jwt.InvalidTokenError:
        raise credentials_exception

    user_manager = UserManager(db)
    user = await user_manager.get_user_by_username(username)
    if user is None:
        raise credentials_exception
    return user


Current_User_Dep = Annotated[User, Depends(get_current_user)]


def require_roles(*roles: UserRole) -> Callable:
    """Dependency factory: endpoint allowed only for given roles."""
    allowed = set(roles)

    async def _checker(user: Current_User_Dep) -> User:
        if user.role not in allowed:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Required role: {', '.join(r.value for r in roles)}",
            )
        return user

    return _checker


ModeratorDep = Annotated[
    User, Depends(require_roles(UserRole.MODERATOR, UserRole.ADMIN))
]
AdminDep = Annotated[User, Depends(require_roles(UserRole.ADMIN))]
