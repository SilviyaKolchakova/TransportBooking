from marshmallow import Schema, fields


class BaseBooking(Schema):
    start_date = fields.Date(required=True, load_only=True)
    end_date = fields.Date(required=True, load_only=True)
