from lab6.models import City, User, Hotel, HotelsChoice, Payment, Booking, Stop, Transport, Trip
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import date

Session = sessionmaker(bind=create_engine('mysql+pymysql://root:Busy18being@localhost/travelLab', echo=True))
session = Session()

# user1 = User(name='John', surname='Brown', passport='PG901234', username='jhnbrwn', password='qwerty123')
# user2 = User(name='Walter', surname='White', passport='PD945888', username='wltrwht', password='heisenberg')
# city1 = City(name='London', country='England')
# city2 = City(name='Manchester', country='England')
# hotel1 = Hotel(name='Hilton')
# hotel2 = Hotel(name='Four Seasons')
# payment1 = Payment(name='cash')
# payment2 = Payment(name='card')
transport1 = Transport(name='plane')
transport2 = Transport(name='bus')
#
#
# session.add(user1)
# session.add(user2)
# session.add(city1)
# session.add(city2)
# session.add(hotel1)
# session.add(transport1)
# session.add(transport2)
# session.add(hotel2)
# session.commit()
#
# trip1 = Trip(days=6, start_date=date(2020,9,8), transport_id=1)
# trip2 = Trip(days=2, start_date=date(2021,9,8), transport_id=2)
#
# session.add(trip1)
# session.add(trip2)
# session.commit()
#
stop1 = Stop(trip_id=5, city_id=1)
stop2 = Stop(trip_id=4, city_id=2)
booking1 = Booking(client_id=1, trip_id=4, payment_id=1)
booking2 = Booking(client_id=2, trip_id=5, payment_id=2)


hotelschoice1 = HotelsChoice(hotel_id=1, city_id=1)
hotelschoice2 = HotelsChoice(hotel_id=2, city_id=1)
session.add(hotelschoice1)
session.add(hotelschoice2)


session.add(stop1)
session.add(stop2)
session.add(booking1)
session.add(booking2)

session.commit()
