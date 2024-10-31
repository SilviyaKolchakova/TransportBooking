from datetime import date, timedelta

from marshmallow import validates, ValidationError

from schemas.base import BaseBooking


class BookingRequestSchema(BaseBooking):
    pass
