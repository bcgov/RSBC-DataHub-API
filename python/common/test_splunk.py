import pytest
import logging
import responses
import json
from python.common.config import Config
import python.common.splunk as splunk
from python.common.splunk import paybc_lookup, icbc_get_driver, icbc_get_vehicle


@responses.activate
def test_splunk_logs_paybc_lookup_event():

    expected_payload = {
        'event': 'paybc_lookup',
        'source': 'be78d6',
        'prohibition_number': '40123456'
    }

    responses.add(responses.GET,
                  '{}:{}/services/collector'.format(Config.SPLUNK_HOST, Config.SPLUNK_PORT),
                  headers={"Authorization": "Splunk " + Config.SPLUNK_TOKEN},
                  json=expected_payload,
                  status=200, match_querystring=True)

    results = paybc_lookup(prohibition_number="40123456", config=Config)

    payload = json.loads(responses.calls[0].request.body.decode())
    logging.warning(json.dumps(payload))
    assert payload == {"event": {"event": "paybc_lookup", "prohibition_number": "40123456"}, "source": "be78d6"}


@responses.activate
def test_splunk_logs_icbc_get_driver_event():
    dl_number = '5161222'
    username = 'someuser@bceid'
    expected_payload = {
        'event': 'icbc_get_driver',
        'source': 'be78d6',
        'queried_bcdl': '5161222'
    }

    responses.add(responses.GET,
                  '{}:{}/services/collector'.format(Config.SPLUNK_HOST, Config.SPLUNK_PORT),
                  headers={"Authorization": "Splunk " + Config.SPLUNK_TOKEN},
                  json=expected_payload,
                  status=200, match_querystring=True)

    results = icbc_get_driver(config=Config, dl_number=dl_number, username=username)

    payload = json.loads(responses.calls[0].request.body.decode())
    logging.warning(json.dumps(payload))
    assert payload == {"event": {
        "event": 'icbc_get_driver',
        "loginUserId": username,
        "queried_bcdl": dl_number},
        "source": "be78d6"}


@responses.activate
def test_splunk_logs_icbc_get_vehicle_event():
    username = 'someuser@bceid'
    plate_number = 'RXC234'
    expected_payload = {
        'event': 'icbc_get_vehicle',
        'source': 'be78d6',
        'queried_plate': plate_number
    }

    responses.add(responses.GET,
                  '{}:{}/services/collector'.format(Config.SPLUNK_HOST, Config.SPLUNK_PORT),
                  headers={"Authorization": "Splunk " + Config.SPLUNK_TOKEN},
                  json=expected_payload,
                  status=200, match_querystring=True)

    results = icbc_get_vehicle(config=Config, plate_number=plate_number, username='someuser@bceid')

    payload = json.loads(responses.calls[0].request.body.decode())
    logging.warning(json.dumps(payload))
    assert payload == {"event": {
        "event": 'icbc_get_vehicle',
        "loginUserId": "someuser@bceid",
        'queried_plate': plate_number
    }, "source": "be78d6"}
