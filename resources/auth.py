from flask import request
from flask_restful import Resource

from managers.user import UserManager


class RegisterUser(Resource):
    def post(self):
        data = request.get_json()
        return UserManager.register(data)


class LoginUser(Resource):
    def post(self):
        data = request.get_json()
        token = UserManager.login(data)
        return {"token": token}
