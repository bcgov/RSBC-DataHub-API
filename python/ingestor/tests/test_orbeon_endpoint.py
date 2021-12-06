import pytest
import base64
import logging
import logging.config
import os
import python.common.rsi_email as rsi_email
from python.ingestor.config import Config
import python.ingestor.routes as routes

os.environ['TZ'] = 'UTC'

@pytest.fixture
def client():
    routes.application.config['TESTING'] = True
    with routes.application.test_client() as client:
        yield client


def mock_rabbitmq(*args):
    print("mocking RabbitMQ")


def test_form_endpoint_rejects_json_payload(client, monkeypatch):
    monkeypatch.setattr(routes, "RabbitMQ", mock_rabbitmq)
    payload = dict({"data": "json"})
    response = client.post('/v1/publish/event/form', json=payload)
    json_data = response.json

    assert "received content type is not XML" in json_data['error']
    assert response.status_code == 422


def test_form_endpoint_rejects_payloads_that_exceed_max_length(client, monkeypatch):
    monkeypatch.setattr(routes, "RabbitMQ", mock_rabbitmq)

    payload = "<xml>" + "long_string" * 10000 + "</xml>"
    header = dict({"Content-Type": "application/xml"})
    response = client.post('/v1/publish/event/form', data=payload, headers=header)
    logging.warning(response.json)
    assert response.status_code == 422


def test_form_endpoint_rejects_submissions_with_incorrect_query_parameter(client, monkeypatch):
    monkeypatch.setattr(routes, "RabbitMQ", mock_rabbitmq)

    payload = "<xml>" + "long_string" * 100 + "</xml>"
    header = dict({"Content-Type": "application/xml"})
    params = dict({"form_name": "prohibition_review"})
    response = client.post('/v1/publish/event/form', data=payload, headers=header, query_string=params)
    logging.warning(response.json)
    json_data = response.json
    assert "missing key query parameter: form" in json_data['error']
    assert response.status_code == 422


def test_form_endpoint_rejects_submissions_with_bad_xml_payload(client, monkeypatch):
    monkeypatch.setattr(routes, "RabbitMQ", mock_rabbitmq)
    bad_payload = "<xml>" + "long_string" * 100
    header = dict({"Content-Type": "application/xml"})
    params = dict({"form": "prohibition_review"})
    response = client.post('/v1/publish/event/form', data=bad_payload, headers=header, query_string=params)
    logging.warning(response.json)
    json_data = response.json
    assert "something went wrong" in json_data['error']
    assert response.status_code == 500


def test_form_endpoint_returns_500_when_rabbitmq_not_available(client, monkeypatch):

    class RabbitMQ:
        def __init__(self, *args):
            pass

        def publish(*args):
            return False

    monkeypatch.setattr(routes, "RabbitMQ", RabbitMQ)

    payload = "<xml>" + "long_string" * 100 + "</xml>"
    header = dict({"Content-Type": "application/xml"})
    params = dict({"form": "prohibition_review"})
    response = client.post('/v1/publish/event/form', data=payload, headers=header, query_string=params)
    logging.warning(response.json)
    assert response.status_code == 500


def test_form_endpoint_saves_submissions_to_rabbitmq(client, monkeypatch):

    class RabbitMQ:
        def __init__(self, *args):
            pass

        def publish(*args):
            return True

    monkeypatch.setattr(routes, "RabbitMQ", RabbitMQ)

    payload = "<xml>" + "long_string" * 100 + "</xml>"
    header = dict({"Content-Type": "application/xml"})
    params = dict({"form": "prohibition_review"})
    response = client.post('/v1/publish/event/form', data=payload, headers=header, query_string=params)
    logging.warning(response.json)
    assert response.status_code == 200


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


def get_basic_authentication_header(monkeypatch, username="name", password="secret") -> dict:
    monkeypatch.setattr(Config, "FLASK_BASIC_AUTH_USER", username)
    monkeypatch.setattr(Config, "FLASK_BASIC_AUTH_PASS", password)
    credentials = base64.b64encode((username + ":" + password).encode('utf-8')).decode('utf-8')
    headers = dict({"Authorization": "Basic {}".format(credentials)})
    logging.debug(headers)
    return headers


def get_evidence_form_data(prohibition_number='20123456', last_name='Gordon'):
    return dict({
        "prohibition_number": prohibition_number,
        "last_name": last_name
    })


def schedule_get(days_offered=3) -> tuple:

    return True, dict({
        "time_slots": list([
            {
                "label": "Fri, Sep 4, 2020 - 10:00am to 11:30am",
                "value": "ZGF0YSB0byBiZSBlbmNvZGVk"
            },
            {
                "label": "Mon, Sep 7, 2020 - 10:00am to 11:30am",
                "value": "ZGF0YSB0byBiZSBlbmNvZGVk"
            },
            {
                "label": "Tue, Sep 8, 2020 - 10:00am to 11:30am",
                "value": "ZGF0YSB0byBiZSBlbmNvZGVk"
            }
        ]),
        "number_review_days_offered": days_offered
    })
