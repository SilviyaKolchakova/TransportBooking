from flask import request
from flask_restful import Resource

from db import db
from managers.admin import AdminManager
from managers.auth import auth
from managers.user import UserManager
from models import UserRole, Booking
from schemas.request.booking import BookingRequestSchema
from schemas.response.booking import BookingResponseSchema
from services.stripe import StripeService

from utils.decorators import permission_required, validate_schema


stripe_service = StripeService()


class BookingsResource(Resource):  # create booking and get list of bookings
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
        # return BookingResponseSchema().dump(booking)
        return UserManager.create_booking(current_user, data)


class BookingConfirm(Resource):
    @auth.login_required
    @permission_required(UserRole.admin)
    def put(self, booking_id):
        AdminManager.confirm_booking(booking_id)
        return 204


class BookingCancel(Resource):
    @auth.login_required
    @permission_required(UserRole.admin)
    def put(self, booking_id):
        AdminManager.cancel_booking(booking_id)
        return 204  # може да върнем освен статса и самия букинг


class BookingDelete(Resource):
    @auth.login_required
    @permission_required(UserRole.user)
    def delete(self, booking_id):
        # TODO: add functionality
        pass


# TODO: create class BookingVehicleAssign. Admins to assign vehicle to confirmed bookings.


class PaymentSuccess(Resource):
    def get(self, session_id):

        if not session_id:
            return {"error": "Session ID not provided"}, 400

        UserManager.retrieve_booking(session_id)

        # TODO: redirect to transport booking app
        return {"message": f"Payment successful for session ID {session_id}"}, 200


class PaymentFailure(Resource):
    def get(self):
        return "Your booking has failed to pay. Plaese...."  # TODO: to check what message should be returned
