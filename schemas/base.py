from datetime import date, timedelta

from marshmallow import Schema, fields, ValidationError, validates


class BaseBooking(Schema):
    start_date = fields.Date(required=True)
    end_date = fields.Date(required=True)

    # Ensure start date is at least 3 days in the future
    @validates("start_date")
    def validate_start_date(self, value):
        if value < date.today() + timedelta(days=3):
            raise ValidationError("Start date must be at least 3 days in the future.")

    # Ensure end_date is after start_date
    @validates("end_date")
    def validate_end(self, value):
        if value <= date.today():
            raise ValidationError("End date must be in the future.")
        if value < date.today() + timedelta(days=4):
            raise ValidationError("End date must be after start date.")


class BaseVehicle(Schema):
    make = fields.Str(required=True)
    model = fields.Str(required=True)
    seating_capacity = fields.Int(required=True)
