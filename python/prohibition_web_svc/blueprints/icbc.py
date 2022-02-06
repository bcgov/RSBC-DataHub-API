from python.prohibition_web_svc.config import Config
from python.prohibition_web_svc.business.keycloak_logic import get_authorized_keycloak_user
import python.prohibition_web_svc.middleware.icbc_middleware as icbc_middleware
import python.prohibition_web_svc.http_responses as http_responses
import python.common.splunk as splunk
from python.common.helper import middle_logic
from flask import request, Blueprint
from flask_cors import CORS
import logging.config

logging.config.dictConfig(Config.LOGGING)
logging.info('*** icbc blueprint loaded ***')

bp = Blueprint('icbc', __name__, url_prefix='/api/v1/icbc')
CORS(bp, resources={"/api/v1/icbc/*": {"origins": Config.ACCESS_CONTROL_ALLOW_ORIGIN}})


@bp.route('/drivers/<string:dl_number>', methods=['GET'])
def get_driver(dl_number):
    if request.method == 'GET':
        kwargs = middle_logic(
            get_authorized_keycloak_user() + [
                {"try": icbc_middleware.get_icbc_api_authorization_header, "fail": [
                    {"try": http_responses.server_error_response, "fail": []},
                ]},
                {"try": icbc_middleware.is_request_not_seeking_test_drivers_licence, "fail": [
                    {"try": icbc_middleware.get_test_driver, "fail": []},
                    {"try": http_responses.successful_get_response, "fail": []},
                ]},
                {"try": icbc_middleware.get_icbc_driver, "fail": [
                    {"try": http_responses.server_error_response, "fail": []},
                ]},
                {"try": splunk.icbc_get_driver, "fail": []}
            ],
            required_permission='driver-get',
            dl_number=dl_number,
            request=request,
            config=Config)
        return kwargs.get('response')


@bp.route('/vehicles/<string:plate_number>', methods=['GET'])
def get_vehicle(plate_number):
    if request.method == 'GET':
        kwargs = middle_logic(
            get_authorized_keycloak_user() + [
                {"try": icbc_middleware.get_icbc_api_authorization_header, "fail": [
                    {"try": http_responses.server_error_response, "fail": []},
                ]},
                {"try": icbc_middleware.is_request_not_seeking_test_plate, "fail": [
                    {"try": icbc_middleware.get_test_plate, "fail": []},
                    {"try": http_responses.successful_get_response, "fail": []},
                ]},
                {"try": icbc_middleware.get_icbc_vehicle, "fail": [
                    {"try": http_responses.server_error_response, "fail": []},
                ]},
                {"try": splunk.icbc_get_vehicle, "fail": []}
            ],
            required_permission='vehicle-get',
            plate_number=plate_number.upper(),
            request=request,
            config=Config)
        return kwargs.get('response')

