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
@pytest.mark.parametrize("event", ["icbc_get_driver", "icbc_get_vehicle"])
def test_splunk_logs_icbc_get_driver_event(event):

    expected_payload = {
        'event': event,
        'source': 'be78d6',
    }

    responses.add(responses.GET,
                  '{}:{}/services/collector'.format(Config.SPLUNK_HOST, Config.SPLUNK_PORT),
                  headers={"Authorization": "Splunk " + Config.SPLUNK_TOKEN},
                  json=expected_payload,
                  status=200, match_querystring=True)

    method_to_call = getattr(splunk, event)
    results = method_to_call(config=Config, username='someuser@bceid')

    payload = json.loads(responses.calls[0].request.body.decode())
    logging.warning(json.dumps(payload))
    assert payload == {"event": {"event": event, "loginUserId": "someuser@bceid"}, "source": "be78d6"}
