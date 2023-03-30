from flask import jsonify, request, Blueprint
from marshmallow import ValidationError
import pymysql

from db_utils import errors, create_entry, update_entry
from schemas import HotelData
from models import Hotel
from db_utils import session

hotel_blueprint = Blueprint('hotel', __name__)
@hotel_blueprint.route("/hotel", methods=["POST", "GET"])
def hotel_():
    if request.method == 'POST':
        json_data = request.json
        if not json_data:
            return errors.bad_request
        try:
            city_data = HotelData().load(json_data)
        except (pymysql.Error, pymysql.Warning) as err:
            return err.messages, 422
        except ValidationError as err:
            return err.messages, 422
        new_city = create_entry(Hotel, **city_data)
        return jsonify(HotelData().dump(new_city))
    if request.method == 'GET':
        city_list = session.query(Hotel).all()
        return HotelData().dump(city_list, many=True), 200

@hotel_blueprint.route('/hotel/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def hotel_byid(id):
    city = session.query(Hotel).filter_by(idhotel=id).first()
    if not city:
        return errors.not_found
    if request.method == 'GET':
        return jsonify(HotelData().dump(city))
    if request.method == 'PUT':
        json_data = request.json
        if not json_data:
            return errors.bad_request
        try:
            data = HotelData().load(json_data, partial=True)
        except (pymysql.Error, pymysql.Warning) as err:
            return err.messages, 422
        except ValidationError as err:
            return err.messages, 422
        updated_city = update_entry(city, **data)
        return HotelData().dump(updated_city)
    if request.method == 'DELETE':
        try:
            session.delete(city)
            session.commit()
        except pymysql.err.IntegrityError:
            session.rollback()
            return jsonify({"message": "foreign key constraint"}), 400  # just json return

        return {"message": "Deleted successfully"}, 200