from datetime import datetime
from unittest.mock import patch

from constants import RENT_PRICE_PER_DAY
from managers.user import UserManager
from models import Booking

from tests import UserFactory
from tests.base import APIBaseTestCase, generate_token, get_session_id, create_booking


class TestBooking(APIBaseTestCase):
    url = "/users/bookings"

    def test_booking_missing_input_fields_raises(self):
        data = {}
        expected_message = {
            "message": "Invalid request: {'start_date': ['Missing data for required field.'], "
            "'end_date': ['Missing data for required field.']}"
        }
        return create_booking(self, data, expected_message)

    def test_booking_missing_start_date_raises(self):
        data = {
            # "start_date": "2024-11-13",
            "end_date": "2024-11-14"
        }
        expected_message = {
            "message": "Invalid request: {'start_date': ['Missing data for required field.']}"
        }
        return create_booking(self, data, expected_message)

    def test_booking_missing_end_date_raises(self):
        data = {
            "start_date": "2024-11-13",
            # "end_date": "2024-11-14"
        }
        expected_message = {
            "message": "Invalid request: {'end_date': ['Missing data for required field.']}"
        }
        return create_booking(self, data, expected_message)

    def test_booking_invalid_start_date_raises(self):
        data = {"start_date": "2024-11-08", "end_date": "2024-11-14"}
        expected_message = {
            "message": "Invalid request: {'start_date': ['Start date must be at least 3 "
            "days in the future.']}"
        }
        return create_booking(self, data, expected_message)

    def test_booking_invalid_end_date_raises(self):
        data = {"start_date": "2024-11-12", "end_date": "2024-11-11"}
        expected_message = {
            "message": "Invalid request: {'_schema': ['End date must be after the start date.']}"
        }
        return create_booking(self, data, expected_message)

    @patch.object(UserManager, "retrieve_booking", return_value=None)
    @patch.object(UserManager, "pay_booking", return_value="stripe.payments.url")
    def test_create_booking(self, mock_payment, mock_retrieve_booking):

        user = UserFactory()
        token = generate_token(user)

        bookings = Booking.query.all()
        self.assertEqual(len(bookings), 0)
        data = {
            "start_date": "2024-11-15",
            "end_date": "2024-11-18",
        }

        response = self.client.post(
            self.url,
            json=data,
            headers={
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json",
            },
        )
        self.assertEqual(response.status_code, 200)

        start_date = datetime.strptime(data["start_date"], "%Y-%m-%d")
        end_date = datetime.strptime(data["end_date"], "%Y-%m-%d")
        data["rent_days"] = (end_date - start_date).days + 1
        data["amount"] = data["rent_days"] * RENT_PRICE_PER_DAY

        bookings = Booking.query.all()
        self.assertEqual(len(bookings), 1)
        booking = bookings[0]

        self.assertEqual(booking.amount, data["amount"])
        self.assertEqual(booking.rent_days, data["rent_days"])
        self.assertEqual(booking.is_paid, False)

        mock_payment.assert_called_once_with(booking, user.full_name, user.email)

        payment_url = f"/payment/success/{get_session_id()}"

        response = self.client.get(payment_url)
        expected_message = {
            "message": f"Payment successful for session ID {get_session_id()}"
        }
        self.assertEqual(response.json, expected_message)
        booking.is_paid = True
        self.assertEqual(booking.is_paid, True)

        mock_retrieve_booking.assert_called_once_with(get_session_id())
