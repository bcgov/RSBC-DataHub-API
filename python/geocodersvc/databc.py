import logging
import requests
import json
from python.geocodersvc.config import Config

logging.basicConfig(level=Config.LOG_LEVEL, format=Config.LOG_FORMAT)


def send_query(**args) -> tuple:
    config = args.get('config')
    try:
        # create query string and execute request
        # request's "params" url encodes the address string
        headers = {'apikey': config.DATA_BC_API_KEY}
        params = {'addressString': args.get('address_raw')}
        response = requests.get(config.DATA_BC_API_URL + '/addresses.geojson',
                                params=params,
                                headers=headers,
                                timeout=5)
    except requests.exceptions.ReadTimeout as error:
        logging.warning('response from DataBC took too long')
        return False, args
    except requests.exceptions.ConnectionError as error:
        logging.warning('no response from the DataBC API')
        return False, args
    if response.status_code == 200:
        args['data_bc_raw'] = response.json()
        logging.debug('response headers: {}'.format(response.headers))
        return True, args
    error = 'DataBC did not return a successful response'
    args['error_string'] = error
    logging.error(error)
    return False, args


def is_response_valid(**args) -> tuple:
    data_bc_raw = args.get('data_bc_raw')
    try:
        coordinates = data_bc_raw['features'][0]['geometry']['coordinates']
        args['data_bc'] = dict({
            "score": data_bc_raw['features'][0]['properties']['score'],
            "precision": data_bc_raw['features'][0]['properties']['matchPrecision'],
            "full_address": data_bc_raw['features'][0]['properties']['fullAddress'],
            "faults": data_bc_raw['features'][0]['properties']['faults'],
            "lat": coordinates[1],
            "lon": coordinates[0]
        })
        logging.debug("faults: {}".format(json.dumps(data_bc_raw['features'][0]['properties']['faults'])))
    except (AttributeError, IndexError) as error:
        error_string = 'response from DataBC did not match expected format'
        args['error_string'] = error_string
        logging.warning(error_string)
        return False, args
    return True, args


def is_confidence_too_low(**args) -> tuple:
    config = args.get('config')
    data_bc = args.get('data_bc')
    logging.debug('Sent DataBC: {} which returned a score of: {}'.format(args.get("address_raw"), data_bc['score']))
    if data_bc['score'] < config.MIN_CONFIDENCE_SCORE:
        return True, args
    return False, args
