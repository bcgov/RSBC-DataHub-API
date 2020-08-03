import requests
import logging
import json


def get_prohibition(prohibition_number: str, config, local_requests=requests):
    endpoint = config.VIPS_API_ROOT_URI + prohibition_number + '/status'
    logging.debug('vips_api_endpoint: ' + endpoint)
    try:
        response = local_requests.get(endpoint, auth=(config.VIPS_API_USER, config.VIPS_API_PASS))
    except AssertionError as error:
        logging.warning('no response from the VIPS API')
        return False, error

    data = response.json()
    if data['resp'] == 'fail':
        logging.warning('VIPS API response: ' + json.dumps(data))
        logging.critical('hard coded response - remove before flight')
        # TODO - Remove before flight - hard coded to work around unknown correlationID parameter
        return True, {
            "resp": "Success",
            "data": {
                "status": {
                    "effectiveDt": "string",
                    "noticeTypeCd": "string",
                    "originalCause": "string",
                    "receiptNumberTxt": "string",
                    "reviewCreatedYn": "string",
                    "reviewEndDtm": "string",
                    "reviewFormSubmittedYn": "string",
                    "reviewStartDtm": "string",
                    "surnameNm": "Jones"
                },
            },
            "httpStatus": 200
        }
        # return False, data
    
    return True, data
