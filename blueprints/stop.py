from flask import jsonify, request, Blueprint
from marshmallow import ValidationError
import pymysql

from db_utils import errors, create_entry, update_entry
from schemas import StopData
from models import Stop
from db_utils import session

stop_blueprint = Blueprint('stop', __name__)
@stop_blueprint.route("/stop", methods=["POST", "GET"])
def stop_():
    if request.method == 'POST':
        json_data = request.json
        if not json_data:
            return errors.bad_request
        try:
            city_data = StopData().load(json_data)
        except (pymysql.Error, pymysql.Warning) as err:
            return err.messages, 422
        except ValidationError as err:
            return err.messages, 422
        new_city = create_entry(Stop, **city_data)
        return jsonify(StopData().dump(new_city))
    if request.method == 'GET':
        city_list = session.query(Stop).all()
        return StopData().dump(city_list, many=True), 200

@stop_blueprint.route('/stop/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def stop_byid(id):
    city = session.query(Stop).filter_by(idchoice=id).first()
    if not city:
        return errors.not_found
    if request.method == 'GET':
        return jsonify(StopData().dump(city))
    if request.method == 'PUT':
        json_data = request.json
        if not json_data:
            return errors.bad_request
        try:
            data = StopData().load(json_data, partial=True)
        except (pymysql.Error, pymysql.Warning) as err:
            return err.messages, 422
        except ValidationError as err:
            return err.messages, 422
        updated_city = update_entry(city, **data)
        return StopData().dump(updated_city)
    if request.method == 'DELETE':
        session.delete(city)
        session.commit()
        return {"message": "Deleted successfully"}, 200