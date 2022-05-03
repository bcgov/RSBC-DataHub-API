import pytest
import responses
import json
from python.prohibition_web_svc.config import Config
from datetime import datetime
import python.prohibition_web_svc.middleware.keycloak_middleware as middleware
from python.prohibition_web_svc.models import db, UserRole, User
from python.prohibition_web_svc.app import create_app
import logging
import json


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
    users = [
        User(username="john@idir",
             user_guid="john@idir",
             agency='RCMP Terrace',
             badge_number='0508',
             first_name='John',
             last_name='Smith'),
        User(username="larry@idir",
             user_guid="larry@idir",
             agency='RCMP Terrace',
             badge_number='0555',
             first_name='Larry',
             last_name='Smith'),
        User(username="mo@idir",
             user_guid="mo@idir",
             agency='RCMP Terrace',
             badge_number='8088',
             first_name='Mo',
             last_name='Smith')
    ]
    db.session.bulk_save_objects(users)
    user_role = [
        UserRole(user_guid='john@idir', role_name='officer', submitted_dt=today),
        UserRole(user_guid='larry@idir', role_name='officer', submitted_dt=today, approved_dt=today),
        UserRole(user_guid='mo@idir', role_name='administrator', submitted_dt=today, approved_dt=today),
        UserRole(user_guid='mo@idir', role_name='officer', submitted_dt=today, approved_dt=today)
    ]
    db.session.bulk_save_objects(user_role)
    db.session.commit()


@responses.activate
def test_administrator_can_get_all_users(as_guest, monkeypatch, roles):
    monkeypatch.setattr(Config, 'ADMIN_USERNAME', 'administrator@idir')
    monkeypatch.setattr(middleware, "get_keycloak_certificates", _mock_keycloak_certificates)
    monkeypatch.setattr(middleware, "decode_keycloak_access_token", _get_administrative_user)
    resp = as_guest.get(Config.URL_PREFIX + "/api/v1/admin/users",
                        follow_redirects=True,
                        content_type="application/json",
                        headers=_get_keycloak_auth_header(_get_keycloak_access_token()))
    logging.debug("dump query response: " + json.dumps(resp.json))
    assert resp.status_code == 200
    assert len(resp.json) == 4
    assert resp.json[0]['user_guid'] == 'john@idir'
    assert responses.calls[0].request.body.decode() == json.dumps({
        'event': {
            'event': 'admin get users',
            'user_guid': 'mo@idir',
            'username': 'mo@idir'
        },
        'source': 'be78d6'
    })


@responses.activate
def test_non_administrators_cannot_get_all_users(as_guest, monkeypatch, roles):
    monkeypatch.setattr(Config, 'ADMIN_USERNAME', 'administrator@idir')
    monkeypatch.setattr(middleware, "get_keycloak_certificates", _mock_keycloak_certificates)
    monkeypatch.setattr(middleware, "decode_keycloak_access_token", _get_authorized_user)
    resp = as_guest.get(Config.URL_PREFIX + "/api/v1/admin/users",
                         follow_redirects=True,
                         content_type="application/json",
                         headers=_get_keycloak_auth_header(_get_keycloak_access_token()))
    logging.debug(json.dumps(resp.json))
    assert resp.status_code == 401
    assert responses.calls[0].request.body.decode() == json.dumps({
        'event': {
            'event': 'permission denied',
            'user_guid': 'larry@idir',
            'username': 'larry@idir'
        },
        'source': 'be78d6'
    })


@responses.activate
def test_unauthenticated_user_cannot_get_all_users(as_guest, monkeypatch, roles):
    resp = as_guest.get(Config.URL_PREFIX + "/api/v1/admin/users",
                         follow_redirects=True,
                         content_type="application/json")
    logging.debug(json.dumps(resp.json))
    assert resp.status_code == 401
    assert responses.calls[0].request.body.decode() == json.dumps({
        'event': {
            'event': 'unauthenticated',
        },
        'source': 'be78d6'
    })


def _get_keycloak_access_token() -> str:
    return 'some-secret-access-token'


def _get_keycloak_auth_header(access_token) -> dict:
    return dict({
        'Authorization': 'Bearer {}'.format(access_token)
    })


def _mock_keycloak_certificates(**kwargs) -> tuple:
    logging.warning("inside _mock_keycloak_certificates()")
    return True, kwargs


def _get_authorized_user(**kwargs) -> tuple:
    logging.warning("inside _get_authorized_user()")
    kwargs['decoded_access_token'] = {'preferred_username': 'larry@idir'}
    return True, kwargs


def _get_administrative_user(**kwargs) -> tuple:
    kwargs['decoded_access_token'] = {'preferred_username': 'mo@idir'}
    return True, kwargs
