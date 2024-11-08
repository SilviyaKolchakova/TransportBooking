from config import create_app
from db import db
from managers.auth import AuthManager
from flask_testing import TestCase

from models import User, Booking
from tests import UserFactory


def generate_token(user):
    return AuthManager.encode_token(user)


def get_session_id():
    return "cs_123456"


def register_user(self, *args, **kwargs):

    data, message = args
    users = User.query.all()
    self.assertEqual(len(users), 0)

    response = self.client.post("/register", json=data)
    self.assertEqual(response.status_code, 400)
    expected_message = message
    self.assertEqual(response.json, expected_message)

    users = User.query.all()
    self.assertEqual(len(users), 0)


def create_booking(self, *args, **kwargs):

    data, message = args
    user = UserFactory()
    token = generate_token(user)

    bookings = Booking.query.all()
    self.assertEqual(len(bookings), 0)

    response = self.client.post(
        "/users/bookings",
        json=data,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        },
    )
    self.assertEqual(response.status_code, 400)
    expected_message = message
    self.assertEqual(response.json, expected_message)

    bookings = Booking.query.all()
    self.assertEqual(len(bookings), 0)


class APIBaseTestCase(TestCase):
    def create_app(self):
        return create_app("config.TestingConfig")

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
