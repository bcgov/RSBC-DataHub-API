import pytest
import logging
import responses
import json
from python.common.config import Config
from python.common.splunk import log_to_splunk
from python.common.splunk_application_for_review import paybc_lookup
from python.prohibition_web_svc.middleware.icbc_middleware import splunk_get_driver, splunk_get_vehicle


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

    is_okay, args = paybc_lookup(splunk_data=expected_payload, config=Config, prohibition_number='40123456')
    log_to_splunk(**args)

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

    is_okay, args = splunk_get_driver(splunk_data=expected_payload,
                                      config=Config,
                                      dl_number=dl_number,
                                      username=username,
                                      user_guid='')
    log_to_splunk(**args)

    payload = json.loads(responses.calls[0].request.body.decode())
    logging.warning(json.dumps(payload))
    assert payload == {"event": {
        "event": 'icbc_get_driver',
        "user_guid": '',
        "username": username,
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

    is_okay, args = splunk_get_vehicle(splunk_data=expected_payload,
                                       config=Config,
                                       plate_number=plate_number,
                                       username=username,
                                       user_guid='')
    log_to_splunk(**args)

    payload = json.loads(responses.calls[0].request.body.decode())
    logging.warning(json.dumps(payload))
    assert payload == {"event": {
        "event": 'icbc_get_vehicle',
        "user_guid": '',
        "username": "someuser@bceid",
        'queried_plate': plate_number
    }, "source": "be78d6"}
