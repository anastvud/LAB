import unittest
from base64 import b64encode

from bcrypt import hashpw, gensalt
from flask import Flask
from lab7.blueprint import api_blueprint
from lab7.db_utils import Session

session = Session()


class Test(unittest.TestCase):
    API_URL = "http://localhost:5000/api/v1"
    USER_URL = "{}/user".format(API_URL)
    CITY_URL = "{}/city".format(API_URL)
    HOTEL_URL = "{}/hotel".format(API_URL)
    HOTELSCHOICE_URL = "{}/hotelschoice".format(API_URL)
    TRANSPORT_URL = "{}/transport".format(API_URL)
    TRIP_URL = "{}/trip".format(API_URL)
    PAYMENT_URL = "{}/payment".format(API_URL)
    BOOKING_URL = "{}/booking".format(API_URL)

    def setUp(self) -> None:
        app = Flask(__name__)
        self.app_context = app.app_context()
        self.app_context.push()
        self.client = app.test_client()
        app.register_blueprint(api_blueprint, url_prefix="/api/v1")
        session.begin()

    def tearDown(self) -> None:
        session.close()
        self.app_context.pop()

    def request_headers_user(self):
        """Returns API request headers."""
        auth = '{0}:{1}'.format('u1', '1')
        return {
            'Accept': 'application/json',
            'Authorization': 'Basic {encoded_login}'.format(
                encoded_login=b64encode(auth.encode('utf-8')).decode('utf-8')
            )
        }

    # def request_headers_user_new(self):
    #     """Returns API request headers."""
    #     auth = '{0}:{1}'.format('userforpl', '111')
    #     return {
    #         'Accept': 'application/json',
    #         'Authorization': 'Basic {encoded_login}'.format(
    #             encoded_login=b64encode(auth.encode('utf-8')).decode('utf-8')
    #         )
    #     }
    #
    def request_headers_user_tony(self):
        """Returns API request headers."""
        auth = '{0}:{1}'.format('tonystark', 'jarvis')
        return {
            'Accept': 'application/json',
            'Authorization': 'Basic {encoded_login}'.format(
                encoded_login=b64encode(auth.encode('utf-8')).decode('utf-8')
            )
        }

    def request_headers_admin(self):
        """Returns API request headers."""
        auth = '{0}:{1}'.format('admin', 'p')
        return {
            'Accept': 'application/json',
            'Authorization': 'Basic {encoded_login}'.format(
                encoded_login=b64encode(auth.encode('utf-8')).decode('utf-8')
            )
        }

    def test_create_user(self):
        payload = {"username": "tonystark",
                   "password": "jarvis",
                   "name": "tony",
                   "surname": "stark",
                   "passport": "pg097889"
                   }

        resp = self.client.post(self.USER_URL, json=payload)
        self.assertEqual(resp.status_code, 200)

    def test_create_user1(self):
        payload = {}
        resp = self.client.post(self.USER_URL, json=payload)
        self.assertEqual(resp.status_code, 400)

    def test_create_user2(self):  # existing
        payload = {"username": "tonystark",
                   "password": "jarvis",
                   "name": "tony",
                   "surname": "stark",
                   "passport": "pg097889"
                   }
        resp = self.client.post(self.USER_URL, json=payload)
        self.assertEqual(resp.status_code, 403)

    def test_login1(self):
        payload = {
            "username": "tonystark",
            "password": "jarvis"
        }
        resp = self.client.get(self.USER_URL + '/login', json=payload)
        self.assertEqual(resp.status_code, 200)

    def test_login2(self):
        payload = {
            "username": "wrong",
            "password": "jarvis"
        }
        resp = self.client.get(self.USER_URL + '/login', json=payload)
        self.assertEqual(resp.status_code, 404)

    def test_login3(self):  # incorrect pass
        payload = {
            "username": "tonystark",
            "password": "jjarvis"
        }
        resp = self.client.get(self.USER_URL + '/login', json=payload)
        self.assertEqual(resp.status_code, 401)

    def test_login4(self):  # incorrect pass
        payload = {}
        resp = self.client.get(self.USER_URL + '/login', json=payload)
        self.assertEqual(resp.status_code, 400)

    def test_get_users(self):
        responce = self.client.get(self.USER_URL, headers=self.request_headers_user())
        self.assertEqual(responce.status_code, 403)

    def test_get_users_admin(self):
        responce = self.client.get(self.USER_URL, headers=self.request_headers_admin())
        self.assertEqual(responce.status_code, 200)

    def test_get_username(self):
        responce = self.client.get(self.USER_URL + "/u1", headers=self.request_headers_user())
        self.assertEqual(responce.status_code, 200)

    def test_put_user_success(self):
        payload = {
            "name": "User"
        }
        resp = self.client.put(self.USER_URL + '/u1', headers=self.request_headers_user(), json=payload)
        self.assertEqual(resp.status_code, 200)

    def test_put_user_no_data(self):
        payload = {}
        resp = self.client.put(self.USER_URL + '/u1', headers=self.request_headers_user(), json=payload)
        self.assertEqual(resp.status_code, 400)

    def test_delete_user_succ(self):
        resp = self.client.delete(self.USER_URL + '/tonystark', headers=self.request_headers_user_tony())
        self.assertEqual(resp.status_code, 200)

    def test_delete_no_acc(self):
        resp = self.client.delete(self.USER_URL + '/admin', headers=self.request_headers_user())
        self.assertEqual(resp.status_code, 403)

    def test_delete_not_found(self):
        resp = self.client.delete(self.USER_URL + '/rand', headers=self.request_headers_user())
        self.assertEqual(resp.status_code, 404)

    def test_get_city(self):
        resp = self.client.get(self.CITY_URL)
        self.assertEqual(resp.status_code, 200)

    def test_get_city_by_id(self):
        id = '1'
        resp = self.client.get(self.CITY_URL + '/' + id)
        self.assertEqual(resp.status_code, 200)

    def test_get_hotel(self):
        resp = self.client.get(self.HOTEL_URL)
        self.assertEqual(resp.status_code, 200)

    def test_get_hotelschoice(self):
        resp = self.client.get(self.HOTELSCHOICE_URL)
        self.assertEqual(resp.status_code, 200)

    def test_get_payment(self):
        resp = self.client.get(self.PAYMENT_URL)
        self.assertEqual(resp.status_code, 200)

    def test_create_payment(self):
        payload = {"name": "gift card"}
        responce = self.client.post(self.PAYMENT_URL, json=payload, headers=self.request_headers_admin())
        self.assertEqual(responce.status_code, 200)

    def test_create_payment_empty(self):
        payload = {}
        responce = self.client.post(self.PAYMENT_URL, json=payload, headers=self.request_headers_admin())
        self.assertEqual(responce.status_code, 400)

    def test_create_payment_no_acc(self):
        payload = {"name": "gift card"}
        responce = self.client.post(self.PAYMENT_URL, json=payload, headers=self.request_headers_user())
        self.assertEqual(responce.status_code, 403)

    def test_create_payment_exists(self):
        payload = {"name": "card"}
        responce = self.client.post(self.PAYMENT_URL, json=payload, headers=self.request_headers_admin())
        self.assertEqual(responce.status_code, 200)

    def test_get_payment_(self):
        resp = self.client.get(self.PAYMENT_URL, headers=self.request_headers_admin())
        self.assertEqual(resp.status_code, 200)

    def test_get_payment_no_auth(self):
        resp = self.client.get(self.PAYMENT_URL)
        self.assertEqual(resp.status_code, 401)

    def test_get_payment_by_id(self):
        resp = self.client.get(self.PAYMENT_URL + '/2', headers=self.request_headers_admin())
        self.assertEqual(resp.status_code, 200)

    def test_get_payment_by_id_no_auth(self):
        resp = self.client.get(self.PAYMENT_URL + '/2')
        self.assertEqual(resp.status_code, 401)

    def test_get_payment_by_id_notfound(self):
        resp = self.client.get(self.PAYMENT_URL + '/6778', headers=self.request_headers_admin())
        self.assertEqual(resp.status_code, 404)

    def test_put_payment(self):
        payload = {"name": "card1"}
        resp = self.client.put(self.PAYMENT_URL + '/1', headers=self.request_headers_admin(), json=payload)
        self.assertEqual(resp.status_code, 200)
        payload = {"name": "cas2"}
        resp = self.client.put(self.PAYMENT_URL + '/2', headers=self.request_headers_admin(), json=payload)

    def test_put_payment_notfound(self):
        payload = {"name": "f"}
        resp = self.client.put(self.PAYMENT_URL + '/4234', headers=self.request_headers_admin(), json=payload)
        self.assertEqual(resp.status_code, 404)

    def test_put_payment_no_acc(self):
        payload = {"name": "f"}
        resp = self.client.put(self.PAYMENT_URL + '/1', headers=self.request_headers_user(), json=payload)
        self.assertEqual(resp.status_code, 403)

    def test_put_payment_empty(self):
        payload = {}
        resp = self.client.put(self.PAYMENT_URL + '/2', headers=self.request_headers_admin(), json=payload)
        self.assertEqual(resp.status_code, 400)

    def test_delete_payment(self):
        resp = self.client.delete(self.PAYMENT_URL + '/11', headers=self.request_headers_admin())
        self.assertEqual(resp.status_code, 200)

    def test_delete_payment_notfound(self):
        resp = self.client.delete(self.PAYMENT_URL + '/6543', headers=self.request_headers_admin())
        self.assertEqual(resp.status_code, 404)

    def test_delete_payment_no_acc(self):
        resp = self.client.delete(self.PAYMENT_URL + '/11', headers=self.request_headers_user())
        self.assertEqual(resp.status_code, 403)

    def test_get_hotel_(self):
        resp = self.client.get(self.HOTEL_URL)
        self.assertEqual(resp.status_code, 200)

    def test_create_hotel(self):
        payload = {"name": "Jordan"}
        responce = self.client.post(self.HOTEL_URL, json=payload, headers=self.request_headers_admin())
        self.assertEqual(responce.status_code, 200)

    def test_create_hotel_empty(self):
        payload = {}
        responce = self.client.post(self.HOTEL_URL, json=payload, headers=self.request_headers_admin())
        self.assertEqual(responce.status_code, 400)

    def test_create_hotel_no_acc(self):
        payload = {"name": "Jordan"}
        responce = self.client.post(self.HOTEL_URL, json=payload, headers=self.request_headers_user())
        self.assertEqual(responce.status_code, 403)

    def test_create_hotel_exists(self):
        payload = {"name": "Mariott"}
        responce = self.client.post(self.HOTEL_URL, json=payload, headers=self.request_headers_admin())
        self.assertEqual(responce.status_code, 200)

    def test_get_hotel_no_auth(self):
        resp = self.client.get(self.HOTEL_URL)
        self.assertEqual(resp.status_code, 401)

    def test_get_hotel_by_id(self):
        resp = self.client.get(self.HOTEL_URL + '/1', headers=self.request_headers_admin())
        self.assertEqual(resp.status_code, 200)

    def test_get_hotel_by_id_no_auth(self):
        resp = self.client.get(self.HOTEL_URL + '/1')
        self.assertEqual(resp.status_code, 401)

    def test_get_hotel_by_id_notfound(self):
        resp = self.client.get(self.HOTEL_URL + '/6778', headers=self.request_headers_admin())
        self.assertEqual(resp.status_code, 404)

    def test_put_hotel(self):
        payload = {"name": "Royal"}
        resp = self.client.put(self.HOTEL_URL + '/2', headers=self.request_headers_admin(), json=payload)
        self.assertEqual(resp.status_code, 200)

    def test_put_hotel_notfound(self):
        payload = {"name": "f"}
        resp = self.client.put(self.HOTEL_URL + '/4234', headers=self.request_headers_admin(), json=payload)
        self.assertEqual(resp.status_code, 404)

    def test_put_hotel_no_acc(self):
        payload = {"name": "f"}
        resp = self.client.put(self.HOTEL_URL + '/1', headers=self.request_headers_user(), json=payload)
        self.assertEqual(resp.status_code, 403)

    def test_put_hotel_empty(self):
        payload = {}
        resp = self.client.put(self.HOTEL_URL + '/2', headers=self.request_headers_admin(), json=payload)
        self.assertEqual(resp.status_code, 400)

    def test_delete_hotel(self):
        resp = self.client.delete(self.HOTEL_URL + '/8', headers=self.request_headers_admin())
        self.assertEqual(resp.status_code, 200)

    def test_delete_hotel_notfound(self):
        resp = self.client.delete(self.HOTEL_URL + '/6543', headers=self.request_headers_admin())
        self.assertEqual(resp.status_code, 404)

    def test_delete_hotel_no_acc(self):
        resp = self.client.delete(self.HOTEL_URL + '/8', headers=self.request_headers_user())
        self.assertEqual(resp.status_code, 403)

    def test_get_transport(self):
        resp = self.client.get(self.TRANSPORT_URL)
        self.assertEqual(resp.status_code, 200)

    def test_get_transport_(self):
        resp = self.client.get(self.TRANSPORT_URL)
        self.assertEqual(resp.status_code, 200)

    def test_create_transport(self):
        payload = {"name": "plane"}
        responce = self.client.post(self.TRANSPORT_URL, json=payload, headers=self.request_headers_admin())
        self.assertEqual(responce.status_code, 200)

    def test_create_transport_empty(self):
        payload = {}
        responce = self.client.post(self.TRANSPORT_URL, json=payload, headers=self.request_headers_admin())
        self.assertEqual(responce.status_code, 400)

    def test_create_transport_no_acc(self):
        payload = {"name": "plane"}
        responce = self.client.post(self.TRANSPORT_URL, json=payload, headers=self.request_headers_user())
        self.assertEqual(responce.status_code, 403)

    def test_create_transport_exists(self):
        payload = {"name": "train"}
        responce = self.client.post(self.TRANSPORT_URL, json=payload, headers=self.request_headers_admin())
        self.assertEqual(responce.status_code, 200)

    def test_get_transport_no_auth(self):
        resp = self.client.get(self.TRANSPORT_URL)
        self.assertEqual(resp.status_code, 401)

    def test_get_transport_by_id(self):
        resp = self.client.get(self.TRANSPORT_URL + '/2', headers=self.request_headers_admin())
        self.assertEqual(resp.status_code, 200)

    def test_get_transport_by_id_no_auth(self):
        resp = self.client.get(self.TRANSPORT_URL + '/2')
        self.assertEqual(resp.status_code, 401)

    def test_get_transport_by_id_notfound(self):
        resp = self.client.get(self.TRANSPORT_URL + '/6778', headers=self.request_headers_admin())
        self.assertEqual(resp.status_code, 404)

    def test_put_transport(self):
        payload = {"name": "train"}
        resp = self.client.put(self.TRANSPORT_URL + '/2', headers=self.request_headers_admin(), json=payload)
        self.assertEqual(resp.status_code, 200)

    def test_put_transport_notfound(self):
        payload = {"name": "f"}
        resp = self.client.put(self.TRANSPORT_URL + '/4234', headers=self.request_headers_admin(), json=payload)
        self.assertEqual(resp.status_code, 404)

    def test_put_transport_no_acc(self):
        payload = {"name": "f"}
        resp = self.client.put(self.TRANSPORT_URL + '/2', headers=self.request_headers_user(), json=payload)
        self.assertEqual(resp.status_code, 403)

    def test_put_transport_empty(self):
        payload = {}
        resp = self.client.put(self.TRANSPORT_URL + '/2', headers=self.request_headers_admin(), json=payload)
        self.assertEqual(resp.status_code, 400)

    def test_delete_transport(self):
        resp = self.client.delete(self.TRANSPORT_URL + '/7', headers=self.request_headers_admin())
        self.assertEqual(resp.status_code, 200)

    def test_delete_transport_notfound(self):
        resp = self.client.delete(self.TRANSPORT_URL + '/6543', headers=self.request_headers_admin())
        self.assertEqual(resp.status_code, 404)

    def test_delete_transport_no_acc(self):
        resp = self.client.delete(self.TRANSPORT_URL + '/7', headers=self.request_headers_user())
        self.assertEqual(resp.status_code, 403)

    def test_get_trip_(self):
        resp = self.client.get(self.TRIP_URL)
        self.assertEqual(resp.status_code, 200)

    def test_create_trip(self):
        payload = {"transport_id": "4"}
        responce = self.client.post(self.TRIP_URL, json=payload, headers=self.request_headers_admin())
        self.assertEqual(responce.status_code, 200)

    def test_create_trip_empty(self):
        payload = {}
        responce = self.client.post(self.TRIP_URL, json=payload, headers=self.request_headers_admin())
        self.assertEqual(responce.status_code, 400)

    def test_create_trip_no_acc(self):
        payload = {"transport_id": "4"}
        responce = self.client.post(self.TRIP_URL, json=payload, headers=self.request_headers_user())
        self.assertEqual(responce.status_code, 403)

    def test_create_trip_exists(self):
        payload = {"days": 3,
                   "start_date": "2021-03-01",
                   "transport_id": 5}
        responce = self.client.post(self.TRIP_URL, json=payload, headers=self.request_headers_admin())
        self.assertEqual(responce.status_code, 200)

    def test_get_trip_no_auth(self):
        resp = self.client.get(self.TRIP_URL)
        self.assertEqual(resp.status_code, 401)

    def test_get_trip_by_id(self):
        resp = self.client.get(self.TRIP_URL + '/5', headers=self.request_headers_admin())
        self.assertEqual(resp.status_code, 200)

    def test_get_trip_by_id_no_auth(self):
        resp = self.client.get(self.TRIP_URL + '/5')
        self.assertEqual(resp.status_code, 401)

    def test_get_trip_by_id_notfound(self):
        resp = self.client.get(self.TRIP_URL + '/6778', headers=self.request_headers_admin())
        self.assertEqual(resp.status_code, 404)

    def test_put_trip(self):
        payload = {"transport_id": 5}
        resp = self.client.put(self.TRIP_URL + '/5', headers=self.request_headers_admin(), json=payload)
        self.assertEqual(resp.status_code, 200)

    def test_put_trip_notfound(self):
        payload = {"name": "f"}
        resp = self.client.put(self.TRIP_URL + '/4234', headers=self.request_headers_admin(), json=payload)
        self.assertEqual(resp.status_code, 404)

    def test_put_trip_no_acc(self):
        payload = {"name": "f"}
        resp = self.client.put(self.TRIP_URL + '/5', headers=self.request_headers_user(), json=payload)
        self.assertEqual(resp.status_code, 403)

    def test_put_trip_empty(self):
        payload = {}
        resp = self.client.put(self.TRIP_URL + '/5', headers=self.request_headers_admin(), json=payload)
        self.assertEqual(resp.status_code, 400)

    def test_delete_trip(self):
        resp = self.client.delete(self.TRIP_URL + '/7', headers=self.request_headers_admin())
        self.assertEqual(resp.status_code, 200)

    def test_delete_trip_notfound(self):
        resp = self.client.delete(self.TRIP_URL + '/6543', headers=self.request_headers_admin())
        self.assertEqual(resp.status_code, 404)

    def test_delete_trip_no_acc(self):
        resp = self.client.delete(self.TRIP_URL + '/7', headers=self.request_headers_user())
        self.assertEqual(resp.status_code, 403)

    def test_get_hotelschoice_(self):
        resp = self.client.get(self.HOTELSCHOICE_URL)
        self.assertEqual(resp.status_code, 200)

    def test_create_hotelschoice(self):
        payload = {    "hotel_id": 2,
    "city_id": 1}
        responce = self.client.post(self.HOTELSCHOICE_URL, json=payload, headers=self.request_headers_admin())
        self.assertEqual(responce.status_code, 200)

    def test_create_hotelschoice_empty(self):
        payload = {}
        responce = self.client.post(self.HOTELSCHOICE_URL, json=payload, headers=self.request_headers_admin())
        self.assertEqual(responce.status_code, 400)

    def test_create_hotelschoice_no_acc(self):
        payload = {    "hotel_id": 2,
    "city_id": 1}
        responce = self.client.post(self.HOTELSCHOICE_URL, json=payload, headers=self.request_headers_user())
        self.assertEqual(responce.status_code, 403)

    def test_create_hotelschoice_exists(self):
        payload = {    "hotel_id": 2,
    "city_id": 1}
        responce = self.client.post(self.HOTELSCHOICE_URL, json=payload, headers=self.request_headers_admin())
        self.assertEqual(responce.status_code, 200)


    def test_get_hotelschoice_no_auth(self):
        resp = self.client.get(self.HOTELSCHOICE_URL)
        self.assertEqual(resp.status_code, 401)

    def test_get_hotelschoice_by_id(self):
        resp = self.client.get(self.HOTELSCHOICE_URL + '/3', headers=self.request_headers_admin())
        self.assertEqual(resp.status_code, 200)

    def test_get_hotelschoice_by_id_no_auth(self):
        resp = self.client.get(self.HOTELSCHOICE_URL + '/3')
        self.assertEqual(resp.status_code, 401)

    def test_get_hotelschoice_by_id_notfound(self):
        resp = self.client.get(self.HOTELSCHOICE_URL + '/6778', headers=self.request_headers_admin())
        self.assertEqual(resp.status_code, 404)

    def test_put_hotelschoice(self):
        payload = {"city_id": 2}
        resp = self.client.put(self.HOTELSCHOICE_URL + '/3', headers=self.request_headers_admin(), json=payload)
        self.assertEqual(resp.status_code, 200)

    def test_put_hotelschoice_notfound(self):
        payload = {"city_id": 2}
        resp = self.client.put(self.HOTELSCHOICE_URL + '/4234', headers=self.request_headers_admin(), json=payload)
        self.assertEqual(resp.status_code, 404)

    def test_put_hotelschoice_no_acc(self):
        payload = {"city_id": 2}
        resp = self.client.put(self.HOTELSCHOICE_URL + '/5', headers=self.request_headers_user(), json=payload)
        self.assertEqual(resp.status_code, 403)

    def test_put_hotelschoice_empty(self):
        payload = {}
        resp = self.client.put(self.HOTELSCHOICE_URL + '/3', headers=self.request_headers_admin(), json=payload)
        self.assertEqual(resp.status_code, 400)

    def test_delete_hotelschoice(self):
        resp = self.client.delete(self.HOTELSCHOICE_URL + '/9', headers=self.request_headers_admin())
        self.assertEqual(resp.status_code, 200)

    def test_delete_hotelschoice_notfound(self):
        resp = self.client.delete(self.HOTELSCHOICE_URL + '/6543', headers=self.request_headers_admin())
        self.assertEqual(resp.status_code, 404)

    def test_delete_hotelschoice_no_acc(self):
        resp = self.client.delete(self.HOTELSCHOICE_URL + '/9', headers=self.request_headers_user())
        self.assertEqual(resp.status_code, 403)

    def test_get_booking_(self):
        resp = self.client.get(self.BOOKING_URL)
        self.assertEqual(resp.status_code, 200)

    def test_create_booking(self):
        payload = {        "client_id": 10,
        "payment_id": 2,
        "trip_id": 5}
        responce = self.client.post(self.BOOKING_URL, json=payload, headers=self.request_headers_admin())
        self.assertEqual(responce.status_code, 200)

    def test_create_booking_empty(self):
        payload = {}
        responce = self.client.post(self.BOOKING_URL, json=payload, headers=self.request_headers_admin())
        self.assertEqual(responce.status_code, 400)

    def test_create_booking_no_acc(self):
        payload = {        "client_id": 10,
        "payment_id": 2,
        "trip_id": 6}
        responce = self.client.post(self.BOOKING_URL, json=payload, headers=self.request_headers_user())
        self.assertEqual(responce.status_code, 403)

    def test_create_booking_exists(self):
        payload = {        "client_id": 10,
        "payment_id": 2,
        "trip_id": 5}
        responce = self.client.post(self.BOOKING_URL, json=payload, headers=self.request_headers_admin())
        self.assertEqual(responce.status_code, 200)


    def test_get_booking_no_auth(self):
        resp = self.client.get(self.BOOKING_URL)
        self.assertEqual(resp.status_code, 401)

    def test_get_booking_by_id(self):
        resp = self.client.get(self.BOOKING_URL + '/10', headers=self.request_headers_admin())
        self.assertEqual(resp.status_code, 200)

    def test_get_booking_by_id_no_auth(self):
        resp = self.client.get(self.BOOKING_URL + '/10')
        self.assertEqual(resp.status_code, 401)

    def test_get_booking_by_id_notfound(self):
        resp = self.client.get(self.BOOKING_URL + '/6778', headers=self.request_headers_admin())
        self.assertEqual(resp.status_code, 404)

    def test_put_booking(self):
        payload = {"city_id": 2}
        resp = self.client.put(self.BOOKING_URL + '/10', headers=self.request_headers_admin(), json=payload)
        self.assertEqual(resp.status_code, 200)

    def test_put_booking_notfound(self):
        payload = {"client_id": 7}
        resp = self.client.put(self.BOOKING_URL + '/4234', headers=self.request_headers_admin(), json=payload)
        self.assertEqual(resp.status_code, 404)

    def test_put_booking_no_acc(self):
        payload = {"client_id": 7}
        resp = self.client.put(self.BOOKING_URL + '/10', headers=self.request_headers_user(), json=payload)
        self.assertEqual(resp.status_code, 403)

    def test_put_booking_empty(self):
        payload = {}
        resp = self.client.put(self.BOOKING_URL + '/10', headers=self.request_headers_admin(), json=payload)
        self.assertEqual(resp.status_code, 400)

    def test_delete_booking(self):
        resp = self.client.delete(self.BOOKING_URL + '/13', headers=self.request_headers_admin())
        self.assertEqual(resp.status_code, 200)

    def test_delete_booking_notfound(self):
        resp = self.client.delete(self.BOOKING_URL + '/6543', headers=self.request_headers_admin())
        self.assertEqual(resp.status_code, 404)

    def test_delete_booking_no_acc(self):
        resp = self.client.delete(self.BOOKING_URL + '/13', headers=self.request_headers_user())
        self.assertEqual(resp.status_code, 403)