from datetime import datetime

from werkzeug.exceptions import BadRequest, abort

from db import db
from models import Booking, Vehicle
from models.enums import BookingStatus


class AdminManager:
    @staticmethod
    def confirm_booking(booking_id):
        booking = AdminManager._validate_booking_status(booking_id)
        booking.status = BookingStatus.confirmed
        # TODO: assign vehicle to booking
        booking.last_modified = datetime.utcnow()
        # TODO: send email to the user
        db.session.add(booking)
        db.session.flush()

    @staticmethod
    def cancel_booking(booking_id):
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
            abort(404, "Booking not found")

        if booking.status != BookingStatus.in_progress:
            raise BadRequest("Booking already processed")
        return booking

    @staticmethod
    def create_vehicle(data):
        vehicle = Vehicle(**data)
        db.session.add(vehicle)
        db.session.flush()

        return vehicle

    @staticmethod
    def get_all_vehicles():
        query = db.select(Vehicle)
        return db.session.execute(query).scalars().all()
