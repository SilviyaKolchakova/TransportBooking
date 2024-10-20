from datetime import datetime

from werkzeug.exceptions import BadRequest

from db import db
from models import Booking
from models.enums import BookingStatus


class AdminManager:
    @staticmethod
    def booking_confirm(booking_id):
        booking = AdminManager._validate_booking_status(booking_id)
        booking.status = BookingStatus.confirmed
        booking.last_modified = datetime.utcnow()
        # TODO: send email to the user
        db.session.add(booking)
        db.session.flush()

    @staticmethod
    def booking_cancel(booking_id):
        booking = AdminManager._validate_booking_status(booking_id)
        booking.status = BookingStatus.canceled
        booking.last_modified = datetime.utcnow()
        # TODO: send email to the user
        db.session.add(booking)
        db.session.flush()

    @staticmethod
    def _validate_booking_status(booking_id):
        booking = db.session.execute(Booking.query.filter_by(pk=booking_id)).scalar()
        if not booking:
            raise BadRequest("Booking does not exist")

        if booking.status != BookingStatus.in_progress:
            raise BadRequest("Booking already processed")
        return booking
