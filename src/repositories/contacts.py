from models.contact import ContactModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, text

from datetime import datetime, timedelta

from schemas.contact import ContactSchema, ContactCreateSchema


class ContactRepo:
    def __init__(self, db):
        self.db: AsyncSession = db

    async def get_all(self, limit: int, offset: int):
        stmt = select(ContactModel).offset(offset).limit(limit)
        contacts = await self.db.execute(stmt)

        return contacts.scalars().all()

    async def create(self, body: ContactCreateSchema):
        contact = ContactModel(**body.model_dump(exclude_unset=True))
        self.db.add(contact)
        await self.db.commit()
        await self.db.refresh(contact)

        return contact

    async def get_by_id(self, contact_id: int):
        stmt = select(ContactModel).filter_by(id=contact_id)
        contacts = await self.db.execute(stmt)

        return contacts.scalar_one_or_none()

    async def update(self, contact_id: int, body: ContactCreateSchema):
        stmt = select(ContactModel).filter_by(id=contact_id)
        result = await self.db.execute(stmt)
        contact = result.scalar_one_or_none()

        if contact:
            contact.name = body.name
            contact.surname = body.surname
            contact.email = body.email
            contact.phone = body.phone
            contact.birthday = body.birthday
            contact.notes = body.notes
            contact.is_favorite = body.is_favorite
            await self.db.commit()
            await self.db.refresh(contact)

        return contact

    async def delete(self, contact_id: int):
        stmt = select(ContactModel).filter_by(id=contact_id)
        result = await self.db.execute(stmt)
        contact = result.scalar_one_or_none()
        if contact:
            await self.db.delete(contact)
            await self.db.commit()

        return contact

    async def get_by_name(self, key_name: str):
        stmt = (
            select(ContactModel)
            .where(text("LOWER(name) LIKE LOWER(:key_name)"))
            .params(key_name=f"%{key_name}%")
        )
        result = await self.db.execute(stmt)

        return result.scalars().all()

    async def get_by_surname(self, key_surname: str):
        stmt = (
            select(ContactModel)
            .where(text("LOWER(surname) LIKE LOWER(:key_name)"))
            .params(key_name=f"%{key_surname}%")
        )
        result = await self.db.execute(stmt)

        return result.scalars().all()

    async def get_by_email(self, key_email: str):
        stmt = (
            select(ContactModel)
            .where(text("LOWER(email) LIKE LOWER(:key_name)"))
            .params(key_name=f"%{key_email}%")
        )
        result = await self.db.execute(stmt)

        return result.scalars().all()

    async def get_upcoming_birthday(self, limit: int, offset: int):
        today = datetime.now().date()
        next_week = today + timedelta(days=7)
        stmt = (
            select(ContactModel)
            .where(ContactModel.birthday.between(today, next_week))
            .offset(offset)
            .limit(limit)
        )
        upcoming_birthdays = await self.db.execute(stmt)

        return upcoming_birthdays.scalars().all()
