from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import Depends

from src.models.users import UserModel
from src.dependencies.database import get_db


async def get_user_by_username(username: str, db: AsyncSession = Depends(get_db)):
    stmt = select(UserModel).filter_by(username=username)
    user = await db.execute(stmt)
    user = user.scalar_one_or_none()

    return user


async def create_user(body: UserModel, db: AsyncSession = Depends(get_db)):
    new_user = UserModel(**body.model_dump())
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    return new_user
