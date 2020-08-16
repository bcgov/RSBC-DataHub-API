import requests
import logging
import json
import uuid


def query_get(prohibition_number: str, config, local_requests=requests):
    correlation_id = str(uuid.uuid4())
    endpoint = config.VIPS_API_ROOT_URI + prohibition_number + '/status/' + correlation_id
    logging.debug('vips_api_endpoint: {}'.format(endpoint))
    try:
        response = local_requests.get(endpoint, auth=(config.VIPS_API_USER, config.VIPS_API_PASS))
    except AssertionError as error:
        logging.warning('no response from the VIPS API')
        return False, error

    data = response.json()
    # Note: VIPS response could be either record found or record not found
    logging.info('VIPS API response: {} correlation_id: {}'.format(json.dumps(data), correlation_id))
    return True, data


def store(message: dict, config, local_requests=requests):
    pass
