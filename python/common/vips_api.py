import requests
import logging
import json


def get_prohibition(prohibition_number, config, local_requests=requests):
    try:
        response = local_requests.get(config.VIPS_API_ROOT_URI + prohibition_number + '/status')
    except AssertionError as error:
        logging.warning('no response from the VIPS API')
        return False, error

    data = response.json()
    if data['resp'] == 'fail':
        logging.warning('VIPS API response: ' + json.dumps(data))
        return False, data
    
    return True, data
