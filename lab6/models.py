from sqlalchemy import create_engine
from sqlalchemy import Column, String, Integer, Date, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

#

engine = create_engine('mysql+pymysql://root:Busy18being@localhost/travelLab', echo=True)

base = declarative_base()

class City (base):
    __tablename__ = 'City'
    idcity = Column(Integer, primary_key=True)
    name = Column(String(15))
    country = Column(String(15))

    def __init__(self, idcity, name, country):
        self.idcity = idcity
        self.name = name
        self.country = country

class User(base):
    __tablename__ = 'User'
    iduser = Column(Integer, primary_key=True)
    name = Column(String(15))
    surname = Column(String(15))
    passport = Column(String(10))
    username = Column(String(20))
    password = Column(String(20))


    def __init__(self, iduser, name, surname, passport, username, password):
        self.iduser = iduser
        self.name = name
        self.surname = surname
        self.passport = passport
        self.username = username
        self.password = password

class Transport(base):
    __tablename__ = 'Transport'
    idtransport = Column(Integer, primary_key=True)
    name = Column(String(15))


    def __init__(self, idtransport, name):
        self.idtransport = idtransport
        self.name = name

class Trip(base):
    __tablename__ = 'Trip'
    idtrip = Column(Integer, primary_key=True)
    days = Column(Integer)
    start_date = Column(Date)
    transport_id = Column(Integer, ForeignKey(Transport.idtransport))
    transport = relationship('Transport', foreign_keys='Trip.transport_id')

    def __init__(self, idtrip, days, start_date, transport_id):
        self.idtrip = idtrip
        self.days = days
        self.start_date = start_date
        self.transport_id = transport_id

class Hotel(base):
    __tablename__ = 'Hotel'
    idhotel = Column(Integer, primary_key=True)
    name = Column(String(15))

    def __init__(self, idhotel, name):
        self.idhotel = idhotel
        self.name = name

class Payment(base):
    __tablename__ = 'Payment'
    idpayment = Column(Integer, primary_key=True)
    name = Column(String(15))

    def __init__(self, idpayment, name):
        self.idpayment = idpayment
        self.name = name


class Booking(base):
    __tablename__ = 'Booking'
    idbooking = Column(Integer, primary_key=True)
    client_id = Column(Integer, ForeignKey(User.iduser))
    trip_id = Column(Integer, ForeignKey(Trip.idtrip))
    payment_id = Column(Integer, ForeignKey(Payment.idpayment))


    client = relationship('User', foreign_keys='Booking.client_id')
    trip = relationship('Trip', foreign_keys='Booking.trip_id')
    payment = relationship('Payment', foreign_keys='Booking.payment_id')


    def __init__(self, idbooking, client_id, trip_id, payment_id):
        self.idbooking = idbooking
        self.client_id = client_id
        self.trip_id = trip_id
        self.payment_id = payment_id

class Stop(base):
    __tablename__ = 'Stop'
    idstop = Column(Integer, primary_key=True)
    trip_id = Column(Integer, ForeignKey(Trip.idtrip))
    city_id = Column(Integer, ForeignKey(City.idcity))

    trip = relationship('Trip', foreign_keys='Stop.trip_id')
    city = relationship('City', foreign_keys='Stop.city_id')


    def __init__(self, idstop, client_id, trip_id, payment_id):
        idstop = idstop
        self.client_id = client_id
        self.trip_id = trip_id
        self.payment_id = payment_id

class HotelsChoice(base):
    __tablename__ = 'HotelsChoice'
    idchoice = Column(Integer, primary_key=True)
    hotel_id = Column(Integer, ForeignKey(Hotel.idhotel))
    city_id = Column(Integer, ForeignKey(City.idcity))

    hotel = relationship('Hotel', foreign_keys='HotelsChoice.hotel_id')
    city = relationship('City', foreign_keys='HotelsChoice.city_id')


    def __init__(self, idchoice, hotel_id, city_id):
        idchoice = idchoice
        self.hotel_id = hotel_id
        self.city_id = city_id


base.metadata.create_all(engine)