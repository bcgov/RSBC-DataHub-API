import python.common.helper as helper
from python.geocoder.config import Config
import python.geocoder.business as business
from flask import request, jsonify, Response, g, Flask
import logging
from functools import wraps


application = Flask(__name__)
application.secret = Config.GEOCODE_SECRET_KEY
logging.basicConfig(level=Config.LOG_LEVEL)
logging.warning('*** geocoder initialized ***')


def basic_auth_required(f):
    """
    Decorator that implements basic auth when added to a route
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not helper.check_credentials(Config, auth.username, auth.password):
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


if __name__ == "__main__":
    application.run(host='0.0.0.0')
