import pytest
from python.prohibition_web_service.config import Config
from datetime import datetime
import python.prohibition_web_service.middleware.keycloak_middleware as middleware
from python.prohibition_web_service.models import db, UserRole
from python.prohibition_web_service.app import create_app
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
    user_role = [
        UserRole(username='john@idir', role_name='officer', submitted_dt=today),
        UserRole(username='larry@idir', role_name='officer', submitted_dt=today, approved_dt=today),
        UserRole(username='mo@idir', role_name='administrator', submitted_dt=today, approved_dt=today),
        UserRole(username='mo@idir', role_name='officer', submitted_dt=today, approved_dt=today)
    ]
    db.session.bulk_save_objects(user_role)
    db.session.commit()


def test_administrator_can_get_all_users(as_guest, monkeypatch, roles):
    monkeypatch.setattr(Config, 'ADMIN_USERNAME', 'administrator@idir')
    monkeypatch.setattr(middleware, "get_keycloak_certificates", _mock_keycloak_certificates)
    monkeypatch.setattr(middleware, "decode_keycloak_access_token", _get_administrative_user)
    resp = as_guest.get("/api/v1/admin/users",
                         follow_redirects=True,
                         content_type="application/json",
                         headers=_get_keycloak_auth_header(_get_keycloak_access_token()))
    logging.debug(json.dumps(resp.json))
    assert resp.status_code == 200
    assert len(resp.json) == 4
    assert resp.json[0]['username'] == 'john@idir'


def test_non_administrators_cannot_get_all_users(as_guest, monkeypatch, roles):
    monkeypatch.setattr(Config, 'ADMIN_USERNAME', 'administrator@idir')
    monkeypatch.setattr(middleware, "get_keycloak_certificates", _mock_keycloak_certificates)
    monkeypatch.setattr(middleware, "decode_keycloak_access_token", _get_authorized_user)
    resp = as_guest.get("/api/v1/admin/users",
                         follow_redirects=True,
                         content_type="application/json",
                         headers=_get_keycloak_auth_header(_get_keycloak_access_token()))
    logging.debug(json.dumps(resp.json))
    assert resp.status_code == 401


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
