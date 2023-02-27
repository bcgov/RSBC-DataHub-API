import pytest
import responses
import json
import python.prohibition_web_svc.middleware.keycloak_middleware as middleware
from python.prohibition_web_svc.models import db, User, UserRole
from python.prohibition_web_svc.app import create_app
from python.prohibition_web_svc.config import Config
import logging
from datetime import datetime


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
    today = datetime.now()
    users = [
        User(
            username='john@idir',
            user_guid="aaa-bbb-ccc",
            agency='RCMP Terrace',
            badge_number="0234",
            first_name="John",
            last_name="Smith"),
        User(
            username='larry@idir',
            user_guid="ddd-eee-fff",
            agency='RCMP Terrace',
            badge_number="8808",
            first_name="Larry",
            last_name="Smith"),
    ]
    db.session.bulk_save_objects(users)
    user_role = UserRole(role_name="officer", user_guid="aaa-bbb-ccc", approved_dt=today, submitted_dt=today)
    db.session.add(user_role)
    db.session.commit()


def test_applying_user_must_supply_an_agency_name_of_at_least_4_characters(as_guest, monkeypatch, roles, database):
    monkeypatch.setattr(middleware, "get_keycloak_certificates", _mock_keycloak_certificates)
    monkeypatch.setattr(middleware, "decode_keycloak_access_token", _get_keycloak_user_who_has_not_applied)
    resp = as_guest.post(Config.URL_PREFIX + "/api/v1/users",
                         json={
                             "agency": "RCMP",
                             "badge_number": "108044",
                             "first_name": "New",
                             "last_name": "Officer"
                         },
                         follow_redirects=True,
                         headers=_get_keycloak_auth_header(_get_keycloak_access_token()))
    assert resp.status_code == 400
    assert resp.json['message'] == "failed validation"
    assert resp.json['errors'] == {'agency': ['min length is 5']}


@responses.activate
def test_user_without_authorization_can_apply_to_use_the_app(as_guest, monkeypatch, roles, database):
    monkeypatch.setattr(middleware, "get_keycloak_certificates", _mock_keycloak_certificates)
    monkeypatch.setattr(middleware, "decode_keycloak_access_token", _get_keycloak_user_who_has_not_applied)
    resp = as_guest.post(Config.URL_PREFIX + "/api/v1/users",
                         json={
                             "agency": "RCMP Terrace",
                             "badge_number": "108044",
                             "first_name": "New",
                             "last_name": "Officer"
                         },
                         follow_redirects=True,
                         headers=_get_keycloak_auth_header(_get_keycloak_access_token()))
    assert resp.status_code == 201
    assert database.session.query(User) \
               .filter(User.user_guid == 'new-officer@idir') \
               .filter(User.agency == 'RCMP Terrace') \
               .filter(User.badge_number == "108044") \
               .filter(User.first_name == "New") \
               .filter(User.last_name == "Officer") \
               .count() == 1
    assert database.session.query(UserRole) \
               .filter(UserRole.role_name == "officer") \
               .filter(UserRole.user_guid == 'new-officer@idir') \
               .filter(UserRole.submitted_dt != None) \
               .filter(UserRole.approved_dt == None) \
               .count() == 1
    assert responses.calls[0].request.body.decode() == json.dumps({
        'event': {
            'event': 'officer has applied',
            'user_guid': 'new-officer@idir',
            'username': 'new-officer@idir',
            'badge_number': '108044'
        },
        'source': 'be78d6'
    })


@responses.activate
def test_bceid_user_can_apply_to_use_the_app(as_guest, monkeypatch, roles, database):
    monkeypatch.setattr(middleware, "get_keycloak_certificates", _mock_keycloak_certificates)
    monkeypatch.setattr(middleware, "decode_keycloak_access_token", _get_bceid_user_who_has_not_applied)
    resp = as_guest.post(Config.URL_PREFIX + "/api/v1/users",
                         json={
                             "agency": "RCMP Terrace",
                             "badge_number": "108044",
                             "first_name": "New",
                             "last_name": "Officer"
                         },
                         follow_redirects=True,
                         headers=_get_keycloak_auth_header(_get_keycloak_access_token()))
    assert resp.status_code == 201
    assert database.session.query(User) \
               .filter(User.username == "new-officer@bceid") \
               .filter(User.user_guid == 'aaa-bbb-ccc-fff') \
               .filter(User.agency == 'RCMP Terrace') \
               .filter(User.first_name == "New") \
               .filter(User.last_name == "Officer") \
               .filter(User.business_guid == "gggg-ffff-dddd-jjjj") \
               .count() == 1
    assert database.session.query(UserRole) \
               .filter(UserRole.role_name == "officer") \
               .filter(UserRole.user_guid == 'aaa-bbb-ccc-fff') \
               .filter(UserRole.submitted_dt != None) \
               .filter(UserRole.approved_dt == None) \
               .count() == 1
    assert responses.calls[0].request.body.decode() == json.dumps({
        'event': {
            'event': 'officer has applied',
            'user_guid': 'aaa-bbb-ccc-fff',
            'username': 'new-officer@bceid',
            'badge_number': '108044'
        },
        'source': 'be78d6'
    })


@responses.activate
def test_idir_user_can_apply_to_use_the_app(as_guest, monkeypatch, roles, database):
    monkeypatch.setattr(middleware, "get_keycloak_certificates", _mock_keycloak_certificates)
    monkeypatch.setattr(middleware, "decode_keycloak_access_token", _get_idir_user_who_has_not_applied)
    resp = as_guest.post(Config.URL_PREFIX + "/api/v1/users",
                         json={
                             "agency": "RCMP Terrace",
                             "badge_number": "108044",
                             "first_name": "New",
                             "last_name": "Officer"
                         },
                         follow_redirects=True,
                         headers=_get_keycloak_auth_header(_get_keycloak_access_token()))
    assert resp.status_code == 201
    assert database.session.query(User) \
               .filter(User.username == "new-officer@idir") \
               .filter(User.user_guid == 'aaa-bbb-ccc-fff') \
               .filter(User.agency == 'RCMP Terrace') \
               .filter(User.first_name == "New") \
               .filter(User.last_name == "Officer") \
               .count() == 1
    assert database.session.query(UserRole) \
               .filter(UserRole.role_name == "officer") \
               .filter(UserRole.user_guid == 'aaa-bbb-ccc-fff') \
               .filter(UserRole.submitted_dt != None) \
               .filter(UserRole.approved_dt == None) \
               .count() == 1
    assert responses.calls[0].request.body.decode() == json.dumps({
        'event': {
            'event': 'officer has applied',
            'user_guid': 'aaa-bbb-ccc-fff',
            'username': 'new-officer@idir',
            'badge_number': '108044'
        },
        'source': 'be78d6'
    })


def test_user_with_keycloak_token_cannot_apply_again_to_use_the_app(as_guest, monkeypatch, roles):
    monkeypatch.setattr(middleware, "get_keycloak_certificates", _mock_keycloak_certificates)
    monkeypatch.setattr(middleware, "decode_keycloak_access_token", _get_authorized_user)
    resp = as_guest.post(Config.URL_PREFIX + "/api/v1/users",
                         json={
                             "agency": "RCMP Terrace",
                             "badge_number": "108044",
                             "first_name": "New",
                             "last_name": "Officer"
                         },
                         follow_redirects=True,
                         content_type="application/json",
                         headers=_get_keycloak_auth_header(_get_keycloak_access_token()))
    assert resp.status_code == 400
    assert resp.json['error'] == 'role already exists'


@responses.activate
def test_user_with_keycloak_token_can_get_their_own_user_details(as_guest, monkeypatch, roles):
    monkeypatch.setattr(middleware, "get_keycloak_certificates", _mock_keycloak_certificates)
    monkeypatch.setattr(middleware, "decode_keycloak_access_token", _get_authorized_user)
    resp = as_guest.get(Config.URL_PREFIX + "/api/v1/users",
                        follow_redirects=True,
                        content_type="application/json",
                        headers=_get_keycloak_auth_header(_get_keycloak_access_token()))
    assert resp.status_code == 200
    assert resp.json == {
        "username": 'john@idir',
        "user_guid": "aaa-bbb-ccc",
        "agency": 'RCMP Terrace',
        "badge_number": "0234",
        "first_name": "John",
        "last_name": "Smith"
    }
    assert responses.calls[0].request.body.decode() == json.dumps({
        'event': {
            'event': 'get user',
            'user_guid': 'aaa-bbb-ccc',
            'username': 'john@idir',
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
    logging.warning("inside _get_unauthorized_user()")
    kwargs['decoded_access_token'] = {
        "idir_guid": "aaa-bbb-ccc",
        'preferred_username': 'john@idir'
    }
    return True, kwargs


def _get_keycloak_user_who_has_not_applied(**kwargs) -> tuple:
    logging.warning("inside _get_keycloak_user_who_has_not_applied()")
    kwargs['decoded_access_token'] = {
        'preferred_username': 'new-officer@idir',
    }
    return True, kwargs


def _get_bceid_user_who_has_not_applied(**kwargs) -> tuple:
    logging.warning("inside _get_bceid_user_who_has_not_applied()")
    kwargs['decoded_access_token'] = {
        'preferred_username': 'new-officer@bceid',
        'bceid_userid': 'aaa-bbb-ccc-fff',
        "bceid_business_name": "RoadSafety Digital Forms",
        "bceid_business_guid": "gggg-ffff-dddd-jjjj"
    }
    return True, kwargs


def _get_idir_user_who_has_not_applied(**kwargs) -> tuple:
    logging.warning("inside _get_idir_user_who_has_not_applied()")
    kwargs['decoded_access_token'] = {
        'preferred_username': 'new-officer@idir',
        'idir_guid': 'aaa-bbb-ccc-fff',
    }
    return True, kwargs


def _get_administrative_user_from_environment_variable(**kwargs) -> tuple:
    kwargs['decoded_access_token'] = {'preferred_username': 'administrator@idir'}
    return True, kwargs
