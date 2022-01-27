# This script retrieves an application and related details from VIPS
# It's used when Appeals doesn't receive the application PDF via email.

import requests
import os
import json
import logging
import argparse
import zlib
import base64
import xmltodict
from requests.auth import HTTPBasicAuth


CORRELATION_ID = 'abc'
VIPS_API_ROOT_URL = os.getenv("VIPS_API_ROOT_URL")
VIPS_USERNAME = os.getenv("VIPS_USERNAME")
VIPS_PASSWORD = os.getenv("VIPS_PASSWORD")


def main():
    parser = argparse.ArgumentParser(description="This script retrieves an application and related details from VIPS")
    parser.add_argument('--prohibition_id', required=True)
    args = parser.parse_args()
    kwargs = get_prohibition(args.prohibition_id, CORRELATION_ID, VIPS_USERNAME, VIPS_PASSWORD)
    prohibition_status = kwargs.get("status")
    # logging.warning(json.dumps(prohibition_status))
    application_id = prohibition_status['data']['status']['reviews'][0]['applicationId']
    # logging.warning("applicationId: " + application_id)
    kwargs = get_application(application_id, CORRELATION_ID, VIPS_USERNAME, VIPS_PASSWORD, **kwargs)
    application_data = kwargs.get('application')
    # logging.warning("application: " + json.dumps(kwargs))
    form_data = application_data['data']['applicationInfo']['formData']
    # logging.warning(form_data)
    kwargs = decode_base64_string(form_data, **kwargs)
    print(json.dumps(kwargs))


def get_prohibition(prohibition_id: str, correlation_id: str, user: str, password: str, **kwargs) -> dict:
    r = requests.get(VIPS_API_ROOT_URL + '/digitalforms/{}/status/{}'.format(prohibition_id, correlation_id),
                    auth=HTTPBasicAuth(user, password))
    if r.status_code == 200:
        kwargs['status'] = r.json()
        return kwargs
    return {}


def get_application(application_id: str, correlation_id: str, user: str, password: str, **kwargs) -> dict:
    r = requests.get(VIPS_API_ROOT_URL + '/digitalforms/{}/application/{}'.format(application_id, correlation_id),
                      auth=HTTPBasicAuth(user, password))
    if r.status_code == 200:
        kwargs['application'] = r.json()
        return kwargs
    return {}


def decode_base64_string(compressed_base64_string: str, **kwargs):
    xml_compressed_bytes = base64.decodebytes(compressed_base64_string.encode())
    xml = zlib.decompress(xml_compressed_bytes)
    kwargs['xml'] = xmltodict.parse(xml)
    # remove formData
    kwargs['application']['data']['applicationInfo']['formData'] = ""
    return kwargs


if __name__ == "__main__":
    main()
