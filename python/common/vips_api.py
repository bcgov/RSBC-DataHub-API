import requests
import logging
import json
import uuid
import python.common.prohibitions as pro
from datetime import datetime, timedelta
from iso8601 import parse_date
from unicodedata import normalize
from python.common.config import Config
import base64

logging.basicConfig(level=Config.LOG_LEVEL)


def list_of_dates_between(start: datetime, end: datetime) -> list:
    results = list()
    delta = end - start
    for i in range(delta.days + 1):
        day = start + timedelta(days=i)
        results.append(day.strftime("%Y-%m-%d"))
    return results


def status_get(prohibition_id: str, config, correlation_id: str) -> tuple:
    """
    Call out to the VIPS API and return the prohibition status
    """
    endpoint = build_endpoint(config.VIPS_API_ROOT_URL, prohibition_id, 'status', correlation_id)
    is_response_successful, data = get(endpoint, config.VIPS_API_USERNAME, config.VIPS_API_PASSWORD, correlation_id)
    is_success = 'resp' in data and data['resp'] == 'success'
    if is_success:
        return True, data['data']['status']
    return False, data['error']


def disclosure_get(document_id: str, config, correlation_id: str):
    endpoint = build_endpoint(config.VIPS_API_ROOT_URL, document_id, 'disclosure', correlation_id)
    return get(endpoint, config.VIPS_API_USERNAME, config.VIPS_API_PASSWORD, correlation_id)


def payment_get(prohibition_id: str, config, correlation_id: str):
    endpoint = build_endpoint(config.VIPS_API_ROOT_URL, prohibition_id, 'payment', 'status', correlation_id)
    return get(endpoint, config.VIPS_API_USERNAME, config.VIPS_API_PASSWORD, correlation_id)


def payment_patch(prohibition_id: str, config, correlation_id: str, **args):
    logging.info('inside payment_patch()')
    endpoint = build_endpoint(config.VIPS_API_ROOT_URL, prohibition_id, 'payment', correlation_id)
    vips_date_string = vips_datetime(args.get('receipt_date'))
    payload = {
            "transactionInfo": {
                "paymentCardType": args.get('card_type'),
                "paymentAmount": args.get('receipt_amount'),
                "paymentDate": vips_date_string,
                "receiptNumberTxt": args.get('receipt_number'),
            }
        }
    return patch(endpoint, config.VIPS_API_USERNAME, config.VIPS_API_PASSWORD, payload, correlation_id)


def application_get(application_id: str, config, correlation_id: str) -> tuple:
    endpoint = build_endpoint(config.VIPS_API_ROOT_URL, application_id, 'application', correlation_id)
    is_success, data = get(endpoint, config.VIPS_API_USERNAME, config.VIPS_API_PASSWORD, correlation_id)
    if is_success and "data" in data and 'applicationInfo' in data['data']:
        return True, data['data']['applicationInfo']
    return False, data


def application_create(form_type: str, prohibition_id: str, config, correlation_id: str, **args):
    endpoint = build_endpoint(config.VIPS_API_ROOT_URL, form_type, prohibition_id, 'application', correlation_id)
    payload = {
        "applicationInfo": {
            "email": args.get('email'),
            "faxNo": args.get('fax', ''),
            "firstGivenNm": args.get('first_name'),
            "formData": args.get('form_date'),
            "manualEntryYN": args.get('manual_entry', 'N'),
            "noticeSubjectCd": args.get('notice_subject_type', 'PERS'),
            "phoneNo": args.get('phone'),
            "presentationTypeCd": args.get('presentation_type'),
            "reviewRoleTypeCd": args.get('applicant_role'),
            "secondGivenNm": args.get('middle_name'),
            "surnameNm": args.get('last_name'),
        }
    }
    return create(endpoint, config.VIPS_API_USERNAME, config.VIPS_API_PASSWORD, payload, correlation_id)


def application_update(guid: str, config, correlation_id: str):
    endpoint = build_endpoint(config.VIPS_API_ROOT_URL, guid, 'application', correlation_id)
    return get(endpoint, config.VIPS_API_USERNAME, config.VIPS_API_PASSWORD, correlation_id)


def schedule_get(notice_type_code: str, review_date: str, config) -> tuple:
    correlation_id = generate_correlation_id()
    endpoint = build_endpoint(
        config.VIPS_API_ROOT_URL,
        notice_type_code,
        "ORAL",
        review_date,
        'review',
        'availableTimeSlot',
        correlation_id)
    logging.debug("get VIPS schedule endpoint: {}".format(endpoint))
    is_successful, data = get(endpoint, config.VIPS_API_USERNAME, config.VIPS_API_PASSWORD, correlation_id)
    if is_successful and data['resp'] == 'success':
        return True, data
    logging.warning('Cannot GET VIPS schedule: {}'.format(json.dumps(data)))
    return False, {}


def health_get(config) -> tuple:
    endpoint = build_endpoint(config.VIPS_API_ROOT_URL, 'api', 'utility', 'ping')
    return get(endpoint, config.VIPS_API_USERNAME, config.VIPS_API_PASSWORD)


def build_endpoint(*args) -> str:
    delimiter = '/'
    return delimiter.join(args)


def get(endpoint: str, user: str, password: str, correlation_id='ABC') -> tuple:
    logging.debug('vips_get_api_endpoint: {}'.format(endpoint))
    try:
        response = requests.get(endpoint, auth=(user, password))
    except AssertionError as error:
        logging.warning('no response from the VIPS API')
        return False, error

    data = response.json()
    # Note: VIPS response could be either record found or record not found
    logging.debug('VIPS API response: {} correlation_id: {}'.format(json.dumps(data), correlation_id))
    return 'resp' in data, data


def create(endpoint: str, user: str, password: str,  payload: dict, correlation_id='ABC') -> tuple:
    logging.info('create endpoint: {}'.format(endpoint))
    logging.info('create payload: {}'.format(json.dumps(payload)))
    try:
        response = requests.post(endpoint, json=payload, auth=(user, password))
    except AssertionError as error:
        logging.warning('no response from the VIPS API')
        return False, error

    data = response.json()
    logging.info('VIPS API response: {} correlation_id: {}'.format(json.dumps(data), correlation_id))
    return response.status_code == 200, data


def patch(endpoint: str, user: str, password: str,  payload: dict, correlation_id='ABC') -> tuple:
    logging.info('patch endpoint: {}'.format(endpoint))
    logging.info('patch payload: {}'.format(json.dumps(payload)))
    try:
        response = requests.patch(endpoint, json=payload, auth=(user, password))
    except AssertionError as error:
        logging.warning('no response from the VIPS API')
        return False, error

    data = response.json()
    logging.info('VIPS API patch response: {} correlation_id: {}'.format(json.dumps(data), correlation_id))
    return response.status_code == 200, data


def remove_accents(input_str):
    nfkd_form = normalize('NFKD', input_str)
    only_ascii = nfkd_form.encode('ASCII', 'ignore')
    return only_ascii


def is_last_name_match(vips_last_name: dict, last_name: str) -> bool:
    logging.debug('compare last name: {} and {}'.format(vips_last_name, last_name))
    return bool(remove_accents(vips_last_name).upper() == remove_accents(last_name).upper())


def has_been_paid(vips_payment_status: dict) -> tuple:
    is_paid = 'data' in vips_payment_status and 'transactionInfo' in vips_payment_status['data']
    valid_response = 'resp' in vips_payment_status
    return valid_response, is_paid


def vips_str_to_datetime(vips_date_time: str) -> datetime:
    """
    This utility takes a VIPS datetime string and
    converts it to a Python datetime object.
    VIPS uses a non-standard datetime format.
    Like this: 2019-01-02 17:30:00 -08:00
    """
    date_string = vips_date_time[0:10]
    time_string = vips_date_time[11:19]
    offset_hour = vips_date_time[20:23]
    offset_minute = vips_date_time[24:26]
    iso8601_string = "{}T{}{}:{}".format(date_string, time_string, offset_hour, offset_minute)
    return parse_date(iso8601_string)


def vips_str_to_friendly_time(vips_date_time: str) -> str:
    """
    This function returns a friendly time "10:00am" when
    given a VIPS date_time string
    """
    # TODO - test to make sure this works correctly
    #  over a change to / from daylight savings time
    date_time_object = vips_str_to_datetime(vips_date_time)
    return date_time_object.strftime("%-I:%M%p")


def _time_slot_to_friendly_time(time_slot: dict) -> dict:
    start_time = time_slot['reviewStartDtm']
    end_time = time_slot['reviewEndDtm']
    return {
        "label": "{} to {}".format(
            vips_str_to_friendly_time(start_time),
            vips_str_to_friendly_time(end_time)),
        "value": encode_time_slot(time_slot)
    }


def encode_time_slot(time_slot: dict) -> str:
    start_time = time_slot['reviewStartDtm']
    end_time = time_slot['reviewEndDtm']
    return bytes.decode(base64.b64encode(str.encode(start_time + "|" + end_time)))


def decode_time_slot(encode_string: str) -> dict:
    decoded_bytes = base64.b64decode(encode_string)
    start_end = bytes.decode(decoded_bytes).split("|")
    return {
        "reviewStartDtm": start_end[0],
        "reviewEndDtm": start_end[1]
    }


def schedule_to_friendly_times(time_slots: dict) -> list:
    """
    This function takes a list of timeslots as returned
    by VIPS GET schedule and returns a list of
    dictionary objects with friendly labels and base64
    encoded VIPS date time string
    {
        label: "10:00am to 11:30am"
        value: "ZGF0YSB0byBiZSBlbmNvZGVk"
    }
    """
    return list(map(_time_slot_to_friendly_time, time_slots))


def vips_datetime(date_time: datetime) -> str:
    """
    This utility takes a Python datetime object and
    converts it to a datetime string for VIPS.
    VIPS uses a non-standard datetime format.
    Like this: 2019-01-02 17:30:00 -08:00
    """
    dt_string = date_time.strftime("%Y-%m-%d %H:%M:%S %z")
    return dt_string[0:23] + ':' + dt_string[23:25]


def generate_correlation_id():
    return str(uuid.uuid4())
