from resources.auth import RegisterUser, LoginUser
from resources.booking import Booking, BookingConfirm, BookingCancel

routes = (
    (RegisterUser, "/register"),
    (LoginUser, "/login"),
    (Booking, "/users/bookings"),
    (BookingConfirm, "/bookings/<int:booking_id>/confirm"),
    (BookingCancel, "/bookings/<int:booking_id>/cancel"),
)
