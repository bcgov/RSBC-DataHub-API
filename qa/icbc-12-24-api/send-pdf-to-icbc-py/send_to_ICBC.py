#!/usr/bin/env python3

import requests
from dotenv import load_dotenv
import json
import logging
import os
import argparse
import base64
from datetime import datetime
from faker import Faker
from requests.auth import HTTPBasicAuth

load_dotenv()

ICBC_CONTRAVENTION_URL = os.getenv("ICBC_CONTRAVENTION_URL")
ICBC_USERNAME = os.getenv("ICBC_USERNAME")
ICBC_PASSWORD = os.getenv("ICBC_PASSWORD")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--filename')
    args = parser.parse_args()
    fake = Faker('en_CA')
    base64_encode_pdf_string = ''
    if args.filename:
        base64_encode_pdf_string = get_pdf(args.filename)
    #send_to_icbc(get_payload(fake, base64_encode_pdf_string))
    send_to_icbc(set_payload(base64_encode_pdf_string))


def send_to_icbc(payload: dict):
    r = requests.post(ICBC_CONTRAVENTION_URL, json=payload, auth=HTTPBasicAuth(ICBC_USERNAME, ICBC_PASSWORD))
    print('response status code: ' + str(r.status_code))
    print("payload: " + json.dumps(payload, indent=4, sort_keys=True))
    if r.status_code != 200:
        logging.warning(r.text)
    else:
        print("response: " + r.text)
    return


def get_pdf(pdf_filename) -> str:
    with open(pdf_filename, "rb") as pdf:
        encoded_bytes = base64.b64encode(pdf.read())
    return encoded_bytes.decode("utf-8")


def get_payload(fake, base64_encode_pdf_string) -> dict:
    driver_name = fake.name().split()
    officer_name = fake.name().split()
    violation_dt = datetime.now()
    return {
        "dlNumber": fake.ssn().replace(" ", "")[0:7],
        "dlJurisdiction": "BC",
        "lastName": driver_name[1],
        "firstName": driver_name[0],
        "birthdate": fake.date().replace("-", ""),
        "plateJurisdiction": "BC",
        "plateNumber": fake.license_plate(),
        "pujCode": "",
        "nscNumber": fake.ssn().replace(" ", "")[0:6],
        "section": "215.2",
        "violationLocation": fake.city().upper(),
        "noticeNumber": "VA" + fake.ssn().replace(" ", "")[0:6],
        "violationDate": violation_dt.strftime("%Y%m%d"),
        "violationTime": violation_dt.strftime("%H:%m"),
        "officerDetachment": "VANCOUVER",
        "officerNumber": fake.province_abbr() + fake.ssn().replace(" ", "")[0:5],
        "officerName": officer_name[1],
        "pdf": base64_encode_pdf_string
    }

def set_payload(base64_encode_pdf_string) -> dict:
    violation_dt = datetime.now()
    return {
        "dlNumber": "1695672",
        "dlJurisdiction": "BC",
        "lastName": "SYC-TSTFOUR",
        "firstName": "TST",
        "birthdate": "19920606",
        "plateJurisdiction": "BC",
        "plateNumber": "AA057A",
        "pujCode": "",
        "nscNumber": "",
        "section": "90.32",  # 12-hour alcohol: 90.32   24-hour alcohol: 215.2
                             # 12-hour drugs:   90.321  24-hour drugs:   215.3
        "violationLocation": "100 MILE HOUSE",
        "noticeNumber": "JZ100694",
        "violationDate": "20221020",
        "violationTime": "09:09",
        "officerDetachment": "RSI",
        "officerNumber": "DE110",
        "officerName": "FORSYTH",
        "pdf": base64_encode_pdf_string
    }


if __name__ == "__main__":
    main()
