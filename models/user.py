from sqlalchemy.orm import Mapped, mapped_column

from db import db
from models.enums import UserType, UserRole


class User(db.Model):
    __tablename__ = "users"

    pk: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(db.String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(db.String(128), nullable=False)
    full_name: Mapped[str] = mapped_column(db.String(280), nullable=False)
    type: Mapped[UserType] = mapped_column(
        db.Enum(UserType), nullable=False, default=UserType.individual.name
    )
    role: Mapped[UserRole] = mapped_column(
        db.Enum(UserRole), default=UserRole.user.name, nullable=False
    )
