# This script adds form ids to the prohibition web service

import requests
import logging
import os
import argparse
from requests.auth import HTTPBasicAuth


BASE_URL = os.getenv("BASE_URL")
FLASK_USER = os.getenv("FLASK_USER")
FLASK_PASS = os.getenv("FLASK_PASS")


def main():
    parser = argparse.ArgumentParser(description="This script adds form ids to the prohibition web service")
    parser.add_argument('--form-type', required=True, choices=['12Hour', '24Hour', 'IRP', 'VI'])
    parser.add_argument('--start', required=True, help='starting number')
    parser.add_argument('--end', required=True, help='ending number')
    parser.add_argument('--env', default='TEST', choices=['TEST', 'PROD'])
    args = parser.parse_args()

    for form_number in range(int(args.start), int(args.end)):
        form_id = "{}{}".format(form_prefix(args.form_type, args.env), form_number)
        logging.warning("adding form_id: " + form_id)
        add_form_ids(args.form_type, form_id)


def add_form_ids(form_type: str, form_id: str):
    payload = {
        "form_id": form_id,
        "form_type": form_type
    }
    r = requests.post(BASE_URL + '/api/v1/admin/forms', json=payload, auth=HTTPBasicAuth(FLASK_USER, FLASK_PASS))
    if r.status_code != 201:
        logging.warning(str(payload))
        logging.warning(r.url)
        logging.warning(r.text)
    return


def form_prefix(form_type: str, environment: str) -> str:
    prefix = {}
    if environment == 'TEST':
        prefix = {
            "12Hour": "JZ",  # a 'JZ' prefix denotes a test number
            "24Hour": "VZ",  # a 'VZ' prefix denotes a test number
            "IRP": "20",
            "VI": "22"
        }
    if environment == 'PROD':
        prefix = {
            "12Hour": "JA",
            "24Hour": "VA",
            "IRP": "20",
            "VI": "22"
        }
    return prefix.get(form_type)


if __name__ == "__main__":
    main()
