import json

from flask import jsonify, request, Blueprint, render_template, redirect, url_for
from marshmallow import ValidationError


from db_utils import errors, create_entry, update_entry
from schemas import CityData, CityReq
from models import City
from db_utils import session

city_blueprint = Blueprint('city', __name__)



@city_blueprint.route("/city", methods=["POST", "GET"])
def city_():
    if request.method == 'POST':
        request_data = {
            "name": request.form['name'],
            "country": request.form['country'],
            "foundation_year": int(request.form['year'])
        }
        json_data = json.dumps(request_data)
        print(json_data)
        if not json_data:
            return errors.bad_request
        try:
            subject_data = CityData().loads(json_data)
            print(subject_data)
        except ValidationError as err:
            return err.messages, 422
        new_subject = create_entry(City, **subject_data)
        return jsonify(CityReq().dump(new_subject))

    if request.method == 'GET':
        city_list = session.query(City).all()
        list = CityData().dump(city_list, many=True)
        return render_template("city.html", cities=list)

@city_blueprint.route('/city/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def city_by_id(id):
    city = session.query(City).filter_by(idcity=id).first()
    if not city:
        return errors.not_found
    if request.method == 'GET':
        return jsonify(CityReq().dump(city))
    if request.method == 'PUT':
        json_data = request.json
        if not json_data:
            return errors.bad_request
        try:
            data = CityReq().load(json_data, partial=True)
        except ValidationError as error:
            return error.messages, 422
        updated_city = update_entry(city, **data)
        return CityReq().dump(updated_city)
    if request.method == 'DELETE':
        session.delete(city)
        session.commit()
        return errors.success

def bla():
    pass

@city_blueprint.route('/city/<string:country>', methods=['GET'])
def city_by_country(country):
    city_list = session.query(City).filter_by(country=country).all()
    if not city_list:
        return errors.not_found
    else:
        return jsonify(CityData().dump(city_list, many=True))