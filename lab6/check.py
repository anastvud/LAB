from lab6.models import City, User, Hotel, HotelsChoice
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

Session = sessionmaker(bind=create_engine('mysql+pymysql://root:Busy18being@localhost/travelLab', echo=True))
session = Session()

user1 = User(1, 'John', 'Brown', 'PG901234', 'jhnbrwn', 'qwerty123')
user2 = User(2, 'Walter', 'White', 'PD945888', 'wltrwht', 'heisenberg')
city1 = City(1, 'London', 'England')
hotel1 = Hotel(1, 'Hilton')

session.add(user1)
session.add(user2)
session.add(city1)
session.add(hotel1)
session.commit()

hotelschoice1 = HotelsChoice(1, 1, 1)
session.add(hotelschoice1)
session.commit()
