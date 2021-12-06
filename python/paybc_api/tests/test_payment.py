import pytest
import python.common.tests.vips_mock as vips_mock
import pytz
import json
import datetime
import logging
import logging.config
import base64
import responses
from python.paybc_api.website.config import Config
from python.common.tests.rabbit_mock import MockRabbitMQ
import python.paybc_api.website.routes as routes
import python.paybc_api.website.app as app
import python.common.common_email_services as common_email


@pytest.fixture
def client(monkeypatch):
    monkeypatch.setattr(Config, "PAYBC_CLIENT_ID", "client-id")
    monkeypatch.setattr(Config, "PAYBC_CLIENT_SECRET", "secret")
    monkeypatch.setenv("AUTHLIB_INSECURE_TRANSPORT", '1')
    monkeypatch.setattr(Config, "ABSOLUTE_DB_PATH", "/tmp")
    application = app.create_app(Config)
    application.testing = True
    with application.test_client() as client:
        yield client


@pytest.fixture
def token(client, monkeypatch):
    headers = get_basic_authentication_header(Config)
    logging.info(headers)
    response = client.post('/oauth/token', data={'grant_type': 'client_credentials'}, headers=headers)
    token = response.json['access_token']
    logging.info("token {}".format(token))
    return token


def test_get_token_endpoint(client, monkeypatch):
    headers = get_basic_authentication_header(Config)
    logging.info(headers)
    response = client.post('/oauth/token', data={'grant_type': 'client_credentials'}, headers=headers)
    logging.info(response.json)
    assert response.status_code == 200


def test_search_endpoint_requires_an_access_token(token, client, monkeypatch):
    response = client.get('/api_v2/search', query_string=get_search_payload())
    logging.warning("search: {}".format(response.json))
    assert response.status_code == 401


@pytest.mark.parametrize("prohibition_types", ['IRP', 'ADP', 'UL'])
@responses.activate
def test_applicant_search_returns_error_if_entered_last_name_incorrect(prohibition_types, token, client):
    responses.add(responses.GET,
                  '{}/{}/status/{}'.format(Config.VIPS_API_ROOT_URL, "20123456", "20123456"),
                  json=vips_mock.status_applied_not_paid(prohibition_types),
                  status=404, match_querystring=True)
    response = client.get('/api_v2/search', query_string=get_search_payload(last_name='Missing'), headers=get_oauth_auth_header(token))
    logging.info("search: {}".format(response.json))
    assert "The last name doesn't match a driving prohibition in the system." in response.json['error']
    assert response.status_code == 200


@pytest.mark.parametrize("prohibition_types", ['IRP', 'ADP', 'UL'])
@responses.activate
def test_applicant_search_returns_error_if_already_paid(prohibition_types, token, client):
    responses.add(responses.GET,
                  '{}/{}/status/{}'.format(Config.VIPS_API_ROOT_URL, "20123456", "20123456"),
                  json=vips_mock.status_applied_and_paid_not_scheduled(prohibition_types),
                  status=200)
    response = client.get('/api_v2/search', query_string=get_search_payload(), headers=get_oauth_auth_header(token))
    logging.info("search: {}".format(response.json))
    assert "The application review fee has already been paid." in response.json['error']
    assert response.status_code == 200


@responses.activate
def test_applicant_search_returns_error_if_not_found_in_vips(token, client):
    responses.add(responses.GET,
                  '{}/{}/status/{}'.format(Config.VIPS_API_ROOT_URL, "20123456", "20123456"),
                  json=vips_mock.status_not_found(),
                  status=404)
    response = client.get('/api_v2/search', query_string=get_search_payload(), headers=get_oauth_auth_header(token))
    logging.info("search: {}".format(response.json))
    assert "The driving prohibition isn't in the system." in response.json['error']
    assert response.status_code == 200


@pytest.mark.parametrize("prohibition_type", ['IRP', 'ADP'])
@responses.activate
def test_applicant_search_returns_error_if_irp_or_adp_older_than_8_days(prohibition_type, token, client):
    iso_format = "%Y-%m-%d"
    tz = pytz.timezone('America/Vancouver')
    date_served = (datetime.datetime.now(tz) - datetime.timedelta(days=9)).strftime(iso_format)

    responses.add(responses.GET,
                  '{}/{}/status/{}'.format(Config.VIPS_API_ROOT_URL, "20123456", "20123456"),
                  json=vips_mock.status_applied_not_paid(prohibition_type, date_served),
                  status=200)

    response = client.get('/api_v2/search', query_string=get_search_payload(), headers=get_oauth_auth_header(token))
    logging.info("search: {}".format(response.json['error']))
    assert "The Notice of Prohibition was issued more than 7 days ago." in response.json['error']
    assert response.status_code == 200


@pytest.mark.parametrize("prohibition_type", ['IRP', 'ADP'])
@responses.activate
def test_applicant_search_successful_if_irp_or_adp_7_days_old(prohibition_type, token, client):
    iso_format = "%Y-%m-%d"
    tz = pytz.timezone('America/Vancouver')
    date_served = (datetime.datetime.now(tz) - datetime.timedelta(days=8)).strftime(iso_format)

    responses.add(responses.GET,
                  '{}/{}/status/{}'.format(Config.VIPS_API_ROOT_URL, "20123456", "20123456"),
                  json=vips_mock.status_applied_not_paid(prohibition_type, date_served),
                  status=200)

    response = client.get('/api_v2/search', query_string=get_search_payload(), headers=get_oauth_auth_header(token))
    logging.info("search: {}".format(response.json))
    assert "error" not in response.json
    assert "https://localhost/api_v2/invoice/20123456" in response.json['items'][0]['selected_invoice']['$ref']
    assert response.status_code == 200


@responses.activate
def test_applicant_search_successful_if_a_ul_review_older_than_8_days(token, client):
    iso_format = "%Y-%m-%d"
    tz = pytz.timezone('America/Vancouver')
    date_served = (datetime.datetime.now(tz) - datetime.timedelta(days=9)).strftime(iso_format)

    responses.add(responses.GET,
                  '{}/{}/status/{}'.format(Config.VIPS_API_ROOT_URL, "20123456", "20123456"),
                  json=vips_mock.status_applied_not_paid("UL", date_served),
                  status=200)

    response = client.get('/api_v2/search', query_string=get_search_payload(), headers=get_oauth_auth_header(token))
    logging.info("search: {}".format(response.json))
    assert "error" not in response.json
    assert "https://localhost/api_v2/invoice/20123456" in response.json['items'][0]['selected_invoice']['$ref']
    assert response.status_code == 200


@pytest.mark.parametrize("prohibition_number", ['20123456', '20123457'])
@responses.activate
def test_successful_search_response_includes_url_to_invoice_endpoint(prohibition_number, token, client):
    iso_format = "%Y-%m-%d"
    tz = pytz.timezone('America/Vancouver')
    date_served = (datetime.datetime.now(tz) - datetime.timedelta(days=6)).strftime(iso_format)

    responses.add(responses.GET,
                  '{}/{}/status/{}'.format(Config.VIPS_API_ROOT_URL, prohibition_number, prohibition_number),
                  json=vips_mock.status_applied_not_paid("UL", date_served),
                  status=200)

    response = client.get('/api_v2/search',
                          query_string=get_search_payload(prohibition_number),
                          headers=get_oauth_auth_header(token))
    logging.info("search: {}".format(response.json))
    endpoint = "https://localhost/api_v2/invoice/{}".format(prohibition_number)
    assert "error" not in response.json
    assert endpoint in response.json['items'][0]['selected_invoice']['$ref']
    assert response.status_code == 200


def test_invoice_endpoint_requires_an_access_token(client):
    response = client.get('/api_v2/invoice/20123456')
    logging.info("invoice: {}".format(response.json))
    assert response.status_code == 401


@responses.activate
def test_search_endpoint_gracefully_handles_text_response_from_vips(token, client):

    responses.add(responses.GET,
                  '{}/{}/status/{}'.format(Config.VIPS_API_ROOT_URL, "20123456", "20123456"),
                  body=vips_mock.status_returns_html_response(),
                  status=200)

    response = client.get('/api_v2/search', query_string=get_search_payload(), headers=get_oauth_auth_header(token))
    logging.info("search: {}".format(response.json))
    assert "error" in response.json
    assert response.status_code == 200


@pytest.mark.parametrize("prohibition_types", ['IRP', 'ADP', 'UL'])
@responses.activate
def test_applicant_invoice_returns_error_if_already_paid(prohibition_types, token, client):

    responses.add(responses.GET,
                  '{}/{}/status/{}'.format(Config.VIPS_API_ROOT_URL, "20123456", "20123456"),
                  json=vips_mock.status_applied_and_paid_not_scheduled(prohibition_types),
                  status=200)

    response = client.get('/api_v2/invoice/20123456', headers=get_oauth_auth_header(token))
    logging.info("invoice: {}".format(response.json))
    assert "The application review fee has already been paid." in response.json['error']
    assert response.status_code == 200


@responses.activate
def test_applicant_invoice_returns_error_if_not_found_in_vips(token, client):

    responses.add(responses.GET,
                  '{}/{}/status/{}'.format(Config.VIPS_API_ROOT_URL, "20123456", "20123456"),
                  json=vips_mock.status_not_found(),
                  status=200)

    response = client.get('/api_v2/invoice/20123456', headers=get_oauth_auth_header(token))
    logging.info("invoice: {}".format(response.json))
    assert "The driving prohibition isn't in the system." in response.json['error']
    assert response.status_code == 200


@pytest.mark.parametrize("prohibition_type", ['IRP', 'ADP'])
@responses.activate
def test_applicant_invoice_returns_error_if_irp_or_adp_older_than_8_days(prohibition_type, token, client):
    iso_format = "%Y-%m-%d"
    tz = pytz.timezone('America/Vancouver')
    date_served = (datetime.datetime.now(tz) - datetime.timedelta(days=9)).strftime(iso_format)

    responses.add(responses.GET,
                  '{}/{}/status/{}'.format(Config.VIPS_API_ROOT_URL, "20123456", "20123456"),
                  json=vips_mock.status_applied_not_paid(prohibition_type, date_served),
                  status=200)

    response = client.get('/api_v2/invoice/20123456', headers=get_oauth_auth_header(token))
    logging.info("invoice: {}".format(response.json))
    assert "The Notice of Prohibition was issued more than 7 days ago." in response.json['error']
    assert response.status_code == 200


@responses.activate
def test_applicant_invoice_successful_if_a_ul_review_older_than_8_days(token, client):
    iso_format = "%Y-%m-%d"
    tz = pytz.timezone('America/Vancouver')
    date_served = (datetime.datetime.now(tz) - datetime.timedelta(days=9)).strftime(iso_format)

    responses.add(responses.GET,
                  '{}/{}/status/{}'.format(Config.VIPS_API_ROOT_URL, "20123456", "20123456"),
                  json=vips_mock.status_applied_not_paid("UL", date_served),
                  status=200)

    responses.add(responses.GET,
                  '{}/{}/application/{}'.format(
                      Config.VIPS_API_ROOT_URL, "bb71037c-f87b-0444-e054-00144ff95452", "20123456"),
                  json=vips_mock.application_get(),
                  status=200)

    response = client.get('/api_v2/invoice/20123456', headers=get_oauth_auth_header(token))
    logging.info("invoice: {}".format(response.json))
    assert "error" not in response.json
    assert "20123456" == response.json["invoice_number"]
    assert "10008" == response.json["pbc_ref_number"]
    assert 50 == response.json["total"]
    assert 50 == response.json["amount_due"]
    assert 0 == response.json["party_number"]
    assert response.status_code == 200


@pytest.mark.parametrize("prohibition_type", ['IRP', 'ADP'])
@responses.activate
def test_successful_invoice_response_includes_url_to_invoice_endpoint(prohibition_type, token, client):
    iso_format = "%Y-%m-%d"
    tz = pytz.timezone('America/Vancouver')
    date_served = (datetime.datetime.now(tz) - datetime.timedelta(days=7)).strftime(iso_format)

    responses.add(responses.GET,
                  '{}/{}/status/{}'.format(Config.VIPS_API_ROOT_URL, "20123456", "20123456"),
                  json=vips_mock.status_applied_not_paid(prohibition_type, date_served),
                  status=200)

    responses.add(responses.GET,
                  '{}/{}/application/{}'.format(
                      Config.VIPS_API_ROOT_URL, "bb71037c-f87b-0444-e054-00144ff95452", "20123456"),
                  json=vips_mock.application_get("ORAL"),
                  status=200)

    response = client.get('/api_v2/invoice/20123456', headers=get_oauth_auth_header(token))
    logging.info("invoice: {}".format(response.json))
    assert "error" not in response.json
    assert "20123456" == response.json["invoice_number"]
    assert "10008" == response.json["pbc_ref_number"]
    assert 200 == response.json["total"]
    assert 200 == response.json["amount_due"]
    assert 0 == response.json["party_number"]
    assert response.status_code == 200


@pytest.mark.parametrize("presentation_type", [['ORAL', 200],  ['WRIT', 100]])
@responses.activate
def test_invoice_amount_is_determined_by_review_presentation_type(presentation_type, token, client):
    iso_format = "%Y-%m-%d"
    tz = pytz.timezone('America/Vancouver')
    date_served = (datetime.datetime.now(tz) - datetime.timedelta(days=6)).strftime(iso_format)

    responses.add(responses.GET,
                  '{}/{}/status/{}'.format(Config.VIPS_API_ROOT_URL, "20123456", "20123456"),
                  json=vips_mock.status_applied_not_paid("IRP", date_served),
                  status=200)

    responses.add(responses.GET,
                  '{}/{}/application/{}'.format(
                      Config.VIPS_API_ROOT_URL, "bb71037c-f87b-0444-e054-00144ff95452", "20123456"),
                  json=vips_mock.application_get(presentation_type[0]),
                  status=200)

    response = client.get('/api_v2/invoice/20123456', headers=get_oauth_auth_header(token))
    logging.info("invoice: {}".format(response.json))
    assert "error" not in response.json
    assert "20123456" == response.json["invoice_number"]
    assert "10008" == response.json["pbc_ref_number"]
    assert presentation_type[1] == response.json["total"]
    assert presentation_type[1] == response.json["amount_due"]
    assert 0 == response.json["party_number"]
    assert response.status_code == 200


def test_receipt_endpoint_requires_an_access_token(client):
    response = client.post('/api_v2/receipt')
    logging.info("receipt: {}".format(response.json))
    assert response.status_code == 401


@pytest.mark.parametrize("prohibition_types", ['IRP', 'ADP', 'UL'])
@responses.activate
def test_receipt_endpoint_returns_error_if_prohibition_not_found(prohibition_types, token, client, monkeypatch):

    responses.add(responses.GET,
                  '{}/{}/status/{}'.format(Config.VIPS_API_ROOT_URL, "20123456", "20123456"),
                  json=vips_mock.status_not_found(),
                  status=404)

    monkeypatch.setattr(routes, "RabbitMQ", MockRabbitMQ)

    response = client.post('/api_v2/receipt',
                           headers=get_oauth_auth_header(token),
                           json=get_receipt_payload())
    logging.info("receipt: {}".format(response.json))
    assert "INCMP" in response.json['status']  # INCMP == INCOMPLETE
    assert response.status_code == 400


@pytest.mark.parametrize("prohibition_types", ['IRP', 'ADP', 'UL'])
@responses.activate
def test_receipt_endpoint_returns_error_if_application_not_saved(prohibition_types, token, client, monkeypatch):
    responses.add(responses.GET,
                  '{}/{}/status/{}'.format(Config.VIPS_API_ROOT_URL, "20123456", "20123456"),
                  json=vips_mock.status_has_never_applied(prohibition_types),
                  status=200)

    monkeypatch.setattr(routes, "RabbitMQ", MockRabbitMQ)

    response = client.post('/api_v2/receipt', headers=get_oauth_auth_header(token), json=get_receipt_payload())
    logging.info("receipt: {}".format(response.json))
    assert "INCMP" in response.json['status']  # INCMP == INCOMPLETE
    assert response.status_code == 400


@pytest.mark.parametrize("prohibition_types", ['IRP', 'ADP', 'UL'])
@responses.activate
def test_receipt_endpoint_returns_error_if_application_data_not_returned(prohibition_types, token, client, monkeypatch):

    responses.add(responses.GET,
                  '{}/{}/status/{}'.format(Config.VIPS_API_ROOT_URL, "20123456", "20123456"),
                  json=vips_mock.status_applied_not_paid(prohibition_types),
                  status=200)

    responses.add(responses.GET,
                  '{}/{}/application/{}'.format(
                      Config.VIPS_API_ROOT_URL, "bb71037c-f87b-0444-e054-00144ff95452", "20123456"),
                  json=vips_mock.application_get_not_found(), status=404)

    monkeypatch.setattr(routes, "RabbitMQ", MockRabbitMQ)
    response = client.post('/api_v2/receipt', headers=get_oauth_auth_header(token), json=get_receipt_payload())
    logging.info("receipt: {}".format(response.json))
    assert "INCMP" in response.json['status']  # INCMP == INCOMPLETE
    assert response.status_code == 400


@pytest.mark.parametrize("prohibition_types", ['IRP', 'ADP', 'UL'])
@responses.activate
def test_receipt_endpoint_returns_success_if_prohibition_already_paid(prohibition_types, token, client, monkeypatch):
    """
    In the event that VIPS status says the application for review has already been paid, return a successful
    response to PayBC.  If we don't send a successful response, PayBC will try again and again indefinitely.
    PayBC likely didn't receive the initial successful response, so is trying again.
    """

    responses.add(responses.GET,
                  '{}/{}/status/{}'.format(Config.VIPS_API_ROOT_URL, "20123456", "20123456"),
                  json=vips_mock.status_applied_and_paid_not_scheduled(prohibition_types), status=200)

    responses.add(responses.GET,
                  '{}/{}/application/{}'.format(
                      Config.VIPS_API_ROOT_URL, "bb71037c-f87b-0444-e054-00144ff95452", "20123456"),
                  json=vips_mock.application_get(), status=200)

    def mock_send_email(*args, **kwargs):
        return True

    class TestRabbit(MockRabbitMQ):

        @staticmethod
        def publish(*args):
            assert "DF.hold" in args[0]
            return True

    monkeypatch.setattr(routes, "RabbitMQ", TestRabbit)
    monkeypatch.setattr(common_email, "send_email", mock_send_email)

    response = client.post('/api_v2/receipt',
                           headers=get_oauth_auth_header(token),
                           json=get_receipt_payload())
    logging.info("receipt: {}".format(response.json))
    assert "APP" in response.json['status']  # APP == APPROVED
    assert response.status_code == 200


@pytest.mark.parametrize("prohibition_types", ['IRP', 'ADP', 'UL'])
@responses.activate
def test_receipt_endpoint_returns_success_creates_verify_schedule_event(prohibition_types, token, client, monkeypatch):

    responses.add(responses.GET,
                  '{}/{}/status/{}'.format(Config.VIPS_API_ROOT_URL, "20123456", "20123456"),
                  json=vips_mock.status_applied_not_paid(prohibition_types), status=200)

    responses.add(responses.GET,
                  '{}/{}/application/{}'.format(
                      Config.VIPS_API_ROOT_URL, "bb71037c-f87b-0444-e054-00144ff95452", "20123456"),
                  json=vips_mock.application_get(), status=200)

    responses.add(responses.PATCH,
                  '{}/{}/payment/{}'.format(
                      Config.VIPS_API_ROOT_URL, "bb71037c-f87b-0444-e054-00144ff95452", "20123456"),
                  json=vips_mock.payment_patch_payload(), status=200)

    def mock_send_email(*args, **kwargs):
        return True

    class TestRabbit(MockRabbitMQ):

        @staticmethod
        def publish(*args):
            message_string = args[1].decode("utf-8")
            message = json.loads(message_string)
            assert "verify_schedule" in message
            assert message['verify_schedule']['order_number'] == "1002581"
            assert message['verify_schedule']['applicant_name'] == "Developer Norris"
            assert "DF.hold" in args[0]
            return True

    monkeypatch.setattr(routes, "RabbitMQ", TestRabbit)
    monkeypatch.setattr(common_email, "send_email", mock_send_email)

    response = client.post('/api_v2/receipt',
                           headers=get_oauth_auth_header(token),
                           json=get_receipt_payload())
    logging.info("receipt: {}".format(response.json))
    assert "APP" in response.json['status']  # APP == APPROVED
    assert response.status_code == 200


@pytest.mark.parametrize("prohibition_types", ['IRP', 'ADP', 'UL'])
@responses.activate
def test_receipt_endpoint_returns_success_and_sends_schedule_email(prohibition_types, token, client, monkeypatch, caplog):
    caplog.set_level(logging.INFO)
    responses.add(responses.GET,
                  '{}/{}/status/{}'.format(Config.VIPS_API_ROOT_URL, "20123456", "20123456"),
                  json=vips_mock.status_applied_not_paid(prohibition_types), status=200)

    responses.add(responses.GET,
                  '{}/{}/application/{}'.format(
                      Config.VIPS_API_ROOT_URL, "bb71037c-f87b-0444-e054-00144ff95452", "20123456"),
                  json=vips_mock.application_get(), status=200)

    responses.add(responses.PATCH,
                  '{}/{}/payment/{}'.format(
                      Config.VIPS_API_ROOT_URL, "bb71037c-f87b-0444-e054-00144ff95452", "20123456"),
                  json=vips_mock.payment_patch_payload(), status=200)

    responses.add(responses.POST, "{}:{}/services/collector".format(
        Config.SPLUNK_HOST, Config.SPLUNK_PORT), status=200)

    responses.add(responses.POST, '{}/realms/{}/protocol/openid-connect/token'.format(
        Config.COMM_SERV_AUTH_URL, Config.COMM_SERV_REALM), json={"access_token": "token"}, status=200)

    responses.add(responses.POST, '{}/api/v1/email'.format(
        Config.COMM_SERV_API_ROOT_URL), json={"sample": "test"}, status=201)

    class TestRabbit(MockRabbitMQ):

        @staticmethod
        def publish(*args):
            return True

    monkeypatch.setattr(routes, "RabbitMQ", TestRabbit)

    response = client.post('/api_v2/receipt',
                           headers=get_oauth_auth_header(token),
                           json=get_receipt_payload())
    logging.info("receipt: {}".format(response.json))
    assert "APP" in response.json['status']  # APP == APPROVED
    assert response.status_code == 200
    email_body = responses.calls[5].request.body.decode('utf-8')
    assert '"to": ["applicant_fake@gov.bc.ca"]' in email_body
    assert '"subject": "Select Review Date - Driving Prohibition 20-123456 Review"' in email_body
    assert 'Dear Developer Norris,' in email_body
    assert '"email": "success", "prohibition_number": "20123456"' in caplog.text


@responses.activate
def test_receipt_endpoint_sends_adp_select_review_date_with_order_number(token, client, monkeypatch):

    responses.add(responses.GET,
                  '{}/{}/status/{}'.format(Config.VIPS_API_ROOT_URL, "20123456", "20123456"),
                  json=vips_mock.status_applied_not_paid("ADP"), status=200)

    responses.add(responses.GET,
                  '{}/{}/application/{}'.format(
                      Config.VIPS_API_ROOT_URL, "bb71037c-f87b-0444-e054-00144ff95452", "20123456"),
                  json=vips_mock.application_get(), status=200)

    responses.add(responses.PATCH,
                  '{}/{}/payment/{}'.format(
                      Config.VIPS_API_ROOT_URL, "bb71037c-f87b-0444-e054-00144ff95452", "20123456"),
                  json=vips_mock.payment_patch_payload(), status=200)

    def mock_send_email(*args, **kwargs):
        assert "applicant_fake@gov.bc.ca" == args[0][0]
        assert "Dear Developer Norris," in args[3]
        assert "Select Review Date - Driving Prohibition 20-123456 Review" == args[1]
        assert "Order number: 1002581" in args[3]
        return True

    class MockRabbitMQ:

        def __init__(self, config):
            pass

        @staticmethod
        def publish(*args):
            return True

    monkeypatch.setattr(routes, "RabbitMQ", MockRabbitMQ)
    monkeypatch.setattr(common_email, "send_email", mock_send_email)

    response = client.post('/api_v2/receipt',
                           headers=get_oauth_auth_header(token),
                           json=get_receipt_payload())
    logging.info("receipt: {}".format(response.json))
    assert "APP" in response.json['status']  # APP == APPROVED
    assert response.status_code == 200


def get_basic_authentication_header(config) -> dict:
    username = config.PAYBC_CLIENT_ID
    password = config.PAYBC_CLIENT_SECRET
    credentials = base64.b64encode((username + ":" + password).encode('utf-8')).decode('utf-8')
    headers = dict({
        'Authorization': 'Basic {}'.format(credentials),
        'Content-Type': 'application/x-www-form-urlencoded'
    })
    logging.debug(headers)
    return headers


def get_search_payload(prohibition_number="20-123456", last_name="Gordon") -> dict:
    return dict({
        "invoice_number": prohibition_number,
        "check_value": last_name
    })


def get_receipt_payload(receipt_amount=200) -> dict:
    return dict({
        "receipt_number": "ABCD-1234",
        "receipt_date": "2020-10-12T15:17:33Z",
        "receipt_amount": receipt_amount,
        "payment_method": "credit card",
        "cardtype": "VISA",
        "transaction_id": "1002581",
        "invoices": [
            {
                "trx_number": "20123456",
                "amount_to_apply": receipt_amount
            }
        ]
    })


def get_oauth_auth_header(token) -> dict:
    return dict({"Authorization": "Bearer {}".format(token)})

