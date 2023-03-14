from flask import Flask
from wsgiref.simple_server import make_server
from route import api_blueprint
from blueprints.city import city_blueprint
from blueprints.trasnport import transport_blueprint


app = Flask(__name__)

with make_server('', 5000, app) as server:
    app.register_blueprint(api_blueprint, url_prefix="/api/v1")
    app.register_blueprint(city_blueprint, url_prefix="/api/v1")
    app.register_blueprint(transport_blueprint, url_prefix="/api/v1")
    print('working')
    server.serve_forever()
