from flask import jsonify, request, Blueprint
from marshmallow import ValidationError
import pymysql

from db_utils import errors, create_entry, update_entry
from schemas import HotelsChoiceData
from models import HotelsChoice
from db_utils import session

hotelschoice_blueprint = Blueprint('hotelschoice', __name__)
@hotelschoice_blueprint.route("/hotelschoice", methods=["POST", "GET"])
def hotelschoice_():
    if request.method == 'POST':
        json_data = request.json
        if not json_data:
            return errors.bad_request
        try:
            city_data = HotelsChoiceData().load(json_data)
        except (pymysql.Error, pymysql.Warning) as err:
            return err.messages, 422
        except ValidationError as err:
            return err.messages, 422
        new_city = create_entry(HotelsChoice, **city_data)
        return jsonify(HotelsChoiceData().dump(new_city))
    if request.method == 'GET':
        city_list = session.query(HotelsChoice).all()
        return HotelsChoiceData().dump(city_list, many=True), 200

@hotelschoice_blueprint.route('/hotelschoice/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def hotelschoice_byid(id):
    city = session.query(HotelsChoice).filter_by(idchoice=id).first()
    if not city:
        return errors.not_found
    if request.method == 'GET':
        return jsonify(HotelsChoiceData().dump(city))
    if request.method == 'PUT':
        json_data = request.json
        if not json_data:
            return errors.bad_request
        try:
            data = HotelsChoiceData().load(json_data, partial=True)
        except (pymysql.Error, pymysql.Warning) as err:
            return err.messages, 422
        except ValidationError as err:
            return err.messages, 422
        updated_city = update_entry(city, **data)
        return HotelsChoiceData().dump(updated_city)
    if request.method == 'DELETE':
        session.delete(city)
        session.commit()
        return {"message": "Deleted successfully"}, 200