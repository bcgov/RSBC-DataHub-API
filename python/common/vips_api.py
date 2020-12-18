import requests
import logging
import json
import uuid
from datetime import datetime, timedelta
from iso8601 import parse_date
from unicodedata import normalize
from python.common.config import Config
import base64

logging.basicConfig(level=Config.LOG_LEVEL, format=Config.LOG_FORMAT)


def list_of_weekdays_dates_between(start: datetime, end: datetime) -> list:
    delta = timedelta(days=1)
    query_date = start
    results = list()
    while query_date <= end:
        day_of_week = query_date.strftime("%a")
        if not (day_of_week == "Sun" or day_of_week == "Sat"):
            results.append(query_date)
        query_date += delta
    return results


def next_business_date(date_time: datetime) -> datetime:
    delta = timedelta(days=1)
    next_day = date_time + delta
    while True:
        day_of_week = next_day.strftime("%a")
        if not (day_of_week == "Sun" or day_of_week == "Sat"):
            return next_day
        next_day += delta


def status_get(prohibition_id: str, config, correlation_id: str) -> tuple:
    """
    Call out to the VIPS API and return the prohibition status. Returns (True, data)
    if the callout to the API was successful.  Returns (False, data) if the call out
    to the API was unsuccessful.  For example, the API is down.
    """
    endpoint = build_endpoint(config.VIPS_API_ROOT_URL, prohibition_id, 'status', correlation_id)
    is_response_successful, data = get(endpoint, config.VIPS_API_USERNAME, config.VIPS_API_PASSWORD, correlation_id)
    if is_response_successful and 'resp' in data:
        return True, data
    return False, dict({})


def disclosure_get(document_id: str, config, correlation_id: str):
    endpoint = build_endpoint(config.VIPS_API_ROOT_URL, document_id, 'disclosure', correlation_id)
    is_response_successful, data = get(endpoint, config.VIPS_API_USERNAME, config.VIPS_API_PASSWORD, correlation_id)
    if 'resp' in data:
        return True, data
    return False, dict({})


def payment_get(prohibition_id: str, config, correlation_id: str):
    endpoint = build_endpoint(config.VIPS_API_ROOT_URL, prohibition_id, 'payment', 'status', correlation_id)
    is_response_successful, data = get(endpoint, config.VIPS_API_USERNAME, config.VIPS_API_PASSWORD, correlation_id)
    if 'resp' in data:
        return True, data
    return False, dict({})


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


def disclosure_patch(document_id: str, **args):
    config = args.get('config')
    correlation_id = args.get('correlation_id')
    today = args.get('today_date')
    logging.info('inside disclosure_patch()')
    endpoint = build_endpoint(config.VIPS_API_ROOT_URL, 'disclosure', correlation_id)
    payload = {
            "disclosure": {
                "disclosedDtm": vips_datetime(today),
                "documentId": document_id
            }
        }
    return patch(endpoint, config.VIPS_API_USERNAME, config.VIPS_API_PASSWORD, payload, correlation_id)


def application_get(application_id: str, config, correlation_id: str) -> tuple:
    endpoint = build_endpoint(config.VIPS_API_ROOT_URL, application_id, 'application', correlation_id)
    is_success, data = get(endpoint, config.VIPS_API_USERNAME, config.VIPS_API_PASSWORD, correlation_id)
    if is_success and "resp" in data:
        return True, data
    return False, data


def application_create(form_type: str, **args):
    config = args.get('config')
    correlation_id = args.get('correlation_id')
    prohibition_number = args.get('prohibition_number')
    endpoint = build_endpoint(config.VIPS_API_ROOT_URL, form_type, prohibition_number, 'application', correlation_id)
    payload = {
        "applicationInfo": {
            "email": args.get('applicant_email_address'),
            "phoneNo": args.get('applicant_phone_number'),
            "presentationTypeCd": args.get('presentation_type'),
            "reviewRoleTypeCd": args.get('applicant_role'),
            "firstGivenNm": args.get('applicant_first_name'),
            "surnameNm": args.get('applicant_last_name'),
            "formData": args.get('xml'),
            "manualEntryYN": 'N',
            "noticeSubjectCd": 'PERS',
        }
    }
    logging.info("application create payload: {}".format(json.dumps(payload)))
    return create(endpoint, config.VIPS_API_USERNAME, config.VIPS_API_PASSWORD, payload, correlation_id)


def application_update(guid: str, config, correlation_id: str):
    endpoint = build_endpoint(config.VIPS_API_ROOT_URL, guid, 'application', correlation_id)
    return get(endpoint, config.VIPS_API_USERNAME, config.VIPS_API_PASSWORD, correlation_id)


def schedule_get(notice_type: str, review_type: str, first_date: datetime, last_date: datetime, config, correlation_id):
    time_slots = list()
    number_review_days_offered = 0
    for query_date in list_of_weekdays_dates_between(first_date, last_date):
        query_date_string = query_date.strftime("%Y-%m-%d")
        endpoint = build_endpoint(
            config.VIPS_API_ROOT_URL,
            notice_type,
            review_type,
            query_date_string,
            'review',
            'availableTimeSlot',
            correlation_id)
        logging.info('check VIPS for time slots available on: {}'.format(query_date_string))
        is_successful, data = get(endpoint, config.VIPS_API_USERNAME, config.VIPS_API_PASSWORD, correlation_id)
        if is_successful:
            if data['resp'] == 'success' and len(data['data']['timeSlots']) > 0:
                number_review_days_offered += 1
                time_slots += time_slots_to_friendly_times(data['data']['timeSlots'], review_type)
    return True, dict({
        "time_slots": time_slots,
        "number_review_days_offered": number_review_days_offered
    })


def schedule_create(**args):
    config = args.get('config')
    correlation_id = args.get('correlation_id')
    prohibition_number = args.get('prohibition_number')
    endpoint = build_endpoint(config.VIPS_API_ROOT_URL, prohibition_number, 'review', 'schedule', correlation_id)
    payload = {
        "timeSlot": args.get('requested_time_slot')
    }
    logging.info("schedule create payload: {}".format(json.dumps(payload)))
    return create(endpoint, config.VIPS_API_USERNAME, config.VIPS_API_PASSWORD, payload, correlation_id)


def health_get(config) -> tuple:
    endpoint = build_endpoint(config.VIPS_API_ROOT_URL, 'api', 'utility', 'ping')
    return get(endpoint, config.VIPS_API_USERNAME, config.VIPS_API_PASSWORD)


def build_endpoint(*args) -> str:
    delimiter = '/'
    return delimiter.join(args)


def get(endpoint: str, user: str, password: str, correlation_id='ABC') -> tuple:
    logging.info('vips get api endpoint: {}'.format(endpoint))
    try:
        response = requests.get(endpoint, verify=False, auth=(user, password))
    except requests.ConnectionError as error:
        logging.warning('no response from the VIPS API: {}'.format(error))
        return False, dict()

    data = response.json()
    # Note: VIPS response could be either record found or record not found
    logging.debug('VIPS API response: {} correlation_id: {}'.format(json.dumps(data), correlation_id))
    return 'resp' in data, data


def create(endpoint: str, user: str, password: str,  payload: dict, correlation_id='ABC') -> tuple:
    try:
        response = requests.post(endpoint, verify=False, json=payload, auth=(user, password))
    except requests.ConnectionError as error:
        logging.warning('no response from the VIPS API: {}'.format(error))
        return False, dict()

    if response.status_code == 201 or response.status_code == 200:
        data = response.json()
        logging.info("create success response: {}".format(json.dumps(data)))
        return True, data
    logging.info('VIPS create() was not successful')
    logging.info('create endpoint: {}'.format(endpoint))
    logging.info('create payload: {}'.format(json.dumps(payload)))
    logging.info('VIPS API response: {} correlation_id: {}'.format(response.text, correlation_id))
    return False, dict()


def patch(endpoint: str, user: str, password: str,  payload: dict, correlation_id='ABC') -> tuple:
    logging.info('patch endpoint: {}'.format(endpoint))
    logging.info('patch payload: {}'.format(json.dumps(payload)))
    try:
        response = requests.patch(endpoint, verify=False, json=payload, auth=(user, password))
    except requests.ConnectionError as error:
        logging.warning('no response from the VIPS API: {}'.format(error))
        return False, dict()

    data = response.json()
    logging.info('VIPS API patch response: {} correlation_id: {}'.format(json.dumps(data), correlation_id))
    return response.status_code == 200, data


def remove_accents(input_str):
    nfkd_form = normalize('NFKD', input_str)
    only_ascii = nfkd_form.encode('ASCII', 'ignore')
    return only_ascii


def is_last_name_match(vips_status: dict, last_name: str) -> bool:
    vips_last_name = vips_status['surnameNm']
    logging.info('compare last name from VIPS: {} with user entered surname {}'.format(vips_last_name, last_name))
    return bool(remove_accents(vips_last_name).upper() == remove_accents(last_name).upper())


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


def time_slot_to_friendly_string(time_slot: dict, presentation_type: str) -> dict:
    start_time = time_slot['reviewStartDtm']
    end_time = time_slot['reviewEndDtm']
    label = ""
    if presentation_type == "ORAL":
        label = "{} - {} to {}".format(
            # Fri, Sep 4, 2020 - 10:00am to 10:30am
            vips_str_to_datetime(start_time).strftime("%a, %b %-d, %Y"),
            vips_str_to_friendly_time(start_time),
            vips_str_to_friendly_time(end_time))
    elif presentation_type == "WRIT":
        label = "{} at 9:30AM".format(
            # Friday, Sept 4, 2020 at 9:30AM
            vips_str_to_datetime(start_time).strftime("%a, %b %-d, %Y"))
    return {
        "label": label,
        "value": encode_time_slot(time_slot)
    }


def time_slots_to_friendly_times(time_slots: dict, presentation_type: str) -> list:
    """
    This function takes a list of timeslots as returned
    by VIPS GET schedule and returns a list of
    dictionary objects with friendly labels and base64
    encoded VIPS date time string.  Written reviews are
    only shown the date -- no times.
    {
        label: "Fri, Sep 4, 2020 - 10:00am to 11:30am"
        value: "ZGF0YSB0byBiZSBlbmNvZGVk"
    }
    """
    return [time_slot_to_friendly_string(time_slot, presentation_type) for time_slot in time_slots]


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
