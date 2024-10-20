from flask import request
from flask_restful import Resource

from managers.admin import AdminManager
from managers.auth import auth
from managers.user import UserManager
from models import UserRole
from schemas.request.booking import BookingRequestSchema
from schemas.response.booking import BookingResponseSchema
from utils.decorators import permission_required, validate_schema


class Booking(Resource):  # create booking and get list of bookings
    @auth.login_required
    def get(self):
        current_user = auth.current_user()

        bookings = UserManager.get_bookings(current_user)
        return BookingResponseSchema().dump(bookings, many=True)

    @auth.login_required
    @permission_required(UserRole.user)
    @validate_schema(BookingRequestSchema)
    def post(self):
        data = request.get_json()
        current_user = auth.current_user()
        booking = UserManager.create_booking(current_user, data)
        return BookingResponseSchema().dump(booking)


class BookingConfirm(Resource):
    @auth.login_required
    @permission_required(UserRole.admin)
    def put(self, booking_id):
        AdminManager.booking_confirm(booking_id)
        return 204  # може да върнем освен статса и самият букинг


class BookingCancel(Resource):
    @auth.login_required
    @permission_required(UserRole.admin)
    def put(self, booking_id):
        AdminManager.booking_cancel(booking_id)
        return 204  # може да върнем освен статса и самият букинг
