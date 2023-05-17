from marshmallow import Schema, fields


class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True)
    password = fields.Str(required=True, load_only=True)
    email = fields.Str(required=True)
    
class UserLoginSchema(Schema):
    username = fields.Str(required=True)
    password = fields.Str(required=True, load_only=True)

class UserUpdateSchema(Schema):
    username = fields.Str()
    email = fields.Str()
    password = fields.Str(load_only=True)
    
class ActiveSchema(Schema):
    id = fields.Int(dump_only=True)
    user_id = fields.Int(required=True)
    date = fields.DateTime(format='%Y-%m-%d')
    time = fields.Float()
    distance = fields.Float()
    speed = fields.Float()

class UpdateActiveSchema(Schema):
    user_id = fields.Int(required=True)
    distance = fields.Float(required=True)
    
    
    
class LocationSchema(Schema):
    id = fields.Int(dump_only=True)
    active_id = fields.Int(required=True)
    latitude = fields.Float(required=True)
    longitude = fields.Float(required=True)
    time = fields.DateTime(format='%Y-%m-%d', required=True)
    
# class AddLocationSchema(Schema):
#     active_id = fields.Int(required=True)
#     latitude = fields.Float(required=True)
#     distance = fields.Float(required=True)
#     time = fields.DateTime(required=True)
    
    