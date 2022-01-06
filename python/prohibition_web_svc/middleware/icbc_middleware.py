import logging
import requests
from datetime import datetime
from flask import jsonify, make_response
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
    url = "{}/vehicles?plateNumber={}&effectiveDate={}".format(
        Config.ICBC_API_ROOT,
        kwargs.get('plate_number'),
        datetime.now().astimezone().replace(microsecond=0).isoformat()
    )
    logging.debug("icbc url:" + url)
    try:
        icbc_response = requests.get(url, headers=kwargs.get('icbc_header'))
        kwargs['response'] = make_response(icbc_response.json(), icbc_response.status_code)
    except Exception as e:
        return False, kwargs
    return True, kwargs


def is_request_not_seeking_test_plate(**kwargs) -> tuple:
    # TODO - remove before flight
    plate_number = kwargs.get('plate_number')
    return plate_number != 'ICBC', kwargs
