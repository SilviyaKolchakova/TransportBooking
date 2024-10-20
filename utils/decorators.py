from flask import request
from marshmallow import Schema
from werkzeug.exceptions import Forbidden, BadRequest

from managers.auth import auth


def permission_required(required_role):
    def decorator(func):
        def wrapper(*args, **kwargs):
            current_user = auth.current_user()

            if current_user.role != required_role:
                raise Forbidden("You do not have access to this resource")
            return func(*args, **kwargs)

        return wrapper

    return decorator


def validate_schema(schema):
    def decorator(func):
        def wrapper(*args, **kwargs):
            current_schema: Schema = schema()
            data = request.get_json()
            errors = current_schema.validate(data)
            if errors:
                raise BadRequest(f"Invalid request: {errors}")
            return func(*args, **kwargs)

        return wrapper

    return decorator
