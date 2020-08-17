import requests
import logging
import json
from unicodedata import normalize


def query_get(prohibition_id: str, config, correlation_id: str) -> tuple:
    endpoint = build_endpoint(config.VIPS_API_ROOT_URL, prohibition_id, 'status', correlation_id)
    return get(endpoint, config.VIPS_API_USERNAME, config.VIPS_API_PASSWORD, correlation_id)


def disclosure_get(document_id: str, config, correlation_id: str):
    endpoint = build_endpoint(config.VIPS_API_ROOT_URL, document_id, 'disclosure', correlation_id)
    return get(endpoint, config.VIPS_API_USERNAME, config.VIPS_API_PASSWORD, correlation_id)


def payment_get(prohibition_id: str, config, correlation_id: str):
    endpoint = build_endpoint(config.VIPS_API_ROOT_URL, prohibition_id, 'payment', 'status', correlation_id)
    return get(endpoint, config.VIPS_API_USERNAME, config.VIPS_API_PASSWORD, correlation_id)


def application_get(guid: str, config, correlation_id: str):
    endpoint = build_endpoint(config.VIPS_API_ROOT_URL, guid, 'application', correlation_id)
    return get(endpoint, config.VIPS_API_USERNAME, config.VIPS_API_PASSWORD, correlation_id)


def application_create(form_type: str, prohibition_id: str, config, correlation_id: str, message: dict):
    # /{formType}/{noticeNo}/application/{correlationId}
    endpoint = build_endpoint(config.VIPS_API_ROOT_URL, form_type, prohibition_id, 'application', correlation_id)
    payload = {
        "applicationInfo": {
            "email": message['form_submission']['form']['identification-information']['driver-email-address'],
            "faxNo": "string",
            "firstGivenNm": message['form_submission']['form']['identification-information']['driver-first-name'],
            "formData": "string",
            "manualEntryYN": "string",
            "noticeSubjectCd": "string",
            "phoneNo": "string",
            "presentationTypeCd": "string",
            "reviewRoleTypeCd": "string",
            "secondGivenNm": "string",
            "surnameNm": message['form_submission']['form']['identification-information']['driver-last-name'],
        }
    }
    return create(endpoint, config.VIPS_API_USERNAME, config.VIPS_API_PASSWORD, payload, correlation_id)


def application_update(guid: str, config, correlation_id: str):
    endpoint = build_endpoint(config.VIPS_API_ROOT_URL, guid, 'application', correlation_id)
    return get(endpoint, config.VIPS_API_USERNAME, config.VIPS_API_PASSWORD, correlation_id)


def schedule_get(notice_type_code: str, review_type_code: str, review_date, config, correlation_id: str) -> tuple:
    endpoint = build_endpoint(
        config.VIPS_API_ROOT_URL,
        notice_type_code,
        review_type_code,
        review_date,
        'review',
        'availableTimeSlot',
        correlation_id)
    return get(endpoint, config.VIPS_API_USERNAME, config.VIPS_API_PASSWORD, correlation_id)


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
    logging.info('VIPS API response: {} correlation_id: {}'.format(json.dumps(data), correlation_id))
    return True, data


def create(endpoint: str, user: str, password: str,  payload: dict, correlation_id='ABC') -> tuple:
    logging.debug('vips_api_endpoint: {}'.format(endpoint))
    try:
        response = requests.post(endpoint, json=payload, auth=(user, password))
    except AssertionError as error:
        logging.warning('no response from the VIPS API')
        return False, error

    data = response.json()
    # Note: VIPS response could be either record found or record not found
    logging.info('VIPS API response: {} correlation_id: {}'.format(json.dumps(data), correlation_id))
    return True, data


def remove_accents(input_str):
    nfkd_form = normalize('NFKD', input_str)
    only_ascii = nfkd_form.encode('ASCII', 'ignore')
    return only_ascii


def is_last_name_match(last_name1: str, last_name2: str) -> bool:
    logging.debug('compare last name: {} and {}'.format(last_name1, last_name2))
    return bool(remove_accents(last_name1).upper() == remove_accents(last_name2).upper())