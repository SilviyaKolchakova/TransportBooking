from argon2 import PasswordHasher
from werkzeug.exceptions import Unauthorized

from db import db


from managers.auth import AuthManager, auth
from models.booking import Booking
from models.enums import UserRole
from models.user import User

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

        if user.role.user == UserRole.user:
            query = query.filter_by(user_pk=user.pk)
            return db.session.execute(query).scalars().all()
        else:
            pass

    @staticmethod
    def create_booking(user, data):
        data["user_pk"] = user.pk
        # data["start_date"] = data["start_date"].strftime("%Y-%m-%d")
        # data["end_date"] = data["end_date"].strftime("%Y-%m-%d")
        booking = Booking(**data)
        db.session.add(booking)
        db.session.flush()
        return booking


