import requests
import logging
import json
import uuid


def get_prohibition(prohibition_number: str, config, local_requests=requests):
    correlation_id = str(uuid.uuid4())
    endpoint = config.VIPS_API_ROOT_URI + prohibition_number + '/status/' + correlation_id
    logging.debug('vips_api_endpoint: ', endpoint)
    try:
        response = local_requests.get(endpoint, auth=(config.VIPS_API_USER, config.VIPS_API_PASS))
    except AssertionError as error:
        logging.warning('no response from the VIPS API')
        return False, error

    data = response.json()
    if data['resp'] == 'fail':
        logging.warning('VIPS API error: ', json.dumps(data), correlation_id)
        return False, data
    logging.info('VIPS API success', json.dumps(data), correlation_id)
    return True, data
