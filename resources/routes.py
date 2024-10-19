from resources.auth import RegisterUser, LoginUser
from resources.booking import Booking

routes = (
    (RegisterUser, "/register"),
    (LoginUser, "/login"),
    (Booking, "/users/bookings"),
)
