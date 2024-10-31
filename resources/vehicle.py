from flask import request
from flask_restful import Resource

from managers import vehicle
from managers.admin import AdminManager
from managers.auth import auth
from managers.vehicle import VehicleManager
from models import UserRole
from schemas.request.vehicle import VehicleRequestSchema
from schemas.response.vehicle import VehicleResponseSchema
from utils.decorators import permission_required, validate_schema


class VehiclesResource(Resource):
    def get(self):
        vehicles = AdminManager.get_all_vehicles()
        return VehicleResponseSchema().dump(vehicles, many=True)

    @auth.login_required
    @permission_required(UserRole.admin)
    @validate_schema(VehicleRequestSchema)
    def post(self):
        data = request.get_json()
        vehicle = AdminManager.create_vehicle(data)
        return VehicleResponseSchema().dump(vehicle)


class VehicleResource(Resource):
    def get(self, vehicle_id):
        return VehicleManager.show_vehicle(vehicle_id)

    @auth.login_required
    @permission_required(UserRole.admin)
    def put(self, vehicle_id):
        data = request.get_json()
        return VehicleManager.update_vehicle(vehicle_id, data), 204

    @auth.login_required
    @permission_required(UserRole.admin)
    def delete(self, vehicle_id):
        return VehicleManager.delete_vehicle(vehicle_id), 204
