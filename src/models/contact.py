from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Date, ForeignKey, Integer
from sqlalchemy.dialects.postgresql import UUID

from src.models.base import Base
from src.models.users import UserModel


class ContactModel(Base):
    __tablename__ = "contacts"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    surname: Mapped[str] = mapped_column(String(50), nullable=True)
    email: Mapped[str] = mapped_column(String(50), nullable=True)
    phone: Mapped[str] = mapped_column(String(50), nullable=True)
    birthday: Mapped[Date] = mapped_column(Date(), nullable=True)
    notes: Mapped[str] = mapped_column(String(1000), nullable=True)
    is_favorite: Mapped[bool] = mapped_column(default=False)
    user_id: Mapped[UUID] = mapped_column(UUID, ForeignKey("users.id"), nullable=True)
    user: Mapped[UserModel] = relationship(
        "UserModel", backref="contacts", lazy="joined"
    )
