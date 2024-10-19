from datetime import datetime


from sqlalchemy.orm import Mapped, mapped_column, relationship

from db import db
from models import User
from models.enums import BookingStatus


class Booking(db.Model):
    __tablename__ = "bookings"

    pk: Mapped[int] = mapped_column(primary_key=True)
    start_date: Mapped[datetime] = mapped_column(db.DateTime, nullable=False)
    end_date: Mapped[datetime] = mapped_column(db.DateTime, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        db.DateTime, default=datetime.utcnow(), nullable=False
    )
    status: Mapped[BookingStatus] = mapped_column(
        db.Enum(BookingStatus), default=BookingStatus.in_progress, nullable=False
    )
    user_pk: Mapped[int] = mapped_column(db.Integer, db.ForeignKey("users.pk"))
    user: Mapped["User"] = relationship("User")

    