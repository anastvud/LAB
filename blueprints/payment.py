from flask import jsonify, request, Blueprint
from marshmallow import ValidationError
import pymysql

from db_utils import errors, create_entry, update_entry
from schemas import PaymentData
from models import Payment
from db_utils import session

payment_blueprint = Blueprint('payment', __name__)

@payment_blueprint.route("/payment", methods=["POST", "GET"])
def payment_():
    if request.method == 'POST':
        json_data = request.json
        if not json_data:
            return errors.bad_request
        try:
            payment_data = PaymentData().load(json_data)
        except ValidationError as err:
            return err.messages, 422
        new_payment = create_entry(Payment, **payment_data)
        return jsonify(PaymentData().dump(new_payment))
    if request.method == 'GET':
        payment_list = session.query(Payment).all()
        return PaymentData().dump(payment_list, many=True), 200

@payment_blueprint.route('/payment/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def payment_by_id(id):
    payment = session.query(Payment).filter_by(idpayment=id).first()
    if not payment:
        return errors.not_found
    if request.method == 'GET':
        return jsonify(PaymentData().dump(payment))
    if request.method == 'PUT':
        json_data = request.json
        if not json_data:
            return errors.bad_request
        try:
            data = PaymentData().load(json_data, partial=True)
        except ValidationError as err:
            return err.messages, 422
        updated_payment = update_entry(payment, **data)
        return PaymentData().dump(updated_payment)
    if request.method == 'DELETE':
        try:
            session.delete(payment)
            session.commit()
            return {"message": "Deleted successfully"}, 200
        except pymysql.err.IntegrityError:
            session.rollback()
            return jsonify({"message": "foreign key constraint"}), 400  # just json return
