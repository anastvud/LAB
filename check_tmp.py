from models import City, User, Hotel, HotelsChoice
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

Session = sessionmaker(bind=create_engine('mysql+pymysql://root:Busy18being@localhost/travelLab', echo=True))
session = Session()

user1 = User(name='John', surname='Brown', passport='PG901234', username='jhnbrwn', password='qwerty123')
user2 = User(name='Walter', surname='White', passport='PD945888', username='wltrwht', password='heisenberg')
city1 = City(name='London', country='England')
hotel1 = Hotel(name='Hilton')

session.add(user1)
session.add(user2)
session.add(city1)
session.add(hotel1)
session.commit()

hotelschoice1 = HotelsChoice(hotel_id=1, city_id=1)
session.add(hotelschoice1)
session.commit()
