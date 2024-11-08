import requests
from marshmallow import Schema, fields, ValidationError, validates, validate

from decouple import config


class UserLoginSchema(Schema):
    # TODO: add validation
    email = fields.Email(required=True)
    password = fields.String(required=True)

    @validates("email")
    def validate_email_with_kickbox(self, email):
        api_key = config("KICKBOX_API_KEY")
        url = f"https://api.kickbox.com/v2/verify?email={email}&apikey={api_key}"

        response = requests.get(url)
        result = response.json()

        if result.get("result") != "deliverable":
            raise ValidationError("Invalid or undeliverable email address.")

    @validates("password")
    def validate_password(self, password):
        if len(password) < 8:
            raise ValidationError("Password must be at least 8 characters long.")

        has_upper = False
        has_lower = False
        has_digit = False
        has_special = False
        special_characters = "!@#$%^&*()-_+=<>?{}[]|\\/:;\"'.,"

        for char in password:
            if char.isupper():
                has_upper = True
            elif char.islower():
                has_lower = True
            elif char.isdigit():
                has_digit = True
            elif char in special_characters:
                has_special = True

        if not has_upper:
            raise ValidationError(
                "Password must contain at least one uppercase letter."
            )
        if not has_lower:
            raise ValidationError(
                "Password must contain at least one lowercase letter."
            )
        if not has_digit:
            raise ValidationError("Password must contain at least one digit.")
        if not has_special:
            raise ValidationError(
                "Password must contain at least one special character."
            )


class UserRegisterSchema(UserLoginSchema):
    full_name = fields.String(required=True, validate=validate.Length(min=4, max=50))

    @validates("full_name")
    def validate_full_name(self, value):
        # TODO: validate value contains only alpha characters

        if len(value.split()) < 2:
            raise ValidationError("Full name must be at least 2 characters")
