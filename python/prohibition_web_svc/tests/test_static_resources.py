import pytest
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


def test_get_agencies(as_guest):
    resp = as_guest.get(Config.URL_PREFIX + "/api/v1/agencies",
                        follow_redirects=True,
                        content_type="application/json")
    assert resp.status_code == 200
    assert "2101" in resp.json


def test_get_impound_lot_operators(as_guest):
    resp = as_guest.get(Config.URL_PREFIX + "/api/v1/impound_lot_operators",
                        follow_redirects=True,
                        content_type="application/json")
    assert resp.status_code == 200
    assert "24 Hour Towing" in resp.json[0]['name']
    

def test_get_provinces(as_guest):
    resp = as_guest.get(Config.URL_PREFIX + "/api/v1/provinces",
                        follow_redirects=True,
                        content_type="application/json")
    assert resp.status_code == 200
    assert 'objectCd' in resp.json[2]
    assert 'objectDsc' in resp.json[2]
    

def test_get_jurisdictions(as_guest):
    resp = as_guest.get(Config.URL_PREFIX + "/api/v1/jurisdictions",
                        follow_redirects=True,
                        content_type="application/json")
    assert resp.status_code == 200
    assert "AB" in resp.json[2]['objectCd']
    assert "Alberta" in resp.json[2]['objectDsc']
    

def test_get_countries(as_guest):
    resp = as_guest.get(Config.URL_PREFIX + "/api/v1/countries",
                        follow_redirects=True,
                        content_type="application/json")
    assert resp.status_code == 200
    assert 'objectCd' in resp.json[2]
    assert 'objectDsc' in resp.json[2]
    

def test_get_cities(as_guest):
    resp = as_guest.get(Config.URL_PREFIX + "/api/v1/cities",
                        follow_redirects=True,
                        content_type="application/json")
    assert resp.status_code == 200
    assert "Victoria" in resp.json
    assert "100 Mile House" in resp.json
    

def test_get_car_colors(as_guest):
    resp = as_guest.get(Config.URL_PREFIX + "/api/v1/colors",
                        follow_redirects=True,
                        content_type="application/json")
    assert resp.status_code == 200
    assert "BLU" in resp.json
    

def test_get_vehicles(as_guest):
    resp = as_guest.get(Config.URL_PREFIX + "/api/v1/vehicles",
                        follow_redirects=True,
                        content_type="application/json")
    assert resp.status_code == 200
    assert "AC" == resp.json[0]['make']
    assert "300" == resp.json[0]['model']


def test_get_vehicle_styles(as_guest):
    resp = as_guest.get(Config.URL_PREFIX + "/api/v1/vehicle_styles",
                        follow_redirects=True,
                        content_type="application/json")
    assert resp.status_code == 200
    assert "2DR" == resp.json[0]

