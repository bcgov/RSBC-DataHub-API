import python.common.helper as helper
from python.geocodersvc.config import Config
import python.geocodersvc.business as business
from flask import request, jsonify, Response, g, Flask
import logging
from functools import wraps


application = Flask(__name__)
application.secret = Config.GEOCODE_SECRET_KEY
logging.basicConfig(level=Config.LOG_LEVEL, format=Config.LOG_FORMAT)
logging.warning('*** geocoder ready for use ***')


def basic_auth_required(f):
    """
    Decorator that implements basic auth when added to a route
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not helper.check_credentials(
                Config.GEOCODE_BASIC_AUTH_USER, Config.GEOCODE_BASIC_AUTH_PASS, auth.username, auth.password):
            message = {'error': 'Unauthorized'}
            resp = jsonify(message)
            resp.status_code = 401
            return resp
        return f(*args, **kwargs)
    return decorated


@application.route('/address', methods=['POST'])
@basic_auth_required
def address():
    """
    Lookup lat/lon of street address using DataBC. If the DataBC's
    confidence score is below threshold determined in the config,
    check the address against Google's API and return both results.
    """
    if request.method == 'POST':
        # invoke middleware functions
        args = helper.middle_logic(business.geocode_address(),
                                   request=request,
                                   config=Config)
        return args.get('response')


@application.route('/ping', methods=['GET'])
def ping():
    """
    This endpoint displays whether or not the geocoder component is responding.
    """
    return jsonify("geocoder is ready"), 200


@application.route('/ready', methods=['GET'])
def ready():
    """
    This endpoint checks whether we can connect to the DataBC Geocoder
    """
    test_address = "4350 STILL CREEK, CHILLIWACK"
    results = helper.middle_logic(business.determine_ready_status(),
                                  config=Config,
                                  address_raw=test_address)
    return results.get('response')


if __name__ == "__main__":
    application.run(host='0.0.0.0')
