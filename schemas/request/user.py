from marshmallow import Schema, fields


class UserLoginSchema(Schema):
    # TODO: add validation
    email = fields.Email(required=True)
    password = fields.String(required=True)


class UserRegisterSchema(UserLoginSchema):
    full_name = fields.String(required=True)
