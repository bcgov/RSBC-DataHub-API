import logging
import logging.config
import requests

# We always return True regardless of whether the Splunk message is
# received successfully or not. We don't want the failure of Splunk logging
# call to disrupt the business flow where this function was called.


def application_accepted(**args) -> tuple:
    splunk_event = {"event": "application_accepted"}
    _post_to_splunk(splunk_event, **args)
    return True, args


def disclosure_sent(**args) -> tuple:
    splunk_event = {"event": "disclosure_sent"}
    _post_to_splunk(splunk_event, **args)
    return True, args


def review_scheduled(**args) -> tuple:
    splunk_event = {"event": "review_scheduled"}
    _post_to_splunk(splunk_event, **args)
    return True, args


def evidence_received(**args) -> tuple:
    splunk_event = {"event": "evidence_received"}
    _post_to_splunk(splunk_event, **args)
    return True, args


def review_fee_paid(**args) -> tuple:
    splunk_event = {"event": "review_fee_paid"}
    _post_to_splunk(splunk_event, **args)
    return True, args


def paybc_lookup(**args) -> tuple:
    splunk_event = {"event": "paybc_lookup"}
    _post_to_splunk(splunk_event, **args)
    return True, args


def paybc_invoice_generated(**args) -> tuple:
    splunk_event = {"event": "paybc_invoice_generated"}
    _post_to_splunk(splunk_event, **args)
    return True, args


def icbc_get_driver(**args) -> tuple:
    username = args.get('username')
    splunk_event = {"event": "icbc_get_driver", "loginUserId": username}
    _post_to_splunk(splunk_event, **args)
    return True, args


def icbc_get_vehicle(**args) -> tuple:
    username = args.get('username')
    splunk_event = {"event": "icbc_get_vehicle", "loginUserId": username}
    _post_to_splunk(splunk_event, **args)
    return True, args


def _post_to_splunk(splunk_event: dict, **args):
    logging.debug("inside _post_to_splunk()")
    config = args.get('config')
    splunk_data = _get_splunk_payload(args.get('prohibition_number'), splunk_event, config.OPENSHIFT_PLATE)
    endpoint = "{}:{}/services/collector".format(config.SPLUNK_HOST, config.SPLUNK_PORT)
    headers = {"Authorization": "Splunk " + config.SPLUNK_TOKEN}
    logging.debug(endpoint)
    logging.debug(str(headers))
    logging.debug(splunk_event)
    try:
        response = requests.post(endpoint, headers=headers, json=splunk_data, verify=False)
    except requests.ConnectionError as error:
        logging.warning('No response from the Splunk API: {}'.format(error))
        return
    if response.status_code != 200:
        logging.warning('response from Splunk was not successful: {}'.format(response.text))
    return


def _get_splunk_payload(prohibition_number: str, splunk_event: dict, openshift_plate: str) -> dict:
    splunk_event['prohibition_number'] = prohibition_number
    splunk_data = dict({})
    splunk_data['event'] = splunk_event
    splunk_data['source'] = openshift_plate
    return splunk_data
