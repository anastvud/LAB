from flask import jsonify, request, Blueprint
from marshmallow import ValidationError
import pymysql

from db_utils import errors, create_entry, update_entry
from schemas import TripData
from models import Trip
from db_utils import session

trip_blueprint = Blueprint('trip', __name__)

@trip_blueprint.route("/trip", methods=["POST", "GET"])
def trip_():
    if request.method == 'POST':
        json_data = request.json
        if not json_data:
            return errors.bad_request
        try:
            trip_data = TripData().load(json_data)
        except ValidationError as err:
            return err.messages, 422
        new_trip = create_entry(Trip, **trip_data)
        return jsonify(TripData().dump(new_trip))
    if request.method == 'GET':
        trip_data = session.query(Trip).all()
        return TripData().dump(trip_data, many=True), 200

@trip_blueprint.route('/trip/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def trip_by_id(id):
    trip = session.query(Trip).filter_by(idtrip=id).first()
    if not trip:
        return errors.not_found
    if request.method == 'GET':
        return jsonify(TripData().dump(trip))
    if request.method == 'PUT':
        json_data = request.json
        if not json_data:
            return errors.bad_request
        try:
            data = TripData().load(json_data, partial=True)
        except ValidationError as err:
            return err.messages, 422
        updated_trip = update_entry(trip, **data)
        return TripData().dump(updated_trip)
    if request.method == 'DELETE':
        try:
            session.delete(trip)
            session.commit()
            return {"message": "Deleted successfully"}, 200
        except pymysql.err.IntegrityError:
            session.rollback()
            return jsonify({"message": "foreign key constraint"}), 400  # just json return
