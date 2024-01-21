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

router = APIRouter(prefix="/auth", tags=["auth"])
get_refresh_token = HTTPBearer()


@router.post(
    "/signup", response_model=UserReadSchema, status_code=status.HTTP_201_CREATED
)
async def signup(body: UserCreateSchema, db: AsyncSession = Depends(get_db)):
    exist_user = await repositories_users.get_user_by_username(body.username, db)
    if exist_user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='Account already exists')
    body.password = auth_service.get_password_hash(body.password)
    new_user = await repositories_users.create_user(body, db)

    return new_user


# @router.post("/login")
# async def login(body: OAuth2PasswordRequestForm, db: AsyncSession = Depends(get_db)):

#     return {}


# @router.post("/refresh_token")
# async def refresh_token(
#     credentials: HTTPAuthorizationCredentials = Security(get_refresh_token),
#     db: AsyncSession = Depends(get_db),
# ):
#     pass
