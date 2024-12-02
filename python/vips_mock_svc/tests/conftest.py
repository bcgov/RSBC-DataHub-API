import pytest
import base64
import logging
from python.vips_mock_svc.vips_mock_svc.config import Config
from python.vips_mock_svc.vips_mock_svc.app import create_app


@pytest.fixture
def application():
    return create_app()


@pytest.fixture
def as_guest(application):
    application.config['TESTING'] = True
    with application.test_client() as client:
        yield client


@pytest.fixture()
def auth_header(monkeypatch, username="name", password="secret") -> dict:
    monkeypatch.setattr(Config, "BASIC_AUTH_USER", username)
    monkeypatch.setattr(Config, "BASIC_AUTH_PASS", password)
    credentials = base64.b64encode((username + ":" + password).encode('utf-8')).decode('utf-8')
    headers = {"Authorization": "Basic {}".format(credentials)}
    logging.warning("add_basic_authentication_header: {} {} {}".format(str(headers), username, password))
    return headers
