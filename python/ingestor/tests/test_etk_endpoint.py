import pytest
import base64
import logging
import logging.config
import os
from python.common.tests.rabbit_mock import MockRabbitMQ, MockRabbitPublishFail
from python.common.helper import load_json_into_dict
from python.ingestor.config import Config
import python.ingestor.routes as routes

os.environ['TZ'] = 'UTC'


@pytest.fixture
def as_guest():
    routes.application.config['TESTING'] = True
    with routes.application.test_client() as client:
        yield client


@pytest.fixture
def as_authorized_user(monkeypatch):
    routes.application.config['TESTING'] = True
    routes.application.test_request_context(headers=get_basic_authentication_header(monkeypatch))
    with routes.application.test_client() as client:
        yield client


def test_etk_endpoint_accepts_json_payload(as_authorized_user, monkeypatch):
    monkeypatch.setattr(routes, "RabbitMQ", MockRabbitMQ)
    payload = dict({"data": "json"})
    response = as_authorized_user.post('/v1/publish/event/etk', json=payload)
    assert response.json == payload
    assert response.status_code == 200


def test_etk_endpoint_accepts_ticket_issuance(as_authorized_user, caplog, monkeypatch):
    monkeypatch.setattr(routes, "RabbitMQ", MockRabbitMQ)
    payload = load_json_into_dict("python/common/tests/sample_data/etk/event_issuance.json")
    response = as_authorized_user.post('/v1/publish/event/etk', json=payload)
    assert 'queue: ingested' in caplog.text
    assert '"event_id": 1234' in caplog.text
    assert '"event_date_time": "2020-01-20 08:23:16"' in caplog.text
    assert response.status_code == 200


def test_etk_endpoint_rejects_ticket_issuance_if_not_published_to_rabbitmq(as_authorized_user, caplog, monkeypatch):
    monkeypatch.setattr(routes, "RabbitMQ", MockRabbitPublishFail)
    payload = load_json_into_dict("python/common/tests/sample_data/etk/event_issuance.json")
    response = as_authorized_user.post('/v1/publish/event/etk', json=payload)
    assert 'queue: ingested' in caplog.text
    assert '"event_id": 1234' in caplog.text
    assert '"event_date_time": "2020-01-20 08:23:16"' in caplog.text
    assert response.status_code == 500


def get_basic_authentication_header(monkeypatch, username="name", password="secret") -> dict:
    monkeypatch.setattr(Config, "FLASK_BASIC_AUTH_USER", username)
    monkeypatch.setattr(Config, "FLASK_BASIC_AUTH_PASS", password)
    credentials = base64.b64encode((username + ":" + password).encode('utf-8')).decode('utf-8')
    headers = dict({"Authorization": "Basic {}".format(credentials)})
    logging.debug(headers)
    return headers

