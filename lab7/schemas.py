from marshmallow import fields, Schema, validate
from datetime import date
from flask_bcrypt import generate_password_hash


class CityData(Schema):
    idcity = fields.Integer()
    name = fields.String()
    country = fields.String()

class CityReq(Schema):
    name = fields.String()
    country = fields.String()

class HotelData(Schema):
    idhotel = fields.Integer()
    name = fields.String()

class HotelsChoiceData(Schema):
    idchoice = fields.Integer()
    hotel_id = fields.Integer()
    city_id = fields.Integer()

class HotelsChoiceReq(Schema):
    hotel_id = fields.Integer()
    city_id = fields.Integer()

class UserData(Schema):
    name = fields.String()
    surname = fields.String()
    username = fields.String()
    passport = fields.String()



class UserSchema(Schema):
    iduser = fields.Integer()
    username = fields.String()
    password = fields.Function(
        deserialize=lambda obj: generate_password_hash(obj), load_only=True
    )
    name = fields.String()
    surname = fields.String()
    passport = fields.String()
