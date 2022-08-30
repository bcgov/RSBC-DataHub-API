import pytest
import logging
import responses
import json
from datetime import datetime
import python.prohibition_web_svc.middleware.keycloak_middleware as middleware
from python.prohibition_web_svc.models import db, UserRole
from python.prohibition_web_svc.app import create_app
from python.prohibition_web_svc.config import Config


@pytest.fixture
def application():
    return create_app()


@pytest.fixture
def as_guest(application):
    application.config['TESTING'] = True
    with application.test_client() as client:
        yield client


@pytest.fixture
def database(application):
    with application.app_context():
        db.init_app(application)
        db.create_all()
        yield db
        db.drop_all()
        db.session.commit()


@pytest.fixture
def roles(database):
    today = datetime.strptime("2021-07-21", "%Y-%m-%d")
    user_role = [
        UserRole(user_guid='john@idir', role_name='officer', submitted_dt=today),
        UserRole(user_guid='', role_name='officer', submitted_dt=today, approved_dt=today)
    ]
    db.session.bulk_save_objects(user_role)
    db.session.commit()


@responses.activate
def test_unauthorized_can_get_agencies(as_guest, monkeypatch, roles):
    responses.add(responses.POST, "{}:{}/services/collector".format(
        Config.SPLUNK_HOST, Config.SPLUNK_PORT), status=200)

    resp = as_guest.get(Config.URL_PREFIX + "/api/v1/static/agencies",
                        follow_redirects=True,
                        content_type="application/json")
    assert resp.status_code == 200
    assert "2101" in resp.json
    assert responses.calls[0].request.body.decode() == json.dumps({
        'event': {
            'event': 'get static resource',
            'resource': 'agencies',
            'user_guid': '',
            'username': ''
        },
        'source': 'be78d6'
    })


@responses.activate
def test_unauthorized_user_gets_impound_lot_operators(as_guest, monkeypatch, roles):
    responses.add(responses.POST, "{}:{}/services/collector".format(
        Config.SPLUNK_HOST, Config.SPLUNK_PORT), status=200)

    resp = as_guest.get(Config.URL_PREFIX + "/api/v1/static/impound_lot_operators",
                        follow_redirects=True,
                        content_type="application/json")
    assert resp.status_code == 200
    assert "24 HOUR TOWING" in resp.json[0]['name']
    assert responses.calls[0].request.body.decode() == json.dumps({
        'event': {
            'event': 'get static resource',
            'resource': 'impound_lot_operators',
            'user_guid': '',
            'username': ''
        },
        'source': 'be78d6'
    })


@responses.activate
def test_unauthorized_user_gets_provinces(as_guest, monkeypatch, roles):
    responses.add(responses.POST, "{}:{}/services/collector".format(
        Config.SPLUNK_HOST, Config.SPLUNK_PORT), status=200)

    resp = as_guest.get(Config.URL_PREFIX + "/api/v1/static/provinces",
                        follow_redirects=True,
                        content_type="application/json")
    assert resp.status_code == 200
    assert 'objectCd' in resp.json[2]
    assert 'objectDsc' in resp.json[2]
    assert responses.calls[0].request.body.decode() == json.dumps({
        'event': {
            'event': 'get static resource',
            'resource': 'provinces',
            'user_guid': '',
            'username': ''
        },
        'source': 'be78d6'
    })


@responses.activate
def test_unauthorized_user_gets_jurisdictions(as_guest, monkeypatch, roles):
    responses.add(responses.POST, "{}:{}/services/collector".format(
        Config.SPLUNK_HOST, Config.SPLUNK_PORT), status=200)
    resp = as_guest.get(Config.URL_PREFIX + "/api/v1/static/jurisdictions",
                        follow_redirects=True,
                        content_type="application/json")
    assert resp.status_code == 200
    assert {"objectCd": "BC", "objectDsc": "BRITISH COLUMBIA"} in resp.json
    assert responses.calls[0].request.body.decode() == json.dumps({
        'event': {
            'event': 'get static resource',
            'resource': 'jurisdictions',
            'user_guid': '',
            'username': ''
        },
        'source': 'be78d6'
    })


@responses.activate
def test_unauthorized_user_can_get_countries(as_guest, monkeypatch, roles):
    responses.add(responses.POST, "{}:{}/services/collector".format(
        Config.SPLUNK_HOST, Config.SPLUNK_PORT), status=200)
    resp = as_guest.get(Config.URL_PREFIX + "/api/v1/static/countries",
                        follow_redirects=True,
                        content_type="application/json")
    assert resp.status_code == 200
    assert 'objectCd' in resp.json[2]
    assert 'objectDsc' in resp.json[2]
    assert responses.calls[0].request.body.decode() == json.dumps({
        'event': {
            'event': 'get static resource',
            'resource': 'countries',
            'user_guid': '',
            'username': ''
        },
        'source': 'be78d6'
    })


@responses.activate
def test_unauthorized_user_gets_cities(as_guest, monkeypatch, roles):
    responses.add(responses.POST, "{}:{}/services/collector".format(
        Config.SPLUNK_HOST, Config.SPLUNK_PORT), status=200)

    resp = as_guest.get(Config.URL_PREFIX + "/api/v1/static/cities",
                        follow_redirects=True,
                        content_type="application/json")
    assert resp.status_code == 200
    assert {'objectCd': 'OHMH', 'objectDsc': '100 MILE HOUSE'} in resp.json
    assert responses.calls[0].request.body.decode() == json.dumps({
        'event': {
            'event': 'get static resource',
            'resource': 'cities',
            'user_guid': '',
            'username': ''
        },
        'source': 'be78d6'
    })


@responses.activate
def test_unauthorized_user_can_get_vehicles(as_guest, monkeypatch, roles):
    resp = as_guest.get(Config.URL_PREFIX + "/api/v1/static/vehicles",
                        follow_redirects=True,
                        content_type="application/json")
    assert resp.status_code == 200
    assert "AMGN" == resp.json[0]['mk']
    assert " - Hummer" == resp.json[0]['search']
    assert responses.calls[0].request.body.decode() == json.dumps({
        'event': {
            'event': 'get static resource',
            'resource': 'vehicles',
            'user_guid': '',
            'username': ''
        },
        'source': 'be78d6'
    })


@responses.activate
def test_unauthorized_user_can_get_vehicle_styles(as_guest, monkeypatch, roles):
    resp = as_guest.get(Config.URL_PREFIX + "/api/v1/static/vehicle_styles",
                        follow_redirects=True,
                        content_type="application/json")
    assert resp.status_code == 200
    assert {"code": "2DR", "name": "2-DOOR SEDAN"} == resp.json[0]
    assert responses.calls[0].request.body.decode() == json.dumps({
        'event': {
            'event': 'get static resource',
            'resource': 'vehicle_styles',
            'user_guid': '',
            'username': ''
        },
        'source': 'be78d6'
    })


@responses.activate
def test_unauthorized_user_can_get_keycloak_config(as_guest):
    resp = as_guest.get(Config.URL_PREFIX + "/api/v1/static/keycloak",
                        follow_redirects=True,
                        content_type="application/json")
    assert resp.status_code == 200
    assert 'realm' in resp.json
    assert 'url' in resp.json
    assert 'clientId' in resp.json
    assert responses.calls[0].request.body.decode() == json.dumps({
        'event': {
            'event': 'get static resource',
            'resource': 'keycloak',
            'user_guid': '',
            'username': ''
        },
        'source': 'be78d6'
    })


@responses.activate
def test_unauthorized_user_can_get_configuration(as_guest):
    resp = as_guest.get(Config.URL_PREFIX + "/api/v1/static/configuration",
                        follow_redirects=True,
                        content_type="application/json")
    assert resp.status_code == 200
    assert resp.json == {
        "environment": "dev"
    }
    assert responses.calls[0].request.body.decode() == json.dumps({
        'event': {
            'event': 'get static resource',
            'resource': 'configuration',
            'user_guid': '',
            'username': ''
        },
        'source': 'be78d6'
    })


def _get_unauthorized_user(**kwargs) -> tuple:
    logging.warning("inside _get_unauthorized_user()")
    kwargs['decoded_access_token'] = {'preferred_username': 'john@idir'}  # keycloak username
    return True, kwargs


def _get_authorized_user(**kwargs) -> tuple:
    logging.warning("inside _get_authorized_user()")
    kwargs['decoded_access_token'] = {'preferred_username': ''}  # keycloak username
    return True, kwargs


def _get_keycloak_access_token() -> str:
    return 'some-secret-access-token'


def _get_keycloak_auth_header(access_token) -> dict:
    return dict({
        'Authorization': 'Bearer {}'.format(access_token)
    })


def _mock_keycloak_certificates(**kwargs) -> tuple:
    logging.warning("inside _mock_keycloak_certificates()")
    return True, kwargs