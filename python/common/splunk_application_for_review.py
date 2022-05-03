import logging
import logging.config
import requests


def application_accepted(**args) -> tuple:
    args['splunk_data'] = {"event": "application_accepted", "prohibition_number": args.get('prohibition_number')}
    return True, args


def disclosure_sent(**args) -> tuple:
    args['splunk_data'] = {"event": "disclosure_sent", "prohibition_number": args.get('prohibition_number')}
    return True, args


def review_scheduled(**args) -> tuple:
    args['splunk_data'] = {"event": "review_scheduled", "prohibition_number": args.get('prohibition_number')}
    return True, args


def evidence_received(**args) -> tuple:
    args['splunk_data'] = {"event": "evidence_received", "prohibition_number": args.get('prohibition_number')}
    return True, args


def review_fee_paid(**args) -> tuple:
    args['splunk_data'] = {"event": "review_fee_paid", "prohibition_number": args.get('prohibition_number')}
    return True, args


def paybc_lookup(**args) -> tuple:
    args['splunk_data'] = {"event": "paybc_lookup", "prohibition_number": args.get('prohibition_number')}
    return True, args


def paybc_invoice_generated(**args) -> tuple:
    args['splunk_data'] = {"event": "paybc_invoice_generated", "prohibition_number": args.get('prohibition_number')}
    return True, args


def _get_review_payload(prohibition_number: str, splunk_event: dict, openshift_plate: str) -> dict:
    """
    Splunk payload for application for review
    """
    splunk_event['prohibition_number'] = prohibition_number
    splunk_data = dict({})
    splunk_data['event'] = splunk_event
    splunk_data['source'] = openshift_plate
    return splunk_data

