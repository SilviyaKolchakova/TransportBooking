from resources.auth import RegisterUser, LoginUser
from resources.booking import (
    BookingConfirm,
    BookingCancel,
    PaymentSuccess,
    PaymentFailure,
    BookingResource,
)
from resources.test_redirect import ExampleResource

routes = (
    (RegisterUser, "/register"),
    (LoginUser, "/login"),
    (BookingResource, "/users/bookings"),
    (BookingConfirm, "/bookings/<int:booking_id>/confirm"),
    (BookingCancel, "/bookings/<int:booking_id>/cancel"),
    (ExampleResource, "/example"),
    (PaymentSuccess, "/payment/success/<string:session_id>"),
    (PaymentFailure, "/payment/failure"),
)
