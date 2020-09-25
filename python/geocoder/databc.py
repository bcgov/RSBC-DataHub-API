import logging
import requests
from python.geocoder.config import Config

logging.basicConfig(level=Config.LOG_LEVEL)

# Minimum acceptable score threshold from DataBC; if below
# threshold, query will be sent to Google for processing
MIN_CONFIDENCE_SCORE = 55


def send_query(**args) -> tuple:
    config = args.get('config')
    try:
        # create query string and execute request
        # request's "params" url encodes the address string
        params = {'addressString': args.get('address_clean')}
        response = requests.get(config.DATA_BC_API_URL + '/addresses.geojson', params=params)
    except AssertionError as error:
        logging.warning('no response from the DataBC API')
        return False, error
    if response.status_code == 200:
        args['data_bc_raw'] = response.json()
        return True, args
    error = 'DataBC did not return a successful response'
    args['error_string'] = error
    logging.info(error)
    return False, args


def is_response_valid(**args) -> tuple:
    data_bc_raw = args.get('data_bc_raw')
    try:
        coordinates = data_bc_raw['features'][0]['geometry']['coordinates']
        args['data_bc'] = dict({
            "score": data_bc_raw['features'][0]['properties']['score'],
            "lat": coordinates[1],
            "lon": coordinates[0]
        })
    except AttributeError as error:
        error_string = 'response from DataBC did not match expected format'
        args['error_string'] = error_string
        logging.info(error_string)
        return False, args
    return True, args


def is_confidence_too_low(**args) -> tuple:
    data_bc = args.get('data_bc')
    if data_bc['score'] < MIN_CONFIDENCE_SCORE:
        logging.info('DataBC returned a score below the minimum threshold, calling alternative (if configured)')
        return True, args
    logging.info('DataBC returned a score above the minimum threshold: {}'.format(data_bc['score']))
    return False, args
