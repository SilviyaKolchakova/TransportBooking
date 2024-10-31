from marshmallow import fields

from schemas.base import BaseVehicle


class VehicleResponseSchema(BaseVehicle):
    pk = fields.Integer(required=True)
