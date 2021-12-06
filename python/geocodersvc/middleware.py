import logging
import re
import json
from python.geocodersvc.config import Config


logging.basicConfig(level=Config.LOG_LEVEL, format=Config.LOG_FORMAT)


def content_type_is_json(**args) -> tuple:
    request = args.get('request')
    if request.content_type == 'application/json':
        return True, args
    error = 'received content type is not JSON'
    args['error_string'] = error
    logging.error(error)
    return False, args


def retrieve_address_data(**args) -> tuple:
    request = args.get('request')
    payload = request.json
    logging.debug("payload: " + json.dumps(payload))
    address_raw = payload.get('address', None)
    if address_raw is not None:
        args['address_raw'] = address_raw
        return True, args
    error = 'no address submitted'
    args['error_string'] = error
    logging.error(error)
    return False, args


def validate_address_data(**args) -> tuple:
    address_raw = args.get('address_raw')
    if 10 < len(address_raw) < 150:
        return True, args
    error = 'address submitted is either too long or too short'
    args['error_string'] = error
    logging.error(error)
    return False, args


def is_google_fail_over_enabled(**args) -> tuple:
    config = args.get('config')
    return config.GOOGLE_FAIL_OVER_ENABLED == 'TRUE', args


def is_google_api_key_provided(**args) -> tuple:
    config = args.get('config')
    if re.match(r"^[A-Z]|[0-9]|[a-z_]{30}$", config.GOOGLE_API_KEY) is None:
        return True, args
    error = ''
    args['error_string'] = error
    logging.error(error)
    return False, args


def generate_data_bc_only_response(**args) -> tuple:
    args['status_code'] = 200
    args['response'] = dict({
        "is_success": True,
        "address_raw": args.get('address_raw'),
        "data_bc": args.get('data_bc'),
    })
    return True, args


def generate_google_and_data_bc_response(**args) -> tuple:
    args['status_code'] = 200
    args['response'] = dict({
        "is_success": True,
        "address_raw": args.get('address_raw'),
        "data_bc": args.get('data_bc'),
        "google": args.get('google')
    })
    return True, args


def generate_data_bc_revert_response(**args) -> tuple:
    """
    This response is used when Google response doesn't deliver
    a satisfactory score and we revert to the DataBC coordinates
    """
    args['status_code'] = 200
    args['response'] = dict({
        "is_success": True,
        "address_raw": args.get('address_raw'),
        "data_bc": args.get('data_bc'),
        "google": args.get('google')
    })
    return True, args


def generate_error_response(**args) -> tuple:
    """
    This response is used when an error has occurred
    """
    args['status_code'] = 400
    args['response'] = dict({
        "is_success": False,
        "error": "DataBC is not responding"
    })
    return True, args

