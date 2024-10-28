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


class BookingResource(Resource):  # create booking and get list of bookings
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
        AdminManager.booking_confirm(booking_id)
        return 204  # може да върнем освен статса и самия букинг


class BookingCancel(Resource):
    @auth.login_required
    @permission_required(UserRole.admin)
    def put(self, booking_id):
        AdminManager.booking_cancel(booking_id)
        return 204  # може да върнем освен статса и самия букинг


class PaymentSuccess(Resource):
    def get(self, session_id):

        if not session_id:
            return {"error": "Session ID not provided"}, 400

        retrieve_session = stripe_service.retrieve_checkout_session(session_id)
        session_booking_id = retrieve_session["metadata"]
        booking_id = session_booking_id["booking_id"]
        # TODO : да se prawi proerlka dali ima booking i kakyv mu e statusa. Da vidq kyde da premestq tazi logika
        booking = db.session.execute(
            db.select(Booking).filter_by(pk=booking_id)
        ).scalar()
        booking.status = "completed"
        db.session.commit()

        # Handle the payment success
        return {"message": f"Payment successful for session ID {session_id}"}, 200


class PaymentFailure(Resource):
    def get(self):
        return "Your booking has failed to pay. Plaese...."  # TODO: to check what message should be returned
