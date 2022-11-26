import pymysql
from bcrypt import checkpw, hashpw, gensalt
from flask import Blueprint, request, jsonify, url_for, Response
from flask_bcrypt import generate_password_hash, check_password_hash
from marshmallow import ValidationError
from flask_httpauth import HTTPBasicAuth
from werkzeug.utils import redirect
from lab7 import db_utils
from lab7.db_utils import errors
from lab7 import schemas
from lab6 import models
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

api_blueprint = Blueprint('api', __name__)
auth = HTTPBasicAuth()

#todo add missing instances from swagger

@auth.verify_password
def verify_password(username, password):
    user = session.query(models.User).filter(models.User.username == username).first()
    return user and checkpw(bytes(password, 'utf-8'), bytes(user.password, 'utf-8'))
 # user = Session.query(User).filter(User.username == username).first()
 #    is_pass_valid = checkpw(bytes(user['password'], 'utf-8'), bytes(password, 'utf-8'))
 #    if is_pass_valid:
 #        return username

def get_current_user() -> models.User:
    username = auth.current_user()
    return session.query(models.User).filter(models.User.username == username).first()


@auth.get_user_roles
def get_user_roles(user):
    if "admin" in user.username.lower():
        return "admin"
    else:
        return "user"


@auth.error_handler
def auth_error(status):
    if status == 401:
        return errors.no_auth
    elif status == 403:
        return errors.no_access



Session = sessionmaker(bind=create_engine('mysql+pymysql://root:Busy18being@localhost/travelLab', echo=True))
session = Session()


### city
@api_blueprint.route("/city", methods=["POST"])
@auth.login_required(role="admin")
def city_():
    if request.method == 'POST':
        json_data = request.json
        if not json_data:
            return errors.bad_request
        try:
            subject_data = schemas.CityData().load(json_data)
        except (pymysql.Error, pymysql.Warning) as err:
            return err.messages, 422
        except ValidationError as err:
            return err.messages, 422
        except KeyError as err:
            return err.messages, 422
        new_subject = db_utils.create_entry(models.City, **subject_data)
        return jsonify(schemas.CityReq().dump(new_subject))

@api_blueprint.route("/city", methods=["GET"])
def city__():
    city_list = session.query(models.City).all()
    return schemas.CityData().dump(city_list, many=True), 200

@api_blueprint.route('/city/<int:id>', methods=['PUT', 'DELETE'])
@auth.login_required(role="admin")
def city_byid(id):
    city = session.query(models.City).filter_by(idcity=id).first()
    if not city:
        return errors.not_found
    if request.method == 'PUT':
        json_data = request.json
        if not json_data:
            return db_utils.errors.bad_request
        try:
            data = schemas.CityReq().load(json_data, partial=True)
        except ValidationError as error:
            return error.messages, 422
        except (pymysql.Error, pymysql.Warning) as err:
            return err.messages, 422
        updated_city = db_utils.update_entry(city, **data)
        return schemas.CityReq().dump(updated_city)
    if request.method == 'DELETE':
        session.delete(city)
        session.commit()
        return {"message": "Deleted successfully"}, 200

@api_blueprint.route('/city/<int:id>', methods=['GET'])
def city_byid_(id):
    city = session.query(models.City).filter_by(idcity=id).first()
    if not city:
        return errors.not_found
    if request.method == 'GET':
        return jsonify(schemas.CityReq().dump(city))

#todo crreate some file management???

### hotel
@api_blueprint.route("/hotel", methods=["POST"])
@auth.login_required(role="admin")
def hotel_():
    if request.method == 'POST':
        json_data = request.json
        if not json_data:
            return errors.bad_request
        try:
            city_data = schemas.HotelData().load(json_data)
        except (pymysql.Error, pymysql.Warning) as err:
            return err.messages, 422
        except ValidationError as err:
            return err.messages, 422
        except KeyError as err:
            return err.messages, 422
        new_city = db_utils.create_entry(models.Hotel, **city_data)
        return jsonify(schemas.HotelData().dump(new_city))

@api_blueprint.route("/hotel", methods=["GET"])
def hotel__():
    city_list = session.query(models.Hotel).all()
    return schemas.HotelData().dump(city_list, many=True), 200

@api_blueprint.route('/hotel/<int:id>', methods=['PUT', 'DELETE'])
@auth.login_required(role="admin")
def hotel_byid(id):
    city = session.query(models.Hotel).filter_by(idhotel=id).first()
    if not city:
        return errors.not_found
    if request.method == 'PUT':
        json_data = request.json
        if not json_data:
            return db_utils.errors.bad_request
        try:
            data = schemas.HotelData().load(json_data, partial=True)
        except (pymysql.Error, pymysql.Warning) as err:
            return err.messages, 422
        except ValidationError as err:
            return err.messages, 422
        except KeyError as err:
            return err.messages, 422
        updated_city = db_utils.update_entry(city, **data)
        return schemas.HotelData().dump(updated_city)
    if request.method == 'DELETE':
        try:
            session.delete(city)
            session.commit()
        except pymysql.err.IntegrityError:
            session.rollback()  # rollback
            return jsonify({"message": "foreign key constraint"}), 400  # just json return


        return {"message": "Deleted successfully"}, 200

@api_blueprint.route('/hotel/<int:id>', methods=['GET'])
def hotel_byid_(id):
    city = session.query(models.Hotel).filter_by(idhotel=id).first()
    if not city:
        return errors.not_found
    return jsonify(schemas.HotelData().dump(city))


### hotels choices
@api_blueprint.route("/hotelschoice", methods=["POST"])
@auth.login_required(role="admin")
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
        except KeyError as err:
            return err.messages, 422
        new_city = db_utils.create_entry(models.HotelsChoice, **city_data)
        return jsonify(schemas.HotelsChoiceData().dump(new_city))

@api_blueprint.route("/hotelschoice", methods=["GET"])
def hotelschoice__():
    city_list = session.query(models.HotelsChoice).all()
    return schemas.HotelsChoiceData().dump(city_list, many=True), 200

@api_blueprint.route('/hotelschoice/<int:id>', methods=['PUT', 'DELETE'])
def hotelschoice_byid(id):
    city = session.query(models.HotelsChoice).filter_by(idchoice=id).first()
    if not city:
        return errors.not_found
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

@api_blueprint.route('/hotelschoice/<int:id>', methods=['GET'])
def hotelschoice_byid_(id):
    city = session.query(models.HotelsChoice).filter_by(idchoice=id).first()
    if not city:
        return errors.not_found
    return jsonify(schemas.HotelsChoiceData().dump(city))



### user
@api_blueprint.route("/user", methods=["POST"])
def create_user():
    request_data = request.json
    if not request_data:
        return errors.bad_request
    try:
        user_data = schemas.UserSchema().load(request_data)
    except ValidationError as err:
        return err.messages, 422
    except KeyError as err:
        return err.messages, 422
    except (pymysql.Error, pymysql.Warning) as err:
        return err.messages, 422
    user = session.query(models.User).filter_by(username=user_data["username"]).first()
    if user:
        return errors.exists
    user = models.User(
        username=request_data['username'],
        password=hashpw(bytes(request_data['password'], 'utf-8'), gensalt(14)).decode(),
        name=request_data['name'],
        surname=request_data['surname'],
        passport=request_data['passport'],
    )
    session.add(user)
    session.commit()
    return jsonify(schemas.UserData().dump(user))

@api_blueprint.route("/user/login", methods=["GET"])
def login():
    json_data = request.json
    if not json_data:
        return errors.bad_request
    try:
        us = schemas.LoginSchema().load(json_data, partial=True)
    except ValidationError as err:
        return err.messages, 422
    except KeyError as err:
        return err.messages, 422
    # if not request.form['username'] or not request.form['password']:
    #     return errors.no_auth
    user = session.query(models.User).filter(models.User.username == us['username']).first()
    if not user:
        return errors.not_found
    is_pass_valid = checkpw(bytes(us['password'], 'utf-8'), bytes(user.password, 'utf-8'))
    if is_pass_valid:
        return {"message": "Successfully logged in"}, 200
    else:
        return {'error': {'code': 400, 'message': 'Incorrect password'}}, 400

#todo rearrange path according to swagger

@api_blueprint.route("/user/logout")
@auth.login_required
def logout():
    return redirect(f"http://logout:logout@{request.host}{url_for('api.login')}")

@api_blueprint.route("/users", methods=["GET"])
@auth.login_required(role="admin")
def get_users():
    users_list = session.query(models.User).all()
    return jsonify(schemas.UserData().dump(users_list, many=True)), 200


@api_blueprint.route('/user/<string:username>', methods=['GET', 'PUT', 'DELETE'])
@auth.login_required
def user_username_api(username):
    user = session.query(models.User).filter_by(username=username).first()

    if not user:
        return errors.not_found
    if request.method == 'GET':
        return schemas.UserData().dump(user), 200
    if request.method == 'PUT':
        if get_current_user().iduser != user.iduser:
            return errors.no_access
        json_data = request.json
        if not json_data:
            return errors.bad_request
        try:
            data = schemas.UserSchema().load(json_data, partial=True)
        except ValidationError as err:
            return err.messages, 422
        except KeyError as err:
            return err.messages, 422
        except (pymysql.Error, pymysql.Warning) as err:
            return err.messages, 422
        for key, value in data.items():
            if key == "username":
                us = session.query(models.User).filter_by(username=data["username"]).first()
                if us:
                    return errors.exists
            if key == "password":
                data['password'] = hashpw(bytes(data['password'], 'utf-8'), gensalt(14)).decode()
                print(data['password'])
        updated_user = db_utils.update_entry(user, **data)
        for key, value in data.items():
            if key == "password" and len(data) == 1:
                return {"message": "Password changed successfully"}, 200
        return schemas.UserData().dump(updated_user), 200
    if request.method == 'DELETE':
        if get_current_user().iduser != user.iduser:
            return errors.no_access
        session.delete(user)
        session.commit()
        return {"message": "Deleted successfully"}, 200

### transport
@api_blueprint.route("/transport", methods=["POST"])
@auth.login_required(role="admin")
def transport_():
    if request.method == 'POST':
        json_data = request.json
        if not json_data:
            return errors.bad_request
        try:
            city_data = schemas.TransportData().load(json_data)
        except (pymysql.Error, pymysql.Warning) as err:
            return err.messages, 422
        except ValidationError as err:
            return err.messages, 422
        except KeyError as err:
            return err.messages, 422
        new_city = db_utils.create_entry(models.Transport, **city_data)
        return jsonify(schemas.TransportData().dump(new_city))


@api_blueprint.route("/transport", methods=["GET"])
def transport__():
    city_list = session.query(models.Transport).all()
    return schemas.TransportData().dump(city_list, many=True), 200

@api_blueprint.route('/transport/<int:id>', methods=['GET', 'PUT', 'DELETE'])
@auth.login_required(role="admin")
def transport_byid(id):
    city = session.query(models.Transport).filter_by(idtransport=id).first()
    if not city:
        return errors.not_found
    if request.method == 'GET':
        return jsonify(schemas.TransportData().dump(city))
    if request.method == 'PUT':
        json_data = request.json
        if not json_data:
            return db_utils.errors.bad_request
        try:
            data = schemas.TransportData().load(json_data, partial=True)
        except (pymysql.Error, pymysql.Warning) as err:
            return err.messages, 422
        except ValidationError as err:
            return err.messages, 422
        except KeyError as err:
            return err.messages, 422
        updated_city = db_utils.update_entry(city, **data)
        return schemas.TransportData().dump(updated_city)
    if request.method == 'DELETE':
        try:
            session.delete(city)
            session.commit()
        except pymysql.err.IntegrityError:
            session.rollback()  # rollback
            return jsonify({"message": "foreign key constraint"}), 400  # just json return


        return {"message": "Deleted successfully"}, 200

### trip
@api_blueprint.route("/trip", methods=["POST"])
@auth.login_required(role="admin")
def trip_():
    if request.method == 'POST':
        json_data = request.json
        if not json_data:
            return errors.bad_request
        try:
            city_data = schemas.TripData().load(json_data)
        except (pymysql.Error, pymysql.Warning) as err:
            return err.messages, 422
        except ValidationError as err:
            return err.messages, 422
        except KeyError as err:
            return err.messages, 422
        new_city = db_utils.create_entry(models.Trip, **city_data)
        return jsonify(schemas.TripData().dump(new_city))


@api_blueprint.route("/trip", methods=["GET"])
@auth.login_required(role="admin")
def trip__():
    city_list = session.query(models.Trip).all()
    return schemas.TripData().dump(city_list, many=True), 200

@api_blueprint.route('/trip/<int:id>', methods=['GET', 'PUT', 'DELETE'])
@auth.login_required
def trip_byid(id):
    city = session.query(models.Trip).filter_by(idtrip=id).first()
    if not city:
        return errors.not_found
    if request.method == 'GET':
        return jsonify(schemas.TripData().dump(city))
    if request.method == 'PUT':
        json_data = request.json
        if not json_data:
            return db_utils.errors.bad_request
        try:
            data = schemas.TripData().load(json_data, partial=True)
        except (pymysql.Error, pymysql.Warning) as err:
            return err.messages, 422
        except ValidationError as err:
            return err.messages, 422
        except KeyError as err:
            return err.messages, 422
        updated_city = db_utils.update_entry(city, **data)
        return schemas.TripData().dump(updated_city)
    if request.method == 'DELETE':
        try:
            session.delete(city)
            session.commit()
        except pymysql.err.IntegrityError:
            session.rollback()  # rollback
            return jsonify({"message": "foreign key constraint"}), 400  # just json return

        return {"message": "Deleted successfully"}, 200

# payment
@api_blueprint.route("/payment", methods=["POST", "GET"])
def payment_():
    if request.method == 'POST':
        json_data = request.json
        if not json_data:
            return errors.bad_request
        try:
            city_data = schemas.PaymentData().load(json_data)
        except (pymysql.Error, pymysql.Warning) as err:
            return err.messages, 422
        except ValidationError as err:
            return err.messages, 422
        new_city = db_utils.create_entry(models.Payment, **city_data)
        return jsonify(schemas.PaymentData().dump(new_city))
    if request.method == 'GET':
        city_list = session.query(models.Payment).all()
        return jsonify(schemas.PaymentData().dump(city_list, many=True)), 200

@api_blueprint.route('/payment/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def payment_byid(id):
    city = session.query(models.Payment).filter_by(idpayment=id).first()
    if not city:
        return errors.not_found
    if request.method == 'GET':
        return jsonify(schemas.PaymentData().dump(city))
    if request.method == 'PUT':
        json_data = request.json
        if not json_data:
            return db_utils.errors.bad_request
        try:
            data = schemas.PaymentData().load(json_data, partial=True)
        except (pymysql.Error, pymysql.Warning) as err:
            return err.messages, 422
        except ValidationError as err:
            return err.messages, 422
        except KeyError as err:
            return err.messages, 422
        updated_city = db_utils.update_entry(city, **data)
        return jsonify(schemas.PaymentData().dump(updated_city))
    if request.method == 'DELETE':
        try:
            session.delete(city)
            session.commit()
        except pymysql.err.IntegrityError:
            session.rollback()  # rollback
            return jsonify({"message": "foreign key constraint"}), 400  # just json return
        return {"message": "Deleted successfully"}, 200

# booking
@api_blueprint.route("/booking", methods=["POST"])
@auth.login_required(role="admin")
def booking_():
    if request.method == 'POST':
        json_data = request.json
        if not json_data:
            return errors.bad_request
        try:
            city_data = schemas.BookingData().load(json_data)
        except (pymysql.Error, pymysql.Warning) as err:
            return err.messages, 422
        except ValidationError as err:
            return err.messages, 422
        except KeyError as err:
            return err.messages, 422
        new_city = db_utils.create_entry(models.Booking, **city_data)
        return jsonify(schemas.BookingData().dump(new_city))

@api_blueprint.route("/booking", methods=["GET"])
@auth.login_required
def booking__():
    city_list = session.query(models.Booking).all()
    return schemas.BookingData().dump(city_list, many=True), 200

@api_blueprint.route('/booking/<int:id>', methods=['GET', 'PUT', 'DELETE'])
@auth.login_required
def booking_byid(id):
    city = session.query(models.Booking).filter_by(idbooking=id).first()
    if not city:
        return errors.not_found
    if request.method == 'GET':
        return jsonify(schemas.BookingData().dump(city))
    if request.method == 'PUT':
        #todo rename temp
        #todo beautify
        json_data = request.json
        temp = json_data['client_id']
        exists = session.query(models.User.iduser).filter_by(iduser=temp).first() is not None
        if not exists:
            return db_utils.errors.not_found1
        if not json_data:
            return db_utils.errors.bad_request
        try:
            data = schemas.BookingData().load(json_data, partial=True)
        except (pymysql.Error, pymysql.Warning) as err:
            return err.messages, 422
        except ValidationError as err:
            return err.messages, 422
        updated_city = db_utils.update_entry(city, **data)
        return schemas.BookingData().dump(updated_city)
    if request.method == 'DELETE':
        session.delete(city)
        session.commit()
        return {"message": "Deleted successfully"}, 200