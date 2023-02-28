from sqlalchemy import Table, Column, String, Integer, Date, Boolean, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

from db_utils import session

base = declarative_base()

class City (base):
    __tablename__ = 'City'
    idcity = Column(Integer, primary_key=True, unique=True, nullable=False, autoincrement=True)
    name = Column(String(15), unique=True, nullable=False)
    foundation_year = Column(Integer, nullable=False)
    country = Column(String(15), nullable=False)

class User(base):
    __tablename__ = 'User'
    iduser = Column(Integer, primary_key=True, unique=True, nullable=False, autoincrement=True)
    name = Column(String(25), nullable=False)
    surname = Column(String(25), nullable=False)
    email = Column(String(25), nullable=False, unique=True)
    number = Column(String(15), nullable=False)
    passport = Column(String(15), nullable=False)
    username = Column(String(20), nullable=False, unique=True)
    password = Column(String(90), nullable=False)

class Transport(base):
    __tablename__ = 'Transport'
    idtransport = Column(Integer, primary_key=True, unique=True, nullable=False, autoincrement=True)
    name = Column(String(15), nullable=False)
    rating = Column(Float, nullable=False)


class Trip(base):
    __tablename__ = 'Trip'
    idtrip = Column(Integer, primary_key=True, unique=True, nullable=False, autoincrement=True)
    price = Column(Float, nullable=False)
    days = Column(Integer, nullable=False)
    start_date = Column(Date, nullable=False)

    transport_id = Column(Integer, ForeignKey(Transport.idtransport), nullable=False)
    transport = relationship('Transport', foreign_keys='Trip.transport_id')

class Hotel(base):
    __tablename__ = 'Hotel'
    idhotel = Column(Integer, primary_key=True, unique=True, nullable=False, autoincrement=True)
    name = Column(String(15), nullable=False)
    rating = Column(Float, nullable=False)
    price = Column(Float, nullable=False)
    breaksfast = Column(Boolean, nullable=False)

    city_id = Column(Integer, ForeignKey(City.idcity), nullable=False)
    city = relationship('City', foreign_keys='Hotel.city_id')

class Payment(base):
    __tablename__ = 'Payment'
    idpayment = Column(Integer, primary_key=True, unique=True, nullable=False, autoincrement=True)
    name = Column(String(15), nullable=False)

class Booking(base):
    __tablename__ = 'Booking'
    idbooking = Column(Integer, primary_key=True, autoincrement=True)
    client_id = Column(Integer, ForeignKey(User.iduser), nullable=False)
    trip_id = Column(Integer, ForeignKey(Trip.idtrip), nullable=False)
    payment_id = Column(Integer, ForeignKey(Payment.idpayment), nullable=False)

    client = relationship('User', foreign_keys='Booking.client_id')
    trip = relationship('Trip', foreign_keys='Booking.trip_id')
    payment = relationship('Payment', foreign_keys='Booking.payment_id')

class Stop(base):
    __tablename__ = 'Stop'
    idstop = Column(Integer, primary_key=True, autoincrement=True)
    trip_id = Column(Integer, ForeignKey(Trip.idtrip), nullable=False)
    city_id = Column(Integer, ForeignKey(City.idcity), nullable=False)
    hotel_id = Column(Integer, ForeignKey(Hotel.idhotel), nullable=False)

    trip = relationship('Trip', foreign_keys='Stop.trip_id')
    city = relationship('City', foreign_keys='Stop.city_id')
    hotel = relationship('Hotel', foreign_keys='Stop.hotel_id')

class HotelsChoice(base):
    __tablename__ = 'HotelsChoice'
    idchoice = Column(Integer, primary_key=True)
    hotel_id = Column(Integer, ForeignKey(Hotel.idhotel), nullable=False)
    city_id = Column(Integer, ForeignKey(City.idcity), nullable=False)

    hotel = relationship('Hotel', foreign_keys='HotelsChoice.hotel_id')
    city = relationship('City', foreign_keys='HotelsChoice.city_id')
