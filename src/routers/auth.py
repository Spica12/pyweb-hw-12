from fastapi import APIRouter, HTTPException, Depends, status, Path, Query, Security
from src.dependencies.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.security import (
    OAuth2PasswordRequestForm,
    HTTPAuthorizationCredentials,
    HTTPBearer,
)

from src.schemas.user import UserCreateSchema, UserReadSchema
from src.repositories import users as repositories_users
from src.services.auth import auth_service

router = APIRouter(tags=["auth"])
get_refresh_token = HTTPBearer()


@router.post(
    "/signup", response_model=UserReadSchema, status_code=status.HTTP_201_CREATED
)
async def signup(body: UserCreateSchema, db: AsyncSession = Depends(get_db)):
    exist_user = await repositories_users.get_user_by_username(body.username, db)
    if exist_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Account already exists"
        )
    body.password = auth_service.get_password_hash(body.password)
    new_user = await repositories_users.create_user(body, db)

    return new_user


@router.post("/login")
async def login(
    body: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)
):
    user = await repositories_users.get_user_by_username(body.username, db)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username"
        )
    if not auth_service.verify_password(body.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid password"
        )
    access_token = await auth_service.create_access_token(data={"sub": user.username})
    refresh_token = await auth_service.create_refresh_token(data={"sub": user.username})

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }


# @router.post("/refresh_token")
# async def refresh_token(
#     credentials: HTTPAuthorizationCredentials = Security(get_refresh_token),
#     db: AsyncSession = Depends(get_db),
# ):
#     pass
