from marshmallow import Schema, fields, validate

class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True, validate=validate.Length(min=4, max=80))
    password = fields.Str(load_only=True, required=True, validate=validate.Length(min=6))

class TaskSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str(required=True, validate=validate.Length(min=1, max=120))
    description = fields.Str(validate=validate.Length(max=200))
    done = fields.Bool()
    user_id = fields.Int(dump_only=True)
