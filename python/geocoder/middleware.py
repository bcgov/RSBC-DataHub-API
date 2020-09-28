import logging
import re
from python.geocoder.config import Config


logging.basicConfig(level=Config.LOG_LEVEL)


def retrieve_address_data(**args) -> tuple:
    request = args.get('request')
    payload = request.json
    address_raw = payload.get('address', None)
    if address_raw is not None:
        args['address_raw'] = address_raw
        return True, args
    error = 'no address submitted'
    args['error_string'] = error
    logging.info(error)
    return False, args


def validate_address_data(**args) -> tuple:
    address_raw = args.get('address_raw')
    if 10 < len(address_raw) < 150:
        return True, args
    error = 'address submitted is either too long or too short'
    args['error_string'] = error
    logging.info(error)
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
    logging.info(error)
    return False, args


def clean_up_address(**args) -> tuple:
    address = args.get('address_raw')
    logging.info('raw address {}'.format(address))
    address = address.replace('\r\n', '\n')
    address = address.replace('/', ' AND ')
    address = address.replace('+', ' AND ')
    address = address.replace('@', ' AND ')
    address = address.replace(' AT ', ' AND ')
    address = address.replace('#', '')
    address = address.replace(' NB', '')
    address = address.replace(' SB', '')
    address = address.replace(' EB', '')
    address = address.replace(' WB', '')
    address = address.replace(' BLOCK', ' BLK')
    address = address.replace('HIGHWAY', 'HWY')
    address = address.replace('\bTRANS-CANADA\b', 'TRANS CANADA')
    address = address.replace('TRANS CANADA HWY', 'BC-1')
    address = address.replace('\bTRANS CANADA\b', 'BC-1')
    address = address.replace('\bTCH', 'BC-1')
    address = address.replace('ISLAND HWY', 'BC-1')
    address = address.replace('PAT BAY HWY', 'PATRICIA BAY HWY')
    address = address.replace('PATRICIA BAY HWY', 'BC-17')
    address = re.sub(r'HWY\s(\d)', r'BC-\g<1>', address)
    address = re.sub(r'[^\S\r\n]{2,}', ' ', address)
    address = re.sub(r'^\s+', '', address)
    logging.info('clean address {}'.format(address))
    args['address_clean'] = address
    return True, args


def generate_data_bc_only_response(**args) -> tuple:
    args['response'] = dict({
        "is_success": True,
        "address_raw": args.get('address_raw'),
        "address_clean": args.get('address_clean'),
        "data_bc": args.get('data_bc'),
    })
    return True, args


def generate_google_and_data_bc_response(**args) -> tuple:
    args['response'] = dict({
        "is_success": True,
        "address_raw": args.get('address_raw'),
        "address_clean": args.get('address_clean'),
        "data_bc": args.get('data_bc'),
        "google": args.get('google')
    })
    return True, args


def generate_data_bc_revert_response(**args) -> tuple:
    """
    This response is used when Google response doesn't deliver
    a satisfactory score and we revert to the DataBC coordinates
    """
    args['response'] = dict({
        "is_success": True,
        "address_raw": args.get('address_raw'),
        "address_clean": args.get('address_clean'),
        "data_bc": args.get('data_bc'),
        "google": args.get('google')
    })
    return True, args

