import pytest
import os
import requests
import base64
import python.geocodersvc.routes as routes
from python.geocodersvc.config import Config

os.environ['TZ'] = 'UTC'


@pytest.fixture
def client():
    routes.application.config['TESTING'] = True
    with routes.application.test_client() as client:
        yield client


@pytest.fixture
def basic_auth(monkeypatch):
    monkeypatch.setattr(Config, "GEOCODE_BASIC_AUTH_USER", "user-id")
    monkeypatch.setattr(Config, "GEOCODE_BASIC_AUTH_PASS", "secret")
    string_credentials = "{}:{}".format(Config.GEOCODE_BASIC_AUTH_USER, Config.GEOCODE_BASIC_AUTH_PASS)
    credentials = (base64.b64encode(string_credentials.encode())).decode()
    header = {"Authorization": "Basic {}".format(credentials)}
    yield header


def test_ping_endpoint_returns_ready_status(client):
    response = client.get('/ping')
    assert response.json == "geocoder is ready"
    assert response.status_code == 200


def test_ready_endpoint_returns_okay_status(client, monkeypatch):
    monkeypatch.setattr(requests, "get", mock_good_request)
    response = client.get('/ready')
    assert response.status_code == 200


def test_ready_endpoint_returns_not_ready_status(client, monkeypatch):
    monkeypatch.setattr(requests, "get", mock_bad_request)
    response = client.get('/ready')
    assert response.json == {"error": "response from DataBC did not match expected format"}
    assert response.status_code == 500


def test_posting_to_address_endpoint_without_basic_auth_yields_401(client, monkeypatch):
    response = client.post('/address')
    assert response.json == {"error": "Unauthorized"}
    assert response.status_code == 401


def test_posting_to_address_endpoint_without_valid_payload_yields_validation_error(client, basic_auth, monkeypatch):
    response = client.post('/address', headers=basic_auth)
    assert response.json == {"error": "not json"}
    assert response.status_code == 500


def test_posting_to_address_endpoint_with_non_json_payload_yields_validation_error(client, basic_auth, monkeypatch):
    payload = "<xml></xml>"
    response = client.post('/address', headers=basic_auth, data=payload)
    assert response.json == {"error": "not json"}
    assert response.status_code == 500


def test_posting_to_address_endpoint_without_address_yields_validation_error(client, basic_auth, monkeypatch):
    monkeypatch.setattr(requests, "get", mock_bad_request)
    payload = dict({"bad_attribute": "value"})
    response = client.post('/address', headers=basic_auth, json=payload)
    assert response.json == {"error": "failed validation"}
    assert response.status_code == 500


def test_posting_to_address_endpoint_with_address_yields_success_response(client, basic_auth, monkeypatch):
    monkeypatch.setattr(requests, "get", mock_good_request)
    payload = dict({"address": "914 Yates, Victoria, BC"})
    response = client.post('/address', headers=basic_auth, json=payload)
    assert "address_raw" in response.json
    assert 'data_bc' in response.json
    assert 'faults' in response.json['data_bc']
    assert response.status_code == 200


def test_bad_response_from_databc_yields_unsuccessful_response(client, basic_auth, monkeypatch):
    monkeypatch.setattr(requests, "get", mock_bad_request)
    payload = dict({"address": "914 Yates, Victoria, BC"})
    response = client.post('/address', headers=basic_auth, json=payload)
    assert "is_success" in response.json
    assert response.json['is_success'] is False
    assert "error" in response.json
    assert "DataBC is not responding" == response.json['error']
    assert response.status_code == 200


def mock_good_request(geocoder_url, **args):

    class Requests:
        headers = "these are headers"
        status_code = 200

        @staticmethod
        def json():
            mock_json = dict({
                "features": [
                    {
                        "geometry": {
                            "coordinates": [123, 49]
                        },
                        "properties": {
                            "score": 90,
                            "matchPrecision": "30",
                            "fullAddress": "some address",
                            "faults": []
                        }
                    }
                ]
            })
            return mock_json
    return Requests


def mock_bad_request(geocoder_url, **args):

    class Requests:
        headers = "these are headers"
        status_code = 200

        @staticmethod
        def json():
            bad_json = dict({
                "features": []
            })
            return bad_json
    return Requests


def unsuccessful_call_to_geocoder(**args) -> tuple:
    return False, args
