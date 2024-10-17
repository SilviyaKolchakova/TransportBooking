from argon2 import PasswordHasher
from werkzeug.exceptions import Unauthorized

from db import db


from managers.auth import AuthManager
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
