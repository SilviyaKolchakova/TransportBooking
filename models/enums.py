import enum


class UserRole(enum.Enum):
    admin = "admin"
    user = "user"


class UserType(enum.Enum):
    business = "business"
    individual = "individual"


class BookingStatus(enum.Enum):
    in_progress = "in_progress"
    confirmed = "confirmed"
    canceled = "canceled"
    completed = "completed"
