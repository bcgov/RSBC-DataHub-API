import pytest
import base64
import logging
from datetime import datetime, timedelta
from python.prohibition_web_svc.models import Form
from python.prohibition_web_svc.app import db, create_app
from python.prohibition_web_svc.config import Config


@pytest.fixture
def app():
    return create_app()


@pytest.fixture
def as_guest(app):
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


@pytest.fixture
def database(app):
    with app.app_context():
        db.init_app(app)
        db.create_all()
        yield db
        db.drop_all()
        db.session.commit()


@pytest.fixture
def forms(database):
    today = datetime.strptime("2021-07-21", "%Y-%m-%d")
    yesterday = today - timedelta(days=1)
    forms = [
        Form(form_id='AA-123332', form_type='24Hour', username='larry@idir', lease_expiry=today, printed=None),
        Form(form_id='AA-123333', form_type='24Hour', username='larry@idir', lease_expiry=yesterday, printed=None),
        Form(form_id='AA-123334', form_type='12Hour', username='larry@idir', lease_expiry=yesterday, printed=None),
        Form(form_id='AA-11111', form_type='24Hour', username=None, lease_expiry=None, printed=None)
    ]
    db.session.bulk_save_objects(forms)
    db.session.commit()


def test_an_administrator_can_list_all_forms_by_type(as_guest, monkeypatch, forms):
    resp = as_guest.get("/api/v1/admin/forms?type=24Hour",
                        content_type="application/json",
                        headers=get_basic_authentication_header(monkeypatch))
    assert resp.status_code == 200
    logging.warning(str(resp.json))
    assert len(resp.json) == 3


def test_a_non_administrator_cannot_list_forms_by_type(as_guest, monkeypatch, forms):
    resp = as_guest.get("/api/v1/admin/forms?type=24Hour",
                        content_type="application/json")
    assert resp.status_code == 401


def test_an_administrator_can_add_a_12hour_form_id(as_guest, monkeypatch, forms, database):
    payload = {'form_type': '12Hour', 'form_id': 'J-100999'}
    resp = as_guest.post("/api/v1/admin/forms",
                         json=payload,
                         content_type="application/json",
                         headers=get_basic_authentication_header(monkeypatch))
    assert resp.status_code == 201
    assert database.session.query(Form) \
               .filter(Form.id == 'J-100999') \
               .filter(Form.form_type == '12Hour') \
               .filter(Form.username == None) \
               .count() == 1


def test_an_administrator_cannot_add_form_without_known_form_type(as_guest, monkeypatch, forms):
    payload = {'form_type': 'bad_type', 'form_id': 'J-100999'}
    resp = as_guest.post("/api/v1/admin/forms",
                         json=payload,
                         content_type="application/json",
                         headers=get_basic_authentication_header(monkeypatch))
    assert resp.status_code == 400


def test_an_administrator_cannot_add_form_with_emtpy_form_id(as_guest, monkeypatch, forms):
    payload = {'form_type': '12Hour', 'form_id': None}
    resp = as_guest.post("/api/v1/admin/forms",
                         json=payload,
                         content_type="application/json",
                         headers=get_basic_authentication_header(monkeypatch))
    assert resp.status_code == 400


def test_an_administrator_cannot_add_form_without_form_id(as_guest, monkeypatch, forms):
    payload = {'form_type': '12Hour'}
    resp = as_guest.post("/api/v1/admin/forms",
                         json=payload,
                         content_type="application/json",
                         headers=get_basic_authentication_header(monkeypatch))
    assert resp.status_code == 400


def get_basic_authentication_header(monkeypatch, username="name", password="secret") -> dict:
    monkeypatch.setattr(Config, "FLASK_BASIC_AUTH_USER", username)
    monkeypatch.setattr(Config, "FLASK_BASIC_AUTH_PASS", password)
    credentials = base64.b64encode((username + ":" + password).encode('utf-8')).decode('utf-8')
    headers = dict({"Authorization": "Basic {}".format(credentials)})
    logging.debug(headers)
    return headers