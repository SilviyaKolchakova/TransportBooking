from datetime import datetime, timedelta
from decouple import config
import jwt
from flask_httpauth import HTTPTokenAuth
from werkzeug.exceptions import Unauthorized

from db import db
from models.user import User


class AuthManager:
    @staticmethod
    def encode_token(user):
        payload = {
            "sub": user.pk,
            "exp": datetime.utcnow() + timedelta(hours=2),
            "role": user.role if isinstance(user.role, str) else user.role.name,
            "type": user.type if isinstance(user.type, str) else user.type.name,
        }
        return jwt.encode(payload, key=config("SECRET_KEY"), algorithm="HS256")

    @staticmethod
    def decode_token(token):
        try:
            result = jwt.decode(
                jwt=token, key=config("SECRET_KEY"), algorithms=config("ALGORITHMS")
            )
            return result["sub"], result["role"]
        except Exception as ex:
            return ex


auth = HTTPTokenAuth(scheme="Bearer")


@auth.verify_token
def verify_token(token):
    try:
        user_pk, user_role = AuthManager.decode_token(token)
        return db.session.execute(db.select(User).filter_by(pk=user_pk)).scalar()
    except Exception:
        return Unauthorized("Invalid or missing token")
