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

Session = sessionmaker(bind=create_engine('mysql+pymysql://root:Busy18being@localhost/travel_agency', echo=True))
session = Session()









### hotels choice
@api_blueprint.route("/hotelschoice", methods=["POST", "GET"])
def hotelschoice_():
    if request.method == 'POST':
        json_data = request.json
        if not json_data:
            return errors.bad_request
        try:
            city_data = schemas.HotelsChoiceData().load(json_data)
        except (pymysql.Error, pymysql.Warning) as err:
            return err.messages, 422
        except ValidationError as err:
            return err.messages, 422
        new_city = db_utils.create_entry(models.HotelsChoice, **city_data)
        return jsonify(schemas.HotelsChoiceData().dump(new_city))
    if request.method == 'GET':
        city_list = session.query(models.HotelsChoice).all()
        return schemas.HotelsChoiceData().dump(city_list, many=True), 200

@api_blueprint.route('/hotelschoice/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def hotelschoice_byid(id):
    city = session.query(models.HotelsChoice).filter_by(idchoice=id).first()
    if not city:
        return errors.not_found
    if request.method == 'GET':
        return jsonify(schemas.HotelsChoiceData().dump(city))
    if request.method == 'PUT':
        json_data = request.json
        if not json_data:
            return db_utils.errors.bad_request
        try:
            data = schemas.HotelsChoiceData().load(json_data, partial=True)
        except (pymysql.Error, pymysql.Warning) as err:
            return err.messages, 422
        except ValidationError as err:
            return err.messages, 422
        updated_city = db_utils.update_entry(city, **data)
        return schemas.HotelsChoiceData().dump(updated_city)
    if request.method == 'DELETE':
        session.delete(city)
        session.commit()
        return {"message": "Deleted successfully"}, 200


### user
@api_blueprint.route("/user", methods=["POST", "GET"])
def create_user():
    if request.method == "POST":
        json_data = request.json
        if not json_data:
            return errors.bad_request
        try:
            user_data = schemas.UserSchema().load(json_data)
        except ValidationError as err:
            return err.messages, 422
        user = session.query(models.User).filter_by(username=user_data["username"]).first()
        if user:
            return errors.exists
        user = db_utils.create_entry(models.User, **user_data)
        return jsonify(schemas.UserData().dump(user)), 200
    if request.method == "GET":
        users_list = session.query(models.User).all()
        return schemas.UserData().dump(users_list, many=True), 200

# @api_blueprint.route('/user/login', methods=['GET'])
# def login():
#     json_data = request.json
#     if not json_data:
#         return errors.bad_request
#     try:
#         data = schemas.UserSchema().load(json_data, partial=True)
#     except ValidationError as err:
#         return err.messages, 422
#     user = session.query(models.User).filter_by(username=data["username"]).first()
#     if not user:
#         return errors.not_found
#     if data['password'] == user.password:
#         return {"message": "Successfully logged in"}, 200
#     else:
#         return {'error': {'code': 400, 'message': 'Incorrect password'}}, 400

@api_blueprint.route('/user/<string:username>', methods=['GET', 'PUT', 'DELETE'])
def user_username_api(username):
    user = session.query(models.User).filter_by(username=username).first()
    if not user:
        return errors.not_found
    if request.method == 'GET':
        return schemas.UserData().dump(user), 200
    if request.method == 'PUT':
        json_data = request.json
        if not json_data:
            return errors.bad_request
        try:
            data = schemas.UserSchema().load(json_data, partial=True)
        except "ValidationError" as err:
            return err.messages, 422
        for key, value in data.items():
            if key == "username":
                us = session.query(models.User).filter_by(username=data["username"]).first()
                if us:
                    return errors.exists
        updated_user = db_utils.update_entry(user, **data)
        for key, value in data.items():
            if key == "password" and len(data) == 1:
                return {"message": "Password changed successfully"}, 200
        return schemas.UserData().dump(updated_user), 200
    if request.method == 'DELETE':
        session.delete(user)
        session.commit()
        return {"message": "Deleted successfully"}, 200