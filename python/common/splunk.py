import logging
import logging.config
import requests


def log_to_splunk(**kwargs) -> tuple:
    """
    We always return True regardless of whether the Splunk message is
    received successfully or not. We don't want the failure of Splunk logging
    call to disrupt the business flow where this function was called.
    """
    config = kwargs.get('config')
    splunk_data = kwargs.get('splunk_data')
    splunk_payload = dict({})
    splunk_payload['event'] = splunk_data
    splunk_payload['source'] = config.OPENSHIFT_PLATE
    _post_to_splunk(splunk_payload, **kwargs)
    return True, kwargs


def _post_to_splunk(splunk_payload: dict, **args) -> bool:
    logging.debug("inside _post_to_splunk()")
    config = args.get('config')
    endpoint = "{}:{}/services/collector".format(config.SPLUNK_HOST, config.SPLUNK_PORT)
    headers = {"Authorization": "Splunk " + config.SPLUNK_TOKEN}
    logging.debug(endpoint)
    logging.debug(str(headers))
    logging.debug(splunk_payload)
    try:
        response = requests.post(endpoint, headers=headers, json=splunk_payload, verify=False)
    except requests.ConnectionError as error:
        logging.warning('No response from the Splunk API: {}'.format(error))
        return False
    if response.status_code != 200:
        logging.warning('response from Splunk was not successful: {}'.format(response.text))
        return False
    return True
