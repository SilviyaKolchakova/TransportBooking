from resources.auth import RegisterUser, LoginUser
from resources.booking import (
    BookingConfirm,
    BookingCancel,
    PaymentSuccess,
    PaymentFailure,
    BookingsResource,
)
from resources.vehicle import VehiclesResource, VehicleResource

routes = (
    (RegisterUser, "/register"),
    (LoginUser, "/login"),
    (BookingsResource, "/users/bookings"),
    (BookingConfirm, "/bookings/<int:booking_id>/confirm"),
    (BookingCancel, "/bookings/<int:booking_id>/cancel"),
    (VehiclesResource, "/vehicles"),
    (VehicleResource, "/vehicles/<int:vehicle_id>"),
    (PaymentSuccess, "/payment/success/<string:session_id>"),
    (PaymentFailure, "/payment/failure"),
)
