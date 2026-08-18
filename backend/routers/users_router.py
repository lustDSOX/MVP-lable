from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel, ConfigDict, EmailStr, Field

from auth import (
    Current_User_Dep,
    DB_Dep,
    AdminDep,
    get_password_hash,
    verify_password,
    create_access_token,
    get_current_user,
)
from db.managers.user_manager import UserManager
from db.models.users import UserRole


async def get_user_manager(db: DB_Dep) -> UserManager:
    return UserManager(db)


Manager_Dep = Annotated[UserManager, Depends(get_user_manager)]

router = APIRouter(prefix="/users", tags=["Users"])

protect_router = APIRouter(
    prefix="/users",
    tags=["Users"],
    dependencies=[Depends(get_current_user)],
)

admin_router = APIRouter(
    prefix="/admin/users",
    tags=["Admin"],
    dependencies=[Depends(get_current_user)],
)


class UserCreate(BaseModel):
    username: str = Field(min_length=6)
    email: EmailStr
    password: str = Field(min_length=6)
    artist_name: str | None = None


class EmailUpdate(BaseModel):
    new_email: EmailStr


class ArtistNameUpdate(BaseModel):
    new_artist_name: str = Field(max_length=20)


class PasswordUpdate(BaseModel):
    new_password: str = Field(min_length=6)


class RoleUpdate(BaseModel):
    role: UserRole


class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    artist_name: str | None
    role: UserRole

    model_config = ConfigDict(from_attributes=True)


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    role: UserRole


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(user_data: UserCreate, user_manager: Manager_Dep):
    if await user_manager.get_user_by_email(user_data.email):
        raise HTTPException(status_code=400, detail="The user with this email already exists")
    if await user_manager.get_user_by_username(user_data.username):
        raise HTTPException(status_code=400, detail="This username is already occupied.")

    hashed_password = get_password_hash(user_data.password)
    try:
        new_user = await user_manager.create_user(
            username=user_data.username,
            artist_name=user_data.artist_name,
            role=UserRole.ARTIST,
            email=user_data.email,
            hashed_password=hashed_password,
        )
        return new_user
    except Exception:
        raise HTTPException(status_code=400, detail="Error on registration user")


@router.post("/login", response_model=TokenResponse)
async def login(
    user_manager: Manager_Dep,
    form_data: OAuth2PasswordRequestForm = Depends(),
):
    user = await user_manager.get_user_by_username(form_data.username)

    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(data={"sub": user.username})
    return TokenResponse(access_token=access_token, role=user.role)


@protect_router.patch("/profile/email", response_model=UserResponse)
async def update_email(
    data: EmailUpdate, user_manager: Manager_Dep, cur_user: Current_User_Dep
):
    try:
        return await user_manager.set_email(cur_user, data.new_email)
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))


@protect_router.patch("/profile/name", response_model=UserResponse)
async def update_artist_name(
    data: ArtistNameUpdate, user_manager: Manager_Dep, cur_user: Current_User_Dep
):
    try:
        return await user_manager.set_artistName(cur_user, data.new_artist_name)
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))


@protect_router.patch("/profile/password", response_model=UserResponse)
async def update_password(
    data: PasswordUpdate, user_manager: Manager_Dep, cur_user: Current_User_Dep
):
    hashed = get_password_hash(data.new_password)
    await user_manager.set_password(cur_user, hashed)
    return cur_user


@router.get("/search", response_model=list[UserResponse])
async def search_users(q: str, user_manager: Manager_Dep):
    return await user_manager.get_users_by_artistName(q)


@protect_router.get("/profile", response_model=UserResponse)
async def get_profile(cur_user: Current_User_Dep):
    return cur_user


@admin_router.patch("/{user_id}/role", response_model=UserResponse)
async def set_user_role(
    user_id: int,
    data: RoleUpdate,
    user_manager: Manager_Dep,
    _: AdminDep,
):
    user = await user_manager.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.role = data.role
    await user_manager.session.commit()
    await user_manager.session.refresh(user)
    return user
