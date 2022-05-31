from python.icbc_mock_svc.config import Config
from flask import request, jsonify, Flask, make_response
import logging
import json
import logging.config
from functools import wraps


application = Flask(__name__)
application.secret = Config.FLASK_SECRET_KEY
logging.basicConfig(level=Config.LOG_LEVEL)
logging.warning('*** icbc mock service initialized ***')


def basic_auth_required(f):
    """
    Decorator that implements basic auth when added to a route
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not _check_credentials(
                Config.ICBC_API_USERNAME, Config.ICBC_API_PASSWORD, auth.username, auth.password):
            logging.warning("Request denied - unauthorized - IP Address: {}".format(request.remote_addr))
            message = 'Authentication Required'
            resp = jsonify(message)
            resp.status_code = 401
            return resp
        return f(*args, **kwargs)
    return decorated


@application.route('/vips/icbc/drivers/<bcdl_number>', methods=['GET'])
@basic_auth_required
def driver(bcdl_number):
    if request.method == 'GET':
        try:
            drivers = _load_json_into_dict('python/icbc_mock_svc/data/drivers.json')
            return make_response(jsonify(drivers[bcdl_number]), 200)
        except Exception as e:
            return make_response(jsonify({
              "error": {
                "code": "404",
                "message": "Not Found",
                "description": "The resource specified in the request was not found",
                "request_uri": "/drivers/" + bcdl_number,
                "request_id": "03f11de1-4286-48cb-a8ef-e6e8776c5b60"
              }
            }), 404)


@application.route('/vips/icbc/vehicles', methods=['GET'])
@basic_auth_required
def vehicle():
    if request.method == 'GET':
        licence_plate = request.args.get('plateNumber')
        try:
            vehicles = _load_json_into_dict('python/icbc_mock_svc/data/vehicles.json')
            return make_response(jsonify(vehicles[licence_plate]), 200)
        except Exception as e:
            return make_response(jsonify({
                    "error": {
                        "code": 404,
                        "message": "Not Found",
                        "description": "vehicle not found",
                        "request_uri": "/vehicles?plateNumber="+licence_plate,
                        "request_id": "8b1e3c93-b977-463a-b54f-e6e8776c5e15"
                    }
                }), 404)


def _load_json_into_dict(file_name) -> dict:
    with open(file_name, 'r') as f:
        data = f.read()
    return json.loads(data)


def _check_credentials(username, password, username_submitted, password_submitted) -> bool:
    if username_submitted == username and password_submitted == password:
        return True
    logging.debug('credential mismatch: {}:{} | {}:{}'.format(username_submitted, username, password_submitted, password))
    return False


if __name__ == "__main__":
    application.run(host='0.0.0.0')
