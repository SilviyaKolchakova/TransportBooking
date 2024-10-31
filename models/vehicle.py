from sqlalchemy.orm import Mapped, mapped_column

from db import db


class Vehicle(db.Model):
    __tablename__ = "vehicles"

    pk: Mapped[int] = mapped_column(primary_key=True)
    make: Mapped[str] = mapped_column(db.String(50), nullable=False)
    model: Mapped[str] = mapped_column(db.String(50), nullable=False)
    seating_capacity: Mapped[int] = mapped_column(db.Integer, nullable=False)
