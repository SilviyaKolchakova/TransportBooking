from flask_testing import TestCase

from models import UserRole, User
from tests.base import generate_token, APIBaseTestCase
from tests.factories import UserFactory


class TestProtectedEndpoints(APIBaseTestCase):
    endpoints = (
        ("GET", "/users/bookings"),
        ("POST", "/users/bookings"),
        ("PUT", "/bookings/1/confirm"),
        ("PUT", "/bookings/1/cancel"),
        ("POST", "/vehicles"),
        ("PUT", "/vehicles/1"),
        ("DELETE", "/vehicles/1"),
    )

    def make_request(self, method, url, headers=None):
        if method == "GET":
            response = self.client.get(url, headers=headers)
        elif method == "POST":
            response = self.client.post(url, headers=headers)
        elif method == "PUT":
            response = self.client.put(url, headers=headers)
        else:
            response = self.client.delete(url, headers=headers)

        return response

    def test_login_required_endpoints_missing_token(self):

        for method, url in self.endpoints:
            response = self.make_request(method, url)

            self.assertEqual(response.status_code, 401)
            expected_message = {"message": "Invalid or missing token"}
            self.assertEqual(response.json, expected_message)

    def test_login_required_endpoints_invalid_token(self):

        headers = {"Authorization": "Bearer invalid token"}

        for method, url in self.endpoints:
            response = self.make_request(method, url, headers=headers)

            self.assertEqual(response.status_code, 401)
            expected_message = {"message": "Invalid or missing token"}
            self.assertEqual(response.json, expected_message)

    def test_permission_required_endpoints_admins(self):
        endpoints = (
            ("PUT", "/bookings/1/confirm"),
            ("PUT", "/bookings/1/cancel"),
            ("POST", "/vehicles"),
            ("PUT", "/vehicles/1"),
            ("DELETE", "/vehicles/1"),
        )
        # regular user(client)
        user = UserFactory()
        user_token = generate_token(user)
        headers = {"Authorization": f"Bearer {user_token}"}

        for method, url in endpoints:
            response = self.make_request(method, url, headers=headers)

            self.assertEqual(response.status_code, 403)
            expected_message = {"message": "No access to perform this action"}
            self.assertEqual(response.json, expected_message)

    def test_permission_required_endpoints_user(self):
        endpoints = (("POST", "/users/bookings"),)
        # user has admin role
        user = UserFactory(role=UserRole.admin)
        user_token = generate_token(user)
        headers = {"Authorization": f"Bearer {user_token}"}
        for method, url in endpoints:
            response = self.make_request(method, url, headers=headers)

            self.assertEqual(response.status_code, 403)
            expected_message = {"message": "No access to perform this action"}
            self.assertEqual(response.json, expected_message)


class TestRegisterSchema(APIBaseTestCase):
    def register_user(self, *args, **kwargs):
        # data = {
        #     "email": "test1bg",  # email value is not valid
        #     "password": "Testpass1!",
        #     "full_name": "Pol Mol",
        # }

        data, message = args
        users = User.query.all()
        self.assertEqual(len(users), 0)

        response = self.client.post("/register", json=data)
        self.assertEqual(response.status_code, 400)
        expected_message = message
        self.assertEqual(response.json, expected_message)

        users = User.query.all()
        self.assertEqual(len(users), 0)

    # def test_register_schema_missing_fields(self):
    #     data = {}
    #
    #     users = User.query.all()
    #     self.assertEqual(len(users), 0)
    #
    #     response = self.client.post("/register", json=data)
    #     self.assertEqual(response.status_code, 400)
    #     expected_message = {
    #         "message": "Invalid request: {'email': ['Missing data for required field.'], 'password': ['Missing data for required field.'], 'full_name': ['Missing data for required field.']}"
    #     }
    #     self.assertEqual(response.json, expected_message)
    #
    #     users = User.query.all()
    #     self.assertEqual(len(users), 0)

    def test_register_schema_missing_fields(self):
        data = {}
        expected_message = {
            "message": "Invalid request: {'email': ['Missing data for required field.'], 'password': ['Missing data for required field.'], 'full_name': ['Missing data for required field.']}"
        }
        return TestRegisterSchema.register_user(self, data, expected_message)

    def test_register_schema_invalid_email(self):
        data = {
            "email": "test1bg",  # email value is not valid
            "password": "Testpass1!",
            "full_name": "Pol Mol",
        }
        expected_message = {
            "message": "Invalid request: {'email': ['Not a valid email address.']}"
        }
        return TestRegisterSchema.register_user(self, data, expected_message)

    def test_register_schema_invalid_password(self):
        data = {
            "email": "test1@j.bg",
            "password": "test", # password value is not valid
            "full_name": "Pol Mol",
        }
        expected_message = {
            "message": "Invalid request: {'password': ['Not a valid password.']}"
        }
        return TestRegisterSchema.register_user(self, data, expected_message)

    # TODO: test not valid passowrd (separate test for each requirement, not valid full_name

    def test_register_success(self):
        data = {"email": "test1@j.bg", "password": "Testpass1!", "full_name": "Pol Mol"}
        users = User.query.all()
        self.assertEqual(len(users), 0)

        response = self.client.post("/register", json=data)
        self.assertEqual(response.status_code, 201)
        token = response.json["token"]
        self.assertIsNotNone(data)

        users = User.query.all()
        self.assertEqual(len(users), 1)


class TestLoginSchema(APIBaseTestCase):
    def test_login_schema_missing_fields(self):
        data = {}

        response = self.client.post("/login", json=data)
        self.assertEqual(response.status_code, 400)
        expected_message = {
            "message": "Invalid request: {'email': ['Missing data for required field.'], 'password': ['Missing data for required field.']}"
        }
        self.assertEqual(response.json, expected_message)

    def test_login_schema_invalid_email(self):
        data = {
            "email": "test1bg",  # email value is not valid
            "password": "testpass",
            "full_name": "Pol Mol",
        }

        response = self.client.post("/register", json=data)
        self.assertEqual(response.status_code, 400)
        expected_message = {
            "message": "Invalid request: {'email': ['Not a valid email address.']}"
        }
        self.assertEqual(response.json, expected_message)
