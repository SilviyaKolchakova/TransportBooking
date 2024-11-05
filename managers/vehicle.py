from http.client import HTTPException

from werkzeug.exceptions import abort

from db import db
from models import Vehicle
from schemas.response.vehicle import VehicleResponseSchema


class VehicleManager:
    @staticmethod
    def update_vehicle(vehicle_id, new_data):
        vehicle = VehicleManager._get_vehicle(vehicle_id)
        vehicle.make = new_data["make"]
        vehicle.model = new_data["model"]
        vehicle.seating_capacity = new_data["seating_capacity"]
        db.session.commit()
        return VehicleResponseSchema().dump(vehicle)

    @staticmethod
    def show_vehicle(vehicle_id):
        vehicle = VehicleManager._get_vehicle(vehicle_id)
        return VehicleResponseSchema().dump(vehicle)

    @staticmethod
    def delete_vehicle(vehicle_id):
        vehicle = VehicleManager._get_vehicle(vehicle_id)
        db.session.delete(vehicle)

    @staticmethod
    def _get_vehicle(vehicle_id):
        vehicle = db.session.execute(Vehicle.query.filter_by(pk=vehicle_id)).scalar()
        if not vehicle:
            abort(404, "Vehicle not found")
        return vehicle
