from datetime import date, timedelta

from marshmallow import Schema, fields, ValidationError, validates, validates_schema


class BaseBooking(Schema):
    start_date = fields.Date(required=True)
    end_date = fields.Date(required=True)

    # Ensure start date is at least 3 days in the future
    @validates("start_date")
    def validate_start_date(self, value):
        if value < date.today() + timedelta(days=3):
            raise ValidationError("Start date must be at least 3 days in the future.")

    # Ensure end_date is after start_date
    @validates_schema
    def validate_end_after_start(self, data, **kwargs):
        start_date = data.get("start_date")
        end_date = data.get("end_date")

        if start_date and end_date:
            if end_date <= start_date:
                raise ValidationError("End date must be after the start date.")


class BaseVehicle(Schema):
    make = fields.Str(required=True)
    model = fields.Str(required=True)
    seating_capacity = fields.Int(required=True)
