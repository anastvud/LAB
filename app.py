from flask import Flask
from wsgiref.simple_server import make_server
from route import api_blueprint


app = Flask(__name__)

with make_server('', 5000, app) as server:
    app.register_blueprint(api_blueprint, url_prefix="/api/v1")
    print('working')
    server.serve_forever()
