import json

from flask import jsonify, request, Blueprint, render_template, redirect, url_for
from marshmallow import ValidationError


from db_utils import errors, create_entry, update_entry
from schemas import CityData
from models import City
from db_utils import session

city_blueprint = Blueprint("city", __name__)


@city_blueprint.route("/start", methods=["POST", "GET"])
def start():
    return render_template("start.html")


@city_blueprint.route("/query", methods=["POST", "GET"])
def query():
    result = session.execute(
        "SELECT c.name as city, c.foundation_year, c.country, h.name as hotel, h.rating, h.price FROM city as c JOIN hotel as h ON h.city_id = c.idcity ORDER BY c.idcity;"
    )
    return render_template("query.html", result=result)


@city_blueprint.route("/city", methods=["POST", "GET"])
def city_():
    if request.method == "GET":
        city_list = session.query(City).all()
        data = CityData().dump(city_list, many=True)
        return render_template("city.html", cities=data)

    if request.method == "POST":
        if "delete_id" in request.form:
            city = (
                session.query(City)
                .filter_by(idcity=int(request.form["delete_id"]))
                .first()
            )
            session.delete(city)
            session.commit()
            return redirect(url_for("city.city_"))
        else:
            request_data = {
                "name": request.form["name"],
                "country": request.form["country"],
                "foundation_year": int(request.form["year"]),
            }
            json_data = json.dumps(request_data)
            if not json_data:
                return errors.bad_request
            try:
                subject_data = CityData().loads(json_data)
                print(subject_data)
            except ValidationError as err:
                return err.messages, 422
            create_entry(City, **subject_data)
            return redirect(url_for("city.city_"))


@city_blueprint.route("/city/<int:id>", methods=["GET", "POST", "DELETE"])
def city_by_id(id):
    city = session.query(City).filter_by(idcity=id).first()
    if not city:
        return errors.not_found

    if request.method == "GET":
        data = CityData().dump(city)
        return render_template("city_id.html", city=data)

    if request.method == "POST":
        request_data = {}

        if request.form["name"]:
            request_data["name"] = request.form["name"]

        if request.form["country"]:
            request_data["country"] = request.form["country"]

        if request.form["year"]:
            request_data["foundation_year"] = int(request.form["year"])

        json_data = json.dumps(request_data)
        if not json_data:
            return errors.bad_request
        try:
            data = CityData().loads(json_data, partial=True)
        except ValidationError as error:
            return error.messages, 422
        updated_city = update_entry(city, **data)
        data = CityData().dump(updated_city)
        return render_template("city_id.html", city=data)


@city_blueprint.route("/city/<string:country>", methods=["GET"])
def city_by_country(country):
    city_list = session.query(City).filter_by(country=country).all()
    if not city_list:
        return errors.not_found
    else:
        return jsonify(CityData().dump(city_list, many=True))
