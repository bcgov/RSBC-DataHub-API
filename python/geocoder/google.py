import logging
from python.geocoder.config import Config
import requests


logging.basicConfig(level=Config.LOG_LEVEL, format=Config.LOG_FORMAT)

# Minimum acceptable score threshold from Google
MIN_CONFIDENCE_SCORE = 55


def send_query(**args) -> tuple:
    config = args.get('config')
    try:
        # create query string and execute request
        params = {'key': config.GOOGLE_API_KEY, 'address': args.get('address')}
        response = requests.get(config.GOOGLE_API_ROOT_URL, params=params)
    except AssertionError as error:
        logging.warning('no response from the Google API')
        return False, error
    if response.status_code == 200:
        args['google_raw'] = response.json()
        return True, args
    error = 'Google did not return a successful response'
    args['error_string'] = error
    logging.info(error)
    return False, args


def is_response_valid(**args) -> tuple:
    google_raw = args.get('google_raw', dict)
    try:
        args['google'] = dict({
            "lat": google_raw['results'][0]['geometry']['location']['lat'],
            "lon": google_raw['results'][0]['geometry']['location']['lng'],
            "score": _get_google_score(google_raw['results'][0]['geometry']['location_type'])
        })
    except AttributeError as error:
        error_string = 'response from DataBC did not match expected format'
        args['error_string'] = error_string
        logging.info(error_string)
        return False, args
    return True, args


def is_confidence_too_low(**args) -> tuple:
    google_data = args.get('google')
    if google_data['score'] < MIN_CONFIDENCE_SCORE:
        logging.info('Google returned a score below the minimum threshold, calling alternative (if configured)')
        return True, args
    logging.info('Google returned a score above the minimum threshold')
    return False, args


def _get_google_score(location_type: str) -> int:
    """
    Convert Google location types to a numeric score
    See: https://developers.google.com/maps/documentation/geocoding/intro
    """
    data = {

        # "ROOFTOP" indicates that the returned result is a precise geocode for
        # which we have location information accurate down to street address precision.
        "ROOFTOP": 90,

        # "RANGE_INTERPOLATED" indicates that the returned result reflects an
        # approximation (usually on a road) interpolated between two precise
        # points (such as intersections). Interpolated results are generally
        # returned when rooftop geocodes are unavailable for a street address.
        "RANGE_INTERPOLATED": 70,

        # "GEOMETRIC_CENTER" indicates that the returned result is the geometric
        # center of a result such as a polyline (for example, a street) or polygon (region).
        "GEOMETRIC_CENTER": 60,

        # "APPROXIMATE" indicates that the returned result is approximate.
        "APPROXIMATE": 40

    }
    return data.get(location_type, -1)
