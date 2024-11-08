from datetime import datetime, timedelta

import factory

from db import db
from models import User, UserType, UserRole, Booking, BookingStatus


class BaseFactory(factory.Factory):
    @classmethod
    def create(cls, **kwargs):
        object = super().create(**kwargs)
        db.session.add(object)
        db.session.flush()
        return object


class UserFactory(BaseFactory):
    class Meta:
        model = User

    pk = factory.Sequence(lambda n: n)
    email = factory.Faker("email")
    password = factory.Faker("password")
    full_name = factory.Faker("name")
    type = UserType.individual
    role = UserRole.user


class BookingFactory(BaseFactory):
    class Meta:
        model = Booking

    pk = factory.Sequence(lambda n: n)
    status = BookingStatus.in_progress
    created_at = datetime.utcnow()
    last_modified_at = datetime.utcnow() + timedelta(days=1)
    rent_days = factory.Faker("pyint")
    amount = factory.Faker("pyfloat")
    user_pk = 0
    start_date = "2024-11-18"
    end_date = "2024-11-20"
