from marshmallow import fields, Schema, validate
from datetime import date
from flask_bcrypt import generate_password_hash

class CityData(Schema):
    name = fields.String()
    foundation_year = fields.Integer()
    country = fields.String()

class UserData(Schema):
    name = fields.String()
    surname = fields.String()
    email = fields.String()

class UserSchema(Schema):
    idclient = fields.Integer()
    name = fields.String()
    surname = fields.String()
    email = fields.String()
    number = fields.String()
    passport = fields.String()
    username = fields.String()
    password = fields.Function(
        deserialize=lambda obj: generate_password_hash(obj), load_only=True
    )

class TransportData(Schema):
    name = fields.String()
    rating = fields.Float()

class TripData(Schema):
    price = fields.Integer()
    days = fields.Integer()
    start_date = fields.Date()
    transport_id = fields.Integer()

class HotelData(Schema):
    name = fields.String()
    rating = fields.Float()
    price = fields.Integer()
    breakfast = fields.Boolean()
    city_id = fields.Integer()

class PaymentData(Schema):
    name = fields.String()

class BookingData(Schema):
    idbooking = fields.Integer()
    client_id = fields.Integer()
    trip_id = fields.Integer()
    payment_id = fields.Integer()

class StopData(Schema):
    idstop = fields.Integer()
    city_id = fields.Integer()
    trip_id = fields.Integer()
    hotel_id = fields.Integer()

class HotelsChoiceData(Schema):
    idchoice = fields.Integer()
    hotel_id = fields.Integer()
    city_id = fields.Integer()

# class HotelsChoiceReq(Schema):
#     hotel_id = fields.Integer()
#     city_id = fields.Integer()


