import logging
import json
import requests
from flask import make_response
import base64
from python.prohibition_web_svc.config import Config


def get_ingestor_api_authorization_header(**kwargs) -> tuple:
    username = kwargs.get('username')
    try:
        encoded_bytes = base64.b64encode("{}:{}".format(Config.FLASK_BASIC_AUTH_USER, Config.FLASK_BASIC_AUTH_PASS).encode('utf-8'))
        kwargs['ingestor_header'] = {
            "Authorization": 'Basic {}'.format(str(encoded_bytes, "utf-8")),
            "Content-Type": "application/json",
            "loginUserId": username
        }
    except Exception as e:
        logging.warning("error creating Ingestor authorization header")
        return False, kwargs
    return True, kwargs




def send_to_ingestor(**kwargs) -> tuple:
    
    try:
        payload = json.dumps(kwargs['icbc_payload'])
        url = "{}/v1/publish/event/etk".format(Config.INGESTOR_URL)       
        ingestor_response = requests.post(url, data=payload, headers=kwargs['ingestor_header'])
        kwargs['response'] = make_response(ingestor_response.text, ingestor_response.status_code)
        
    except Exception as e:
        return False, kwargs
    return True, kwargs



