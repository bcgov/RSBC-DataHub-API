from flask import jsonify, Response
import logging


def ready_response(**args) -> tuple:
    args['response'] = Response(status=200)
    return True, args


def failed_validation(**args) -> tuple:
    # Note: business rule requires 500 returned when validation fails
    logging.warning("failed validation")
    args['error_string'] = 'failed validation'
    return _common_error_function(500, **args)


def not_json(**args) -> tuple:
    # Note: business rule requires 500 returned when validation fails
    error_string = 'not json'
    args['error_string'] = error_string
    logging.warning(error_string)
    return _common_error_function(500, **args)


def server_error(**args) -> tuple:
    args['error_string'] = 'something went wrong'
    return _common_error_function(500, **args)


def database_error(**args) -> tuple:
    args['error_string'] = 'error writing to the database'
    return _common_error_function(500, **args)


def geocoder_error(**args) -> tuple:
    return _common_error_function(500, **args)


def okay(**args) -> tuple:
    args['response'] = jsonify({"success": True}), 200
    return True, args


def _common_error_function(http_status_code: int, **args) -> tuple:
    error_string = args.get('error_string')
    args['response'] = jsonify({"error": error_string}), http_status_code
    return False, args

