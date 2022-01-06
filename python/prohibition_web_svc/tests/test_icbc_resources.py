import pytest
import responses
from datetime import datetime
import python.prohibition_web_svc.middleware.keycloak_middleware as middleware
from python.prohibition_web_svc.models import db, UserRole
from python.prohibition_web_svc.app import create_app
from python.prohibition_web_svc.config import Config
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
        UserRole(username='larry@idir', role_name='officer', submitted_dt=today, approved_dt=today)
    ]
    db.session.bulk_save_objects(user_role)
    db.session.commit()


@responses.activate
def test_authorized_user_can_get_driver(as_guest, monkeypatch, roles):
    monkeypatch.setattr(middleware, "get_keycloak_certificates", _mock_keycloak_certificates)
    monkeypatch.setattr(middleware, "decode_keycloak_access_token", _get_authorized_user)

    responses.add(responses.GET,
                  '{}/drivers/{}'.format(Config.ICBC_API_ROOT, "5120503"),
                  json=_sample_driver_response(),
                  status=200)

    responses.add(responses.POST, "{}:{}/services/collector".format(
        Config.SPLUNK_HOST, Config.SPLUNK_PORT), status=200)

    resp = as_guest.get("/api/v1/icbc/drivers/5120503",
                        follow_redirects=True,
                        content_type="application/json",
                        headers=_get_keycloak_auth_header(_get_keycloak_access_token()))
    assert resp.status_code == 200
    assert 'dlNumber' in resp.json
    assert resp.json['dlNumber'] == "5120503"
    assert responses.calls[0].request.headers['loginUserId'] == 'larry@idir'


def test_unauthorized_user_cannot_get_driver(as_guest, monkeypatch, roles):
    monkeypatch.setattr(middleware, "get_keycloak_certificates", _mock_keycloak_certificates)
    monkeypatch.setattr(middleware, "decode_keycloak_access_token", _get_unauthorized_user)
    resp = as_guest.get("/api/v1/icbc/drivers/5120503",
                        follow_redirects=True,
                        content_type="application/json",
                        headers=_get_keycloak_auth_header("invalid-token"))
    assert resp.status_code == 401


def test_user_without_keycloak_login_cannot_get_driver(as_guest, monkeypatch):
    monkeypatch.setattr(middleware, "get_keycloak_certificates", _mock_keycloak_certificates)
    resp = as_guest.get("/api/v1/icbc/drivers/5120503",
                        follow_redirects=True,
                        content_type="application/json",
                        headers=_get_keycloak_auth_header("invalid-token"))
    assert resp.status_code == 401


@responses.activate
def test_authorized_user_gets_driver_not_found(as_guest, monkeypatch, roles):
    monkeypatch.setattr(middleware, "get_keycloak_certificates", _mock_keycloak_certificates)
    monkeypatch.setattr(middleware, "decode_keycloak_access_token", _get_authorized_user)

    responses.add(responses.GET,
                   '{}/drivers/{}'.format(Config.ICBC_API_ROOT, "1234"),
                  json=_driver_not_found(),
                  status=400)

    responses.add(responses.POST, "{}:{}/services/collector".format(
        Config.SPLUNK_HOST, Config.SPLUNK_PORT), status=200)

    resp = as_guest.get("/api/v1/icbc/drivers/1234",
                        follow_redirects=True,
                        content_type="application/json",
                        headers=_get_keycloak_auth_header(_get_keycloak_access_token()))
    assert resp.status_code == 400
    assert 'error' in resp.json
    assert resp.json['error']['message'] == "Not Found"
    assert resp.json['error']['description'] == "The resource specified in the request was not found"
    assert responses.calls[0].request.headers['loginUserId'] == 'larry@idir'


@responses.activate
def test_authorized_user_gets_vehicle_not_found(as_guest, monkeypatch, roles):
    monkeypatch.setattr(middleware, "get_keycloak_certificates", _mock_keycloak_certificates)
    monkeypatch.setattr(middleware, "decode_keycloak_access_token", _get_authorized_user)

    responses.add(responses.GET,
                  '{}/vehicles?plateNumber={}&effectiveDate={}'.format(
                      Config.ICBC_API_ROOT,
                      "AAAAA",
                      datetime.now().astimezone().replace(microsecond=0).isoformat()
                  ),
                  json=_vehicle_not_found(),
                  status=400)

    responses.add(responses.POST, "{}:{}/services/collector".format(
        Config.SPLUNK_HOST, Config.SPLUNK_PORT), status=200)

    resp = as_guest.get("/api/v1/icbc/vehicles/AAAAA",
                        follow_redirects=True,
                        content_type="application/json",
                        headers=_get_keycloak_auth_header(_get_keycloak_access_token()))
    logging.warning(json.dumps(resp.json))
    assert resp.status_code == 400
    assert 'error' in resp.json
    assert resp.json['error']['message'] == "Not Found"
    assert resp.json['error']['description'] == "vehicle not found"
    assert responses.calls[0].request.headers['loginUserId'] == 'larry@idir'


@responses.activate
def test_authorized_user_gets_vehicle(as_guest, monkeypatch, roles):
    monkeypatch.setattr(middleware, "get_keycloak_certificates", _mock_keycloak_certificates)
    monkeypatch.setattr(middleware, "decode_keycloak_access_token", _get_authorized_user)

    responses.add(responses.GET,
                  '{}/vehicles?plateNumber={}&effectiveDate={}'.format(
                      Config.ICBC_API_ROOT,
                      "LD626J",
                      datetime.now().astimezone().replace(microsecond=0).isoformat()
                  ),
                  json=sample_vehicle_response(),
                  status=200)

    responses.add(responses.POST, "{}:{}/services/collector".format(
        Config.SPLUNK_HOST, Config.SPLUNK_PORT), status=200)

    resp = as_guest.get("/api/v1/icbc/vehicles/LD626J",
                        follow_redirects=True,
                        content_type="application/json",
                        headers=_get_keycloak_auth_header(_get_keycloak_access_token()))
    assert resp.status_code == 200
    assert 'plateNumber' in resp.json[0]
    assert resp.json[0]['plateNumber'] == "LD626J"
    assert responses.calls[0].request.headers['loginUserId'] == 'larry@idir'


@responses.activate
def test_request_for_licence_plate_using_lowercase_automatically_converted_to_upper(as_guest, monkeypatch, roles):
    monkeypatch.setattr(middleware, "get_keycloak_certificates", _mock_keycloak_certificates)
    monkeypatch.setattr(middleware, "decode_keycloak_access_token", _get_authorized_user)

    responses.add(responses.GET,
                  '{}/vehicles?plateNumber={}&effectiveDate={}'.format(
                      Config.ICBC_API_ROOT,
                      "LD626J",
                      datetime.now().astimezone().replace(microsecond=0).isoformat()
                  ),
                  json=sample_vehicle_response(),
                  status=200)

    responses.add(responses.POST, "{}:{}/services/collector".format(
        Config.SPLUNK_HOST, Config.SPLUNK_PORT), status=200)

    resp = as_guest.get("/api/v1/icbc/vehicles/ld626j",
                        follow_redirects=True,
                        content_type="application/json",
                        headers=_get_keycloak_auth_header(_get_keycloak_access_token()))
    assert resp.status_code == 200
    assert 'plateNumber' in resp.json[0]
    assert resp.json[0]['plateNumber'] == "LD626J"
    assert responses.calls[0].request.headers['loginUserId'] == 'larry@idir'


def test_unauthorized_user_cannot_get_vehicle(as_guest, monkeypatch, roles):
    monkeypatch.setattr(middleware, "get_keycloak_certificates", _mock_keycloak_certificates)
    monkeypatch.setattr(middleware, "decode_keycloak_access_token", _get_unauthorized_user)
    resp = as_guest.get("/api/v1/icbc/vehicles/5120503",
                        follow_redirects=True,
                        content_type="application/json",
                        headers=_get_keycloak_auth_header("invalid-token"))
    assert resp.status_code == 401


def test_user_without_keycloak_login_cannot_get_vehicle(as_guest, monkeypatch):
    monkeypatch.setattr(middleware, "get_keycloak_certificates", _mock_keycloak_certificates)
    resp = as_guest.get("/api/v1/icbc/vehicles/5120503",
                        follow_redirects=True,
                        content_type="application/json",
                        headers=_get_keycloak_auth_header("invalid-token"))
    assert resp.status_code == 401


def test_authorized_user_gets_fake_vehicle_if_using_icbc_licence_plate(as_guest, monkeypatch, roles):
    # TODO - remove before flight - this functionality shouldn't go to production
    monkeypatch.setattr(middleware, "get_keycloak_certificates", _mock_keycloak_certificates)
    monkeypatch.setattr(middleware, "decode_keycloak_access_token", _get_authorized_user)
    # responds without calling ICBC - useful for demos when ICBC doesn't respond
    resp = as_guest.get("/api/v1/icbc/vehicles/ICBC",
                        follow_redirects=True,
                        content_type="application/json",
                        headers=_get_keycloak_auth_header(_get_keycloak_access_token()))
    assert resp.status_code == 200
    assert 'plateNumber' in resp.json[0]
    assert resp.json[0]['plateNumber'] == "LD626J"


def _sample_driver_response() -> dict:
    return {
      "dlNumber": "5120503",
      "birthDate": "1955-02-22",
      "party": {
        "ICBCEnterpriseID": "976949180580602",
        "partyType": "Person",
        "lastName": "JOHNSTONE",
        "firstName": "KAREN",
        "secondName": "PATRICIA",
        "thirdName": "",
        "nameType": "Legal",
        "birthDate": "1955-02-22",
        "dlNumber": "5120503",
        "dlPlaceOfIssue": "BC",
        "addresses": [
          {
            "addressType": "Mailing",
            "addressLine1": "9150 ARRASTRA CREEK FOREST SER",
            "addressLine2": "",
            "addressLine3": "",
            "city": "COALMONT",
            "region": "BC",
            "country": "CAN",
            "postalCode": "V0X1W0",
            "unitNumber": "",
            "streetNumber": "9150",
            "streetName": "ARRASTRA CREEK FOREST SERVICE",
            "streetType": "RD",
            "streetDirection": "",
            "boxNumber": "",
            "location": "",
            "postalStationName": "",
            "postalStationQualifier": "",
            "postalStationType": "",
            "routeServiceClass": "",
            "routeServiceNumber": "",
            "additionalDeliveryInfo": ""
          }
        ]
      }
    }


def sample_vehicle_response() -> list:
    return [
      {
        "plateNumber": "LD626J",
        "registrationNumber": "03371224",
        "vehicleIdNumber": "5Y2SL65806Z418645",
        "effectiveDate": "",
        "vehicleMake": "PONTIAC",
        "vehicleModel": "VIBE",
        "vehicleStyle": "FourDoorSedan",
        "vehicleModelYear": "2006",
        "vehicleColour": "Grey",
        "vehicleType": "Passenger",
        "nscNumber": "",
        "vehicleParties": [
          {
            "roleType": "RegisteredOwner",
            "party": {
              "ICBCEnterpriseID": "138929719980602",
              "partyType": "Person",
              "lastName": "WIEBE",
              "firstName": "ANDREW",
              "secondName": "JAMES",
              "thirdName": "",
              "nameType": "Legal",
              "birthDate": "1964-09-22",
              "dlNumber": "4714606",
              "dlPlaceOfIssue": "BC",
              "addresses": [
                {
                  "addressType": "Residence",
                  "addressLine1": "7608 HEATHER ST",
                  "addressLine2": "",
                  "addressLine3": "",
                  "city": "VANCOUVER",
                  "region": "BC",
                  "country": "CAN",
                  "postalCode": "V6P3R1",
                  "unitNumber": "",
                  "streetNumber": "7608",
                  "streetName": "HEATHER",
                  "streetType": "ST",
                  "streetDirection": "",
                  "boxNumber": "",
                  "location": "",
                  "postalStationName": "",
                  "postalStationQualifier": "",
                  "postalStationType": "",
                  "routeServiceClass": "",
                  "routeServiceNumber": "",
                  "additionalDeliveryInfo": ""
                }
              ]
            }
          }
        ]
      }
    ]


def _vehicle_not_found() -> dict:
    return {
      "error": {
        "code": 404,
        "message": "Not Found",
        "description": "vehicle not found",
        "request_uri": "/vehicles?plateNumber=LD626J",
        "request_id": "716243aa-ca18-441d-aa3e-e6e8776ca825"
      }
    }


def _driver_not_found() -> dict:
    return {
      "error": {
        "code": 404,
        "message": "Not Found",
        "description": "The resource specified in the request was not found",
        "request_uri": "/drivers/1234",
        "request_id": "091d5895-2942-4d48-848d-e6e8776c9600"
      }
    }


def _get_keycloak_access_token() -> str:
    return 'some-secret-access-token'


def _get_keycloak_auth_header(access_token) -> dict:
    return dict({
        'Authorization': 'Bearer {}'.format(access_token)
    })


def _mock_keycloak_certificates(**kwargs) -> tuple:
    logging.warning("inside _mock_keycloak_certificates()")
    return True, kwargs


def _get_unauthorized_user(**kwargs) -> tuple:
    logging.warning("inside _get_unauthorized_user()")
    kwargs['decoded_access_token'] = {'preferred_username': 'john@idir'}  # keycloak username
    return True, kwargs


def _get_authorized_user(**kwargs) -> tuple:
    logging.warning("inside _get_authorized_user()")
    kwargs['decoded_access_token'] = {'preferred_username': 'larry@idir'}  # keycloak username
    return True, kwargs
