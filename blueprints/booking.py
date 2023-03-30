from flask import jsonify, request, Blueprint
from marshmallow import ValidationError
import pymysql

from db_utils import errors, create_entry, update_entry
from schemas import BookingData
from models import Booking
from db_utils import session

booking_blueprint = Blueprint('booking', __name__)
@booking_blueprint.route("/booking", methods=["POST", "GET"])
def booking_():
    if request.method == 'POST':
        json_data = request.json
        if not json_data:
            return errors.bad_request
        try:
            city_data = BookingData().load(json_data)
        except (pymysql.Error, pymysql.Warning) as err:
            return err.messages, 422
        except ValidationError as err:
            return err.messages, 422
        new_city = create_entry(Booking, **city_data)
        return jsonify(BookingData().dump(new_city))
    if request.method == 'GET':
        city_list = session.query(Booking).all()
        return BookingData().dump(city_list, many=True), 200

@booking_blueprint.route('/booking/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def booking_byid(id):
    city = session.query(Booking).filter_by(idchoice=id).first()
    if not city:
        return errors.not_found
    if request.method == 'GET':
        return jsonify(BookingData().dump(city))
    if request.method == 'PUT':
        json_data = request.json
        if not json_data:
            return errors.bad_request
        try:
            data = BookingData().load(json_data, partial=True)
        except (pymysql.Error, pymysql.Warning) as err:
            return err.messages, 422
        except ValidationError as err:
            return err.messages, 422
        updated_city = update_entry(city, **data)
        return BookingData().dump(updated_city)
    if request.method == 'DELETE':
        session.delete(city)
        session.commit()
        return {"message": "Deleted successfully"}, 200