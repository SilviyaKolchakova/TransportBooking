from datetime import datetime

from argon2 import PasswordHasher
from werkzeug.exceptions import Unauthorized

from constants import RENT_PRICE_PER_DAY
from db import db


from managers.auth import AuthManager, auth
from models.booking import Booking
from models.enums import UserRole
from models.user import User

from services.stripe import StripeService

stripe_service = StripeService()

ph = PasswordHasher()


class UserManager:
    @staticmethod
    def login(data):
        user = db.session.execute(
            db.select(User).filter_by(email=data["email"])
        ).scalar()
        if user and ph.verify(user.password, data["password"]):
            return AuthManager.encode_token(user)
        raise Unauthorized()

    @staticmethod
    def register(user_data):
        user_data["password"] = ph.hash(user_data["password"])

        user_data["role"] = UserRole.user.name
        user = User(**user_data)
        db.session.add(user)
        db.session.flush()

        token = AuthManager.encode_token(user)
        return {"token": token}, 201

    @staticmethod
    def get_bookings(user):
        # TODO: to check how it was handled in the previous course
        query = db.select(Booking)

        if user.role == UserRole.user:
            query = query.filter_by(user_pk=user.pk)
            return db.session.execute(query).scalars().all()
        else:
            return db.session.execute(query).scalars().all()

    @staticmethod
    def create_booking(user, data):
        data["user_pk"] = user.pk

        start_date = datetime.strptime(data["start_date"], "%Y-%m-%d")
        end_date = datetime.strptime(data["end_date"], "%Y-%m-%d")
        data["rent_days"] = (end_date - start_date).days
        data["amount"] = (
            data["rent_days"] * RENT_PRICE_PER_DAY
        )  # TODO: put rent_per_day_price as constant

        booking = Booking(**data)
        current_user = auth.current_user()
        customer_name = current_user.full_name
        customer_email = current_user.email

        db.session.add(booking)

        db.session.flush()

        return UserManager.pay_booking(booking, customer_name, customer_email)

    @staticmethod
    def pay_booking(booking, customer_name, customer_email):

        stripe_customer = stripe_service.create_customer(customer_name, customer_email)
        stripe_customer_id = stripe_customer["id"]
        url = stripe_service.create_checkout_session(
            stripe_customer_id, booking.amount, currency="bgn", booking_id=booking.pk
        )
        return url

    @staticmethod
    def retrieve_booking(session_id):
        retrieve_session = stripe_service.retrieve_checkout_session(session_id)
        session_booking_id = retrieve_session["metadata"]
        booking_id = session_booking_id["booking_id"]
        # TODO : да se prawi proerlka dali ima booking i kakyv mu e statusa. Da vidq kyde da premestq tazi logika
        booking = db.session.execute(
            db.select(Booking).filter_by(pk=booking_id)
        ).scalar()
        booking.is_paid = True
        db.session.commit()
