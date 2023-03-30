from flask import Flask
from wsgiref.simple_server import make_server
from blueprints.city import city_blueprint
from blueprints.transport import transport_blueprint
from blueprints.payment import payment_blueprint
from blueprints.trip import trip_blueprint
from blueprints.hotel import hotel_blueprint
from blueprints.booking import booking_blueprint
from blueprints.stop import stop_blueprint
from blueprints.hotelschoice import hotelschoice_blueprint
from blueprints.user import user_blueprint


app = Flask(__name__)

with make_server('', 5000, app) as server:
    app.register_blueprint(city_blueprint, url_prefix="/api/v1")
    app.register_blueprint(transport_blueprint, url_prefix="/api/v1")
    app.register_blueprint(payment_blueprint, url_prefix="/api/v1")
    app.register_blueprint(trip_blueprint, url_prefix="/api/v1")
    app.register_blueprint(hotel_blueprint, url_prefix="/api/v1")
    app.register_blueprint(booking_blueprint, url_prefix="/api/v1")
    app.register_blueprint(stop_blueprint, url_prefix="/api/v1")
    app.register_blueprint(hotelschoice_blueprint, url_prefix="/api/v1")
    app.register_blueprint(user_blueprint, url_prefix="/api/v1")
    print('working')
    server.serve_forever()
