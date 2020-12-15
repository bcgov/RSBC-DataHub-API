from python.common.message import encode_message
from python.writer.config import Config
import requests
import logging
import copy
import re
import json

logging.basicConfig(level=Config.LOG_LEVEL, format=Config.LOG_FORMAT)


def publish_to_fail_queue(**args) -> tuple:
    config = args.get('config')
    message_with_errors = args.get('message')
    writer = args.get('writer')
    is_success = writer.publish(config.FAIL_QUEUE, encode_message(message_with_errors, config.ENCRYPT_KEY))
    return is_success, args


def get_address_from_message(**args) -> tuple:
    m = args.get('message')
    event_type = m['event_type']
    args['address_raw'] = m[event_type]['violation_highway_desc'] + ", " + m[event_type]['violation_city_name']
    args['business_id'] = m[event_type]['ticket_number']
    return True, args


def clean_up_address(**args) -> tuple:
    # make a copy so we don't change the original
    address_raw = args.get('address_raw')
    address = copy.copy(address_raw)
    logging.info('raw address {}'.format(address))
    address = address.replace('\r\n', '\n')
    address = re.sub(r'^[NEWS]/B', '', address)
    address = re.sub(r'&amp;', ' AND ', address)
    address = re.sub(r'\s+S/O\s+', ' AND ', address)
    address = re.sub(r'\s+SOUTH OF\s+', ' AND ', address)
    address = re.sub(r'\s+N/O\s+', ' AND ', address)
    address = re.sub(r'\s+NORTH OF\s+', ' AND ', address)
    address = re.sub(r'\s+W/O\s+', ' AND ', address)
    address = re.sub(r'\s+WEST OF\s+', ' AND ', address)
    address = re.sub(r'\s+E/O\s+', ' AND ', address)
    address = re.sub(r'\s+EAST OF\s+', ' AND ', address)
    address = address.replace('/', ' AND ')
    address = address.replace('+', ' AND ')
    address = address.replace('@', ' AND ')
    address = address.replace(' AT ', ' AND ')
    address = address.replace('#', ' ')
    address = re.sub(r'\s+-\s+', ' AND ', address)
    address = address.replace(' NB', '')
    address = address.replace(' SB', '')
    address = address.replace(' EB', '')
    address = address.replace(' WB', '')
    address = re.sub(r'\s+BLK\s+', ' ', address)
    address = re.sub(r'\s+BLOCK\s+', ' ', address)
    address = address.replace('HIGHWAY', 'HWY')
    address = address.replace('TRANS CANADA HWY', 'TRANS-CANADA HWY')
    address = address.replace('PAT BAY HWY', 'PATRICIA BAY HWY')
    address = re.sub(r'HWY\s+1([\s+|,])', r'TRANS-CANADA HWY\g<1>', address)
    address = re.sub(r'HWY\sONE([\s+|,])', r'TRANS-CANADA HWY\g<1>', address)
    address = re.sub(r'HWY\s?(\d+)', r'HWY-\g<1>', address)
    address = re.sub(r'HWY-(\d+)(\s?)(SOUTH|NORTH|EAST|WEST|[NEWS])', r'HWY-\g<1> ', address)
    address = re.sub(r'[^\S\r\n]{2,}', ' ', address)
    address = re.sub(r'^\s+', '', address)
    address = address + ", BC"
    logging.info('clean address {}'.format(address))
    args['address_clean'] = address
    return True, args


def build_payload_to_send_to_geocoder(**args) -> tuple:
    args['payload'] = dict({
        "address": args.get('address_clean')
    })
    return True, args


def callout_to_geocoder_api(**args) -> tuple:
    config = args.get('config')
    endpoint = config.GEOCODER_API_URI
    payload = args.get('payload')
    logging.debug('Geocoder endpoint: {}'.format(endpoint))
    try:
        response = requests.post(endpoint,
                                 json=payload,
                                 auth=(config.GEOCODE_BASIC_AUTH_USER, config.GEOCODE_BASIC_AUTH_PASS))
    except requests.ConnectionError as error:
        logging.warning('no response from the Geocoder API: {}'.format(error))
        return False, args

    if response.status_code != 200:
        error_message_string = response.text
        logging.warning('response from the Geocoder API: {}'.format(error_message_string))
        args['error_message_string'] = error_message_string
        return False, args

    data = response.json()
    logging.debug('Response from RSI Geocoder: {}'.format(json.dumps(data)))
    args['geocoder_response'] = data
    return True, args


def transform_geocoder_response(**args) -> tuple:
    """
    Transform the response from the Geocoder API into a format
    required by the BI geolocation table
    """
    business_id = args.get('business_id')
    geocoder = args.get('geocoder_response')
    args['geolocation'] = dict({
        "business_program": "ETK",
        "business_type": "violation",
        "business_id": business_id,
        "long": str(geocoder['data_bc']['lon']),
        "lat": str(geocoder['data_bc']['lat']),
        "precision": geocoder['data_bc']['precision'],
        "requested_address": args.get('address_raw'),
        "submitted_address": args['address_clean'],
        "databc_long": str(geocoder['data_bc']['lon']),
        "databc_lat": str(geocoder['data_bc']['lat']),
        "databc_score": str(geocoder['data_bc']['score']),
        "databc_precision": geocoder['data_bc']['precision'],
        "full_address": geocoder['data_bc']['full_address'],
        "faults": json.dumps(geocoder['data_bc']['faults'])
    })
    logging.info("DataBC score: {} precision: {} faults: {}".format(
        geocoder['data_bc']['score'],
        geocoder['data_bc']['precision'],
        geocoder['data_bc']['faults'],
    ))
    return True, args


def add_geolocation_data_to_message(**args) -> tuple:
    message = args.get('message')
    geolocation = args.get('geolocation')
    event_type = message['event_type']
    message[event_type]['geolocation'] = geolocation
    args['message'] = message
    logging.info("added geolocation data to the message")
    return True, args
