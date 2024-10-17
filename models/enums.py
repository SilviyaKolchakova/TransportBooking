import enum


class UserRole(enum.Enum):
    admin = "admin"
    user = "user"


class UserType(enum.Enum):
    business = "business"
    individual = "individual"


class BookingStatus(enum.Enum):
    pending = "pending"
    confirmed = "confirmed"
    canceled = "canceled"


class VehicleType(enum.Enum):
    eight_seats = "8_seats"
    sixteen_seats = "16_seats"
    thirty_seats = "30_seats"
