import factory

from db import db
from models import User, UserType, UserRole


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
