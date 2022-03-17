import logging
import requests
from datetime import datetime
from flask import make_response
import base64
from python.prohibition_web_svc.config import Config


def get_icbc_api_authorization_header(**kwargs) -> tuple:
    username = kwargs.get('username')
    try:
        encoded_bytes = base64.b64encode("{}:{}".format(Config.ICBC_API_USERNAME, Config.ICBC_API_PASSWORD).encode('utf-8'))
        kwargs['icbc_header'] = {
            "Authorization": 'Basic {}'.format(str(encoded_bytes, "utf-8")),
            "loginUserId": username
        }
    except Exception as e:
        logging.warning("error creating ICBC authorization header")
        return False, kwargs
    return True, kwargs


def get_icbc_driver(**kwargs) -> tuple:
    url = "{}/drivers/{}".format(Config.ICBC_API_ROOT, kwargs.get('dl_number'))
    try:
        icbc_response = requests.get(url, headers=kwargs.get('icbc_header'))
        kwargs['response'] = make_response(icbc_response.json(), icbc_response.status_code)
    except Exception as e:
        return False, kwargs
    return True, kwargs


def get_icbc_vehicle(**kwargs) -> tuple:
    url = "{}/vehicles".format(Config.ICBC_API_ROOT)
    url_parameters = {
        "plateNumber": kwargs.get('plate_number'),
        # TODO - removed effectiveDate for debugging purposes
        # "effectiveDate": datetime.now().astimezone().replace(microsecond=0).isoformat()
    }
    try:
        icbc_response = requests.get(url, headers=kwargs.get('icbc_header'), params=url_parameters)
        logging.warning("icbc url:" + icbc_response.url)
        kwargs['response'] = make_response(icbc_response.json(), icbc_response.status_code)
    except Exception as e:
        return False, kwargs
    return True, kwargs


def is_request_not_seeking_test_plate(**kwargs) -> tuple:
    config = kwargs.get('config')
    logging.debug("Environment: " + config.ENVIRONMENT)
    if config.ENVIRONMENT == 'prod':
        # Never return the test plate in PROD
        return True, kwargs
    plate_number = kwargs.get('plate_number')
    return plate_number != 'ICBC', kwargs


def splunk_get_driver(**kwargs) -> tuple:
    kwargs['splunk_data'] = {
        "event": "icbc_get_driver",
        "username": kwargs.get('username'),
        "user_guid": kwargs.get('user_guid'),
        "queried_bcdl": kwargs.get("dl_number")
    }
    return True, kwargs


def splunk_get_vehicle(**kwargs) -> tuple:
    kwargs['splunk_data'] = {
        "event": "icbc_get_vehicle",
        "username": kwargs.get('username'),
        "user_guid": kwargs.get('user_guid'),
        "queried_plate": kwargs.get('plate_number')
    }
    return True, kwargs
