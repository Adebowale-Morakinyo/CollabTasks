from marshmallow import Schema, fields


class UserSchema(Schema):
    id = fields.Int()
    username = fields.Str()
    password = fields.Str(load_only=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)


class UserLoginResponseSchema(Schema):
    access_token = fields.Str()
    refresh_token = fields.Str()


class TokenRefreshResponseSchema(Schema):
    access_token = fields.Str()


class TaskSchema(Schema):
    id = fields.Int()
    title = fields.Str(required=True)
    description = fields.Str()
    priority = fields.Int()
    user_id = fields.Int(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
