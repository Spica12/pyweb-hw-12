from datetime import datetime, timedelta
from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from jose import JWTError, jwt
from sqlalchemy.ext.asyncio import AsyncSession


from src.conf.config import config
from src.models.users import UserModel
from src.repositories.users import UserRepo
from src.schemas.user import UserCreateSchema
from src.dependencies.database import get_db


class AuthService:
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    SECRET_KEY = config.SECRET_KEY
    ALGORITHM = config.ALGORITHM

    oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

    def __init__(self, db: AsyncSession):
        self.repo = UserRepo(db=db)

    def get_password_hash(self, password: str):
        return self.pwd_context.hash(password)

    def verify_password(self, plain_password, hashed_pasword):
        return self.pwd_context.verify(plain_password, hashed_pasword)

    async def create_user(self, body: UserCreateSchema):
        new_user = await self.repo.create_user(body)
        return new_user

    async def get_user_by_username(self, username: str):
        user = await self.repo.get_user_by_username(username)
        return user

    async def create_access_token(
        self, data: dict, expires_delta: Optional[float] = None
    ):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + timedelta(seconds=expires_delta)
        else:
            expire = datetime.utcnow() + timedelta(days=7)
        to_encode.update(
            {"iat": datetime.utcnow(), "exp": expire, "scope": "access_token"}
        )
        encode_jwt = jwt.encode(to_encode, self.SECRET_KEY, algorithm=self.ALGORITHM)

        return encode_jwt

    async def create_refresh_token(
        self, data: dict, expires_delta: Optional[float] = None
    ):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + timedelta(seconds=expires_delta)
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)
        to_encode.update(
            {"iat": datetime.utcnow(), "exp": expire, "scope": "refresh_token"}
        )
        encode_jwt = jwt.encode(to_encode, self.SECRET_KEY, algorithm=self.ALGORITHM)

        return encode_jwt

    async def update_refresh_token(self, user: UserModel, refresh_token: str | None):
        await self.repo.update_token(user, refresh_token)

    async def decode_refresh_token(self, refresh_token: str):
        try:
            payload = jwt.decode(
                refresh_token, self.SECRET_KEY, algorithms=[self.ALGORITHM]
            )
            if payload["scope"] == "refresh_token":
                username = payload["sub"]
                return username
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid scope for token",
            )

        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
            )

    async def get_refresh_token_by_user(self, user: UserModel):
        refresh_token = await self.repo.get_refresh_token(user)
        return refresh_token

    async def get_current_user(
        self, token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)
    ):
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-AUTHENTICATE": "BEARER"},
        )
        try:
            payload = jwt.decode(token, self.SECRET_KEY, algorithms=[self.ALGORITHM])
            username = payload["sub"]
            if payload["scope"] == "access_token":
                if username is None:
                    raise credentials_exception
            else:
                raise credentials_exception
        except JWTError:
            raise credentials_exception

        user = await self.repo.get_user_by_username(username)
        if user is None:
            raise credentials_exception

        return user
