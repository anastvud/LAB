from flask import jsonify, request, Blueprint
from marshmallow import ValidationError
import pymysql

from db_utils import errors, create_entry, update_entry
from schemas import TransportData
from models import Transport
from db_utils import session

transport_blueprint = Blueprint('transport', __name__)

@transport_blueprint.route("/transport", methods=["POST", "GET"])
def transport_():
    if request.method == 'POST':
        json_data = request.json
        if not json_data:
            return errors.bad_request
        try:
            transport_data = TransportData().load(json_data)
        except ValidationError as err:
            return err.messages, 422
        new_transport = create_entry(Transport, **transport_data)
        return jsonify(TransportData().dump(new_transport))
    if request.method == 'GET':
        trasnport_list = session.query(Transport).all()
        return TransportData().dump(trasnport_list, many=True), 200

@transport_blueprint.route('/transport/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def transport_by_id(id):
    transport = session.query(Transport).filter_by(idtransport=id).first()
    if not transport:
        return errors.not_found
    if request.method == 'GET':
        return jsonify(TransportData().dump(transport))
    if request.method == 'PUT':
        json_data = request.json
        if not json_data:
            return errors.bad_request
        try:
            data = TransportData().load(json_data, partial=True)
        except ValidationError as err:
            return err.messages, 422
        updated_transport = update_entry(transport, **data)
        return TransportData().dump(updated_transport)
    if request.method == 'DELETE':
        try:
            session.delete(transport)
            session.commit()
            return {"message": "Deleted successfully"}, 200
        except pymysql.err.IntegrityError:
            session.rollback()
            return jsonify({"message": "foreign key constraint"}), 400  # just json return
