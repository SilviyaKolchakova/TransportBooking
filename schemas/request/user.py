import requests
from marshmallow import Schema, fields, ValidationError, validates, validate

from decouple import config


class UserLoginSchema(Schema):
    # TODO: add validation
    email = fields.Email(required=True)
    password = fields.String(required=True)

    @validates("email")
    def validate_email_kickbox(self, email):
        kickbox_api_key = config("KICKBOX_API_KEY")
        response = requests.get(
            f"https://api.kickbox.com/v2/verify?email={email}&apikey={kickbox_api_key}"
        )
        return response.json()


class UserRegisterSchema(UserLoginSchema):
    full_name = fields.String(required=True, validate=validate.Length(min=4, max=50))

    @validates("full_name")
    def validate_full_name(self, value):
        if len(value.split()) < 2:
            raise ValidationError("Full name must be at least 2 characters")
