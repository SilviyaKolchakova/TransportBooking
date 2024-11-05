from config import create_app
from db import db
from managers.auth import AuthManager
from flask_testing import TestCase


def generate_token(user):
    return AuthManager.encode_token(user)


class APIBaseTestCase(TestCase):
    def create_app(self):
        return create_app("config.TestingConfig")

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
