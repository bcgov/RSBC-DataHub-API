from python.prohibition_web_svc.config import Config
from python.common.helper import middle_logic
from python.prohibition_web_svc.business.keycloak_logic import get_authorized_keycloak_user
import python.prohibition_web_svc.http_responses as http_responses
import python.prohibition_web_svc.middleware.splunk_middleware as splunk_middleware
from flask import request, make_response, Blueprint
from python.common.splunk import log_to_splunk
from flask_cors import CORS

import logging.config
import python.common.helper as helper
from flask import jsonify

logging.config.dictConfig(Config.LOGGING)
logging.info('*** static blueprint loaded ***')

bp = Blueprint('static', __name__, url_prefix=Config.URL_PREFIX + '/api/v1')
CORS(bp, resources={Config.URL_PREFIX + "/api/v1/static/*": {"origins": Config.ACCESS_CONTROL_ALLOW_ORIGIN}})


@bp.route('/static/<string:resource>', methods=['GET'])
def index(resource):
    """
    List all static ids
    """
    if request.method == 'GET':
        kwargs = middle_logic([
              {"try": _is_not_configuration, "fail": [
                  {"try": splunk_middleware.log_static_get, "fail": []},
                  {"try": _get_configuration, "fail": [
                      {"try": http_responses.server_error_response, "fail": []},
                  ]},
                  {"try": log_to_splunk, "fail": []},
              ]},
              {"try": _is_not_keycloak, "fail": [
                  {"try": splunk_middleware.log_static_get, "fail": []},
                  {"try": _get_keycloak, "fail": [
                      {"try": http_responses.server_error_response, "fail": []},
                  ]},
                  {"try": log_to_splunk, "fail": []},
              ]},
              {"try": splunk_middleware.log_static_get, "fail": []},
              {"try": _is_known_resource, "fail": [
                  {"try": http_responses.bad_request_response, "fail": []},
              ]},
              {"try": _is_resource_agencies, "fail": [
                  {"try": _get_resource, "fail": [
                      {"try": http_responses.server_error_response, "fail": []},
                  ]},
                  {"try": log_to_splunk, "fail": []},
              ]},
              {"try": _get_agencies, "fail": [
                  {"try": http_responses.server_error_response, "fail": []},
              ]},
              {"try": log_to_splunk, "fail": []},
            ],
            resource=resource,
            required_permission='static-get',
            request=request,
            config=Config)
        return kwargs.get('response')


@bp.route('/static/<string:resource>/<string:static_id>', methods=['GET'])
def get(resource, static_id):
    if request.method == 'GET':
        return make_response({"error": "method not implemented"}, 405)


@bp.route('/static/<string:resource>', methods=['POST'])
def create(resource):
    if request.method == 'POST':
        return make_response({"error": "method not implemented"}, 405)


@bp.route('/static/<string:resource>/<string:static_id>', methods=['PATCH'])
def update(resource, static_id):
    if request.method == 'PATCH':
        return make_response({"error": "method not implemented"}, 405)


def _get_agencies(**kwargs) -> tuple:
    resource = kwargs.get('resource')
    try:
        data = helper.load_json_into_dict('python/prohibition_web_svc/data/agencies.json'.format(resource))
        kwargs['response'] = make_response(data, 200)
        # static = helper.load_json_into_dict('python/prohibition_web_svc/data/agencies.json')
        # ids = [o['id'] for o in static]
        # kwargs['response'] = make_response(jsonify(ids), 200)
        return True, kwargs
    except Exception as e:
        logging.warning("error getting static data")
        return False, kwargs


def _get_keycloak(**kwargs) -> tuple:
    config = {
        "realm": Config.KEYCLOAK_REALM,
        "url": Config.KEYCLOAK_AUTH_URL,
        "clientId": Config.KEYCLOAK_CLIENT_ID
    }
    kwargs['response'] = make_response(config, 200)
    return True, kwargs


def _is_known_resource(**kwargs) -> tuple:
    known_resources = [
        'agencies',
        'cities',
        'countries',
        'impound_lot_operators',
        'jurisdictions',
        'keycloak',
        'provinces',
        'vehicle_styles',
        'vehicles',
    ]
    return kwargs.get('resource') in known_resources, kwargs


def _is_resource_agencies(**kwargs) -> tuple:
    return kwargs.get('resource') == 'agencies', kwargs


def _is_not_keycloak(**kwargs) -> tuple:
    return kwargs.get('resource') != 'keycloak', kwargs


def _is_not_configuration(**kwargs) -> tuple:
    return kwargs.get('resource') != 'configuration', kwargs


def _get_configuration(**kwargs) -> tuple:
    config = {
        "environment": Config.ENVIRONMENT,
    }
    kwargs['response'] = make_response(config, 200)
    return True, kwargs


def _get_resource(**kwargs) -> tuple:
    resource = kwargs.get('resource')
    try:
        data = helper.load_json_into_dict('python/prohibition_web_svc/data/{}.json'.format(resource))
        kwargs['response'] = make_response(data, 200)
        return True, kwargs
    except Exception as e:
        logging.warning("error getting {} data".format(resource))
        return False, kwargs
