from models import City, User, Hotel, HotelsChoice
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import schemas, models
import pymysql
from flask import Blueprint, jsonify, request
from marshmallow import ValidationError
import db_utils
from db_utils import errors
import schemas
import models
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

api_blueprint = Blueprint('api', __name__)

engine = create_engine('mysql+pymysql://root:Busy18being@localhost/travel_agency', echo=True)
Session = sessionmaker(bind=engine)
session = Session()

import pandas as pd

# user_table = pd.read_sql_table(table_name="City", con=engine)
# def c():
#     city_list = session.query(models.City).all()
#     return list(schemas.CityData().dump(city_list, many=True))

# session.commit()




@api_blueprint.route("/test", methods=["GET"])
def city_____():
    city_list = session.query(models.City).all()
    return schemas.CityData().dump(city_list, many=True), 200

