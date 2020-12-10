import pytest
import datetime
import base64
import logging
import python.common.rsi_email as rsi_email
from python.ingestor.config import Config
import python.common.vips_api as vips
import python.ingestor.routes as routes


@pytest.fixture
def client():
    routes.application.config['TESTING'] = True
    with routes.application.test_client() as client:
        yield client


def mock_rabbitmq(*args):
    print("mocking RabbitMQ")


def test_check_templates_endpoint(client, monkeypatch):

    monkeypatch.setattr(Config, "ENVIRONMENT", "dev")
    monkeypatch.setattr(routes, "RabbitMQ", mock_rabbitmq)

    response = client.get('/check_templates')
    assert "Email Templates" in str(response.data)
    assert response.status_code == 200


@pytest.mark.parametrize("environment", [('prod', 'test')])
def test_check_templates_endpoint_responds_only_in_dev(environment, client, monkeypatch):

    monkeypatch.setattr(Config, "ENVIRONMENT", environment)
    monkeypatch.setattr(routes, "RabbitMQ", mock_rabbitmq)

    with pytest.raises(TypeError):
        client.get('/check_templates')


@pytest.mark.parametrize("template", rsi_email.content_data().keys())
def test_check_endpoint(template, client, monkeypatch):

    monkeypatch.setattr(Config, "ENVIRONMENT", "dev")
    monkeypatch.setattr(routes, "RabbitMQ", mock_rabbitmq)

    response = client.get('/check?template=' + template)
    assert response.status_code == 200


@pytest.mark.parametrize("template", rsi_email.content_data())
def test_check_endpoint_does_not_respond_in_test(template, client, monkeypatch):

    monkeypatch.setattr(Config, "ENVIRONMENT", "test")
    monkeypatch.setattr(routes, "RabbitMQ", mock_rabbitmq)

    with pytest.raises(TypeError):
        client.get('/check?template=' + template[0])


@pytest.mark.parametrize("template", rsi_email.content_data())
def test_check_endpoint_does_not_respond_in_prod(template, client, monkeypatch):

    monkeypatch.setattr(Config, "ENVIRONMENT", "prod")
    monkeypatch.setattr(routes, "RabbitMQ", mock_rabbitmq)

    with pytest.raises(TypeError):
        client.get('/check?template=' + template[0])


def test_the_evidence_endpoint_requires_basic_auth(client, monkeypatch):

    monkeypatch.setattr(routes, "RabbitMQ", mock_rabbitmq)

    response = client.post('/evidence', data=dict({
        "prohibition_number": "99999",
        "last_name": "smith"
    }))
    assert response.status_code == 401  # Unauthorized


def test_an_applicant_cannot_submit_evidence_with_prohibition_number_that_is_too_short(client, monkeypatch):

    monkeypatch.setattr(routes, "RabbitMQ", mock_rabbitmq)

    response = client.post('/evidence',
                           headers=get_basic_authentication_header(monkeypatch),
                           data=get_evidence_form_data('99999'))
    json_data = response.json
    assert response.status_code == 200
    assert 'You have entered an invalid prohibition number, please try again.' in json_data['data']['error']
    assert json_data['data']['is_valid'] is False


def test_an_applicant_cannot_submit_evidence_after_their_review_has_concluded(client, monkeypatch):

    def mock_status_get(*args, **kwargs):
        return status_gets(True, "IRP", "2020-09-01", True, "2020-09-15", "Gordon", True)

    monkeypatch.setattr(vips, "status_get", mock_status_get)
    monkeypatch.setattr(routes, "RabbitMQ", mock_rabbitmq)

    response = client.post('/evidence',
                           headers=get_basic_authentication_header(monkeypatch),
                           data=get_evidence_form_data())
    json_data = response.json
    assert response.status_code == 200
    assert "You can't submit evidence less than 48 hours before your review." in json_data['data']['error']
    assert json_data['data']['is_valid'] is False


def test_an_applicant_cannot_submit_evidence_if_they_have_not_applied(client, monkeypatch):

    def mock_status_get(*args, **kwargs):
        return status_gets(True, "IRP", "2020-09-01", True, "2020-09-15", "Gordon", False)

    monkeypatch.setattr(vips, "status_get", mock_status_get)
    monkeypatch.setattr(routes, "RabbitMQ", mock_rabbitmq)

    response = client.post('/evidence',
                           headers=get_basic_authentication_header(monkeypatch),
                           data=get_evidence_form_data())
    json_data = response.json
    assert response.status_code == 200
    assert "You must apply before you can submit evidence." in json_data['data']['error']
    assert json_data['data']['is_valid'] is False


def test_an_applicant_cannot_submit_evidence_if_they_have_not_paid(client, monkeypatch):

    def mock_status_get(*args, **kwargs):
        return status_gets(True, "IRP", "2020-09-01", False, "2020-09-15", "Gordon", True)

    monkeypatch.setattr(vips, "status_get", mock_status_get)
    monkeypatch.setattr(routes, "RabbitMQ", mock_rabbitmq)

    response = client.post('/evidence',
                           headers=get_basic_authentication_header(monkeypatch),
                           data=get_evidence_form_data())
    json_data = response.json
    assert response.status_code == 200
    assert "You must pay before you can submit evidence." in json_data['data']['error']
    assert json_data['data']['is_valid'] is False


def test_an_applicant_cannot_submit_evidence_if_their_last_name_does_not_match_vips(client, monkeypatch):

    def mock_status_get(*args, **kwargs):
        return status_gets(True, "IRP", "2020-09-01", True, "2020-09-15", "Wrong-Name", True)

    monkeypatch.setattr(vips, "status_get", mock_status_get)
    monkeypatch.setattr(routes, "RabbitMQ", mock_rabbitmq)

    response = client.post('/evidence',
                           headers=get_basic_authentication_header(monkeypatch),
                           data=get_evidence_form_data())
    json_data = response.json
    assert response.status_code == 200
    assert "The last name doesn't match a driving prohibition in the system." in json_data['data']['error']
    assert json_data['data']['is_valid'] is False


def test_an_applicant_cannot_submit_evidence_if_no_matching_prohibition_in_vips(client, monkeypatch):

    monkeypatch.setattr(vips, "status_get", mock_status_not_found)
    monkeypatch.setattr(routes, "RabbitMQ", mock_rabbitmq)

    response = client.post('/evidence',
                           headers=get_basic_authentication_header(monkeypatch),
                           data=get_evidence_form_data())
    json_data = response.json
    assert response.status_code == 200
    assert "The driving prohibition isn't in the system." in json_data['data']['error']
    assert json_data['data']['is_valid'] is False


def test_an_applicant_cannot_submit_evidence_if_the_review_date_is_less_than_48hrs_from_now(client, monkeypatch):
    iso_format = "%Y-%m-%d"
    date_served = (datetime.datetime.now() - datetime.timedelta(days=7)).strftime(iso_format)
    review_start_date = (datetime.datetime.now() + datetime.timedelta(days=2)).strftime(iso_format)
    logging.debug("datetimes: {} | {}".format(date_served, review_start_date))

    def mock_status_get(*args, **kwargs):
        return status_gets(True, "IRP", date_served, True, review_start_date, "Gordon", True)

    monkeypatch.setattr(vips, "status_get", mock_status_get)
    monkeypatch.setattr(routes, "RabbitMQ", mock_rabbitmq)

    response = client.post('/evidence',
                           headers=get_basic_authentication_header(monkeypatch),
                           data=get_evidence_form_data())
    json_data = response.json
    assert response.status_code == 200
    assert "You can't submit evidence less than 48 hours before your review." in json_data['data']['error']
    assert json_data['data']['is_valid'] is False


def test_an_applicant_cannot_submit_evidence_if_the_review_date_has_not_been_scheduled(client, monkeypatch):
    iso_format = "%Y-%m-%d"
    date_served = (datetime.datetime.now() - datetime.timedelta(days=7)).strftime(iso_format)

    def mock_status_get(*args, **kwargs):
        return status_gets(True, "IRP", date_served, True, "", "Gordon", True)

    monkeypatch.setattr(vips, "status_get", mock_status_get)
    monkeypatch.setattr(routes, "RabbitMQ", mock_rabbitmq)

    response = client.post('/evidence',
                           headers=get_basic_authentication_header(monkeypatch),
                           data=get_evidence_form_data())
    json_data = response.json
    assert response.status_code == 200
    assert "You must book a review date before you can submit evidence for the review." in json_data['data']['error']
    assert json_data['data']['is_valid'] is False


def test_an_applicant_can_submit_evidence_happy_path(client, monkeypatch):
    iso_format = "%Y-%m-%d"
    date_served = (datetime.datetime.now() - datetime.timedelta(days=7)).strftime(iso_format)
    review_start_date = (datetime.datetime.now() + datetime.timedelta(days=3)).strftime(iso_format)

    def mock_status_get(*args, **kwargs):
        return status_gets(True, "IRP", date_served, True, review_start_date, "Gordon", True)

    monkeypatch.setattr(vips, "status_get", mock_status_get)
    monkeypatch.setattr(routes, "RabbitMQ", mock_rabbitmq)

    response = client.post('/evidence',
                           headers=get_basic_authentication_header(monkeypatch),
                           data=get_evidence_form_data())
    json_data = response.json
    assert response.status_code == 200
    assert json_data['data']['is_valid'] is True


def get_basic_authentication_header(monkeypatch, username="name", password="secret") -> dict:
    monkeypatch.setattr(Config, "FLASK_BASIC_AUTH_USER", username)
    monkeypatch.setattr(Config, "FLASK_BASIC_AUTH_PASS", password)
    credentials = base64.b64encode((username + ":" + password).encode('utf-8')).decode('utf-8')
    headers = dict({"Authorization": "Basic {}".format(credentials)})
    logging.debug(headers)
    return headers


def get_evidence_form_data(prohibition_number='00999999', last_name='Gordon'):
    return dict({
        "prohibition_number": prohibition_number,
        "last_name": last_name
    })


def mock_status_not_found(*args, **kwargs):
    return True, dict({
        "resp": "fail",
        "error": {
            "message": "Record not found",
            "httpStatus": 404
        }
    })


def status_gets(is_success, prohibition_type, date_served, is_paid, review_start_date, last_name, is_applied):
    data = {
            "resp": "success",
            "data": {
                "status": {
                    "noticeTypeCd": prohibition_type,
                    "noticeServedDt": date_served + " 00:00:00 -08:00",
                    "reviewFormSubmittedYn": "N",
                    "reviewCreatedYn": "N",
                    "originalCause": "IRP7",
                    "surnameNm": last_name,
                    "driverLicenceSeizedYn": "Y",
                    "disclosure": []
                }
            }
        }
    if len(review_start_date) > 0:
        data['data']['status']['reviewStartDtm'] = review_start_date + ' 09:30:00 -07:00'
    if is_paid:
        data['data']['status']['receiptNumberTxt'] = 'AAABBB123'
    if is_applied:
        data['data']['status']['applicationId'] = 'GUID-GUID-GUID-GUID'
    return is_success, data

