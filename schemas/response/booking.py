from marshmallow import fields
from marshmallow_enum import EnumField

from schemas.base import BaseBooking
from models.enums import BookingStatus


class BookingResponseSchema(BaseBooking):
    pk = fields.Integer(required=True)
    status = EnumField(BookingStatus, by_value=True)
    created_at = fields.DateTime(required=True)
    last_modified_at = fields.DateTime(required=True)
    rent_days = fields.Integer(required=True)
    amount = fields.Float(required=True)
    user_pk = fields.Integer(required=True)
