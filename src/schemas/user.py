from pydantic import BaseModel, EmailStr, Field
from datetime import date

import uuid


class UserCreateSchema(BaseModel):
    username: EmailStr
    password: str = Field(min_length=6, max_length=12)


class UserReadSchema(BaseModel):
    id: uuid.UUID
    username: EmailStr
    password: str
