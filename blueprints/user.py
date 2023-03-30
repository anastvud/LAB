from flask import jsonify, request, Blueprint
from marshmallow import ValidationError

from db_utils import errors, create_entry, update_entry
from schemas import UserSchema, UserData
from models import User
from db_utils import session

user_blueprint = Blueprint('user', __name__)
@user_blueprint.route("/user", methods=["POST", "GET"])
def create_user():
    if request.method == "POST":
        json_data = request.json
        if not json_data:
            return errors.bad_request
        try:
            user_data = UserSchema().load(json_data)
        except ValidationError as err:
            return err.messages, 422
        user = session.query(User).filter_by(username=user_data["username"]).first()
        if user:
            return errors.exists
        user = create_entry(User, **user_data)
        return jsonify(UserData().dump(user)), 200
    if request.method == "GET":
        users_list = session.query(User).all()
        return UserData().dump(users_list, many=True), 200

@user_blueprint.route('/user/<string:username>', methods=['GET', 'PUT', 'DELETE'])
def user_username_api(username):
    user = session.query(User).filter_by(username=username).first()
    if not user:
        return errors.not_found
    if request.method == 'GET':
        return UserData().dump(user), 200
    if request.method == 'PUT':
        json_data = request.json
        if not json_data:
            return errors.bad_request
        try:
            data = UserSchema().load(json_data, partial=True)
        except "ValidationError" as err:
            return err.messages, 422
        for key, value in data.items():
            if key == "username":
                us = session.query(User).filter_by(username=data["username"]).first()
                if us:
                    return errors.exists
        updated_user = update_entry(user, **data)
        for key, value in data.items():
            if key == "password" and len(data) == 1:
                return {"message": "Password changed successfully"}, 200
        return UserData().dump(updated_user), 200
    if request.method == 'DELETE':
        session.delete(user)
        session.commit()
        return {"message": "Deleted successfully"}, 200