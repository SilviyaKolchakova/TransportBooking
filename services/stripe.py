import requests

from decouple import config


class StripeService:
    def __init__(self):
        self.api_key = config("STRIPE_API_KEY")
        self.base_url = "https://api.stripe.com/v1"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/x-www-form-urlencoded",
        }

    def create_customer(self, name, email):
        url = f"{self.base_url}/customers"
        data = {"name": name, "email": email}
        response = requests.post(url, headers=self.headers, data=data)
        return response.json()

    def create_checkout_session(
        self, customer_id, amount, currency="usd", booking_id=None
    ):

        url = f"{self.base_url}/checkout/sessions"
        metadata = {}
        if booking_id is not None:
            metadata["booking_id"] = str(booking_id)

        data = {
            "payment_method_types[]": "card",
            "line_items[0][price_data][currency]": currency,
            "line_items[0][price_data][product_data][name]": "Booking Payment",
            "line_items[0][price_data][unit_amount]": amount * 100,
            "line_items[0][quantity]": 1,
            "mode": "payment",
            "success_url": "http://127.0.0.1:5000//payment/success/{CHECKOUT_SESSION_ID}",
            "cancel_url": "http://127.0.0.1:5000//payment/failure",  # TODO:
            "customer": customer_id,
            "metadata[booking_id]": str(booking_id) if booking_id is not None else "",
        }
        response = requests.post(url, headers=self.headers, data=data)

        if response.status_code == 200:

            return response.json()
        else:
            return {"error": response.json()}

    def retrieve_checkout_session(self, session_id):
        url = f"{self.base_url}/checkout/sessions/{session_id}"
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            return response.json()
