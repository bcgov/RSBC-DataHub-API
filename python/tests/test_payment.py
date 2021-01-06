import pytest
import pytz
import json
import datetime
import logging
import base64
from python.paybc_api.website.config import Config
import python.paybc_api.website.routes as routes
import python.paybc_api.website.app as app
import python.common.vips_api as vips
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
    logging.warning(headers)
    response = client.post('/oauth/token', data={'grant_type': 'client_credentials'}, headers=headers)
    token = response.json['access_token']
    logging.warning("token {}".format(token))
    return token


def test_get_token_endpoint(client, monkeypatch):
    headers = get_basic_authentication_header(Config)
    logging.warning(headers)
    response = client.post('/oauth/token', data={'grant_type': 'client_credentials'}, headers=headers)
    logging.warning(response.json)
    assert response.status_code == 200


def test_search_endpoint_requires_an_access_token(token, client, monkeypatch):
    response = client.get('/api_v2/search', query_string=get_search_payload())
    logging.warning("search: {}".format(response.json))
    assert response.status_code == 401


@pytest.mark.parametrize("prohibition_types", ['IRP', 'ADP', 'UL'])
def test_applicant_search_returns_error_if_entered_last_name_incorrect(prohibition_types, token, client, monkeypatch):

    def mock_status_get(*args, **kwargs):
        return status_get(True, prohibition_types, "2020-09-01", "Wrong-Name", True, True)

    monkeypatch.setattr(vips, "status_get", mock_status_get)

    response = client.get('/api_v2/search', query_string=get_search_payload(), headers=get_oauth_auth_header(token))
    logging.warning("search: {}".format(response.json))
    assert "The last name doesn't match a driving prohibition in the system." in response.json['error']
    assert response.status_code == 200


@pytest.mark.parametrize("prohibition_types", ['IRP', 'ADP', 'UL'])
def test_applicant_search_returns_error_if_already_paid(prohibition_types, token, client, monkeypatch):

    def mock_status_get(*args, **kwargs):
        return status_get(True, prohibition_types, "2020-09-01", "Gordon", True, True)

    monkeypatch.setattr(vips, "status_get", mock_status_get)

    response = client.get('/api_v2/search', query_string=get_search_payload(), headers=get_oauth_auth_header(token))
    logging.warning("search: {}".format(response.json))
    assert "The application review fee has already been paid." in response.json['error']
    assert response.status_code == 200


@pytest.mark.parametrize("prohibition_types", ['IRP', 'ADP', 'UL'])
def test_applicant_search_returns_error_if_not_found_in_vips(prohibition_types, token, client, monkeypatch):

    def mock_status_get(*args, **kwargs):
        return status_get(False, prohibition_types, "2020-09-01", "Gordon", True, True)

    monkeypatch.setattr(vips, "status_get", mock_status_get)

    response = client.get('/api_v2/search', query_string=get_search_payload(), headers=get_oauth_auth_header(token))
    logging.warning("search: {}".format(response.json))
    assert "The driving prohibition isn't in the system." in response.json['error']
    assert response.status_code == 200


@pytest.mark.parametrize("prohibition_type", ['IRP', 'ADP'])
def test_applicant_search_returns_error_if_irp_or_adp_older_than_7_days(prohibition_type, token, client, monkeypatch):
    iso_format = "%Y-%m-%d"
    tz = pytz.timezone('America/Vancouver')
    date_served = (datetime.datetime.now(tz) - datetime.timedelta(days=8)).strftime(iso_format)

    def mock_status_get(*args, **kwargs):
        return status_get(True, prohibition_type, date_served, "Gordon", False, True)

    monkeypatch.setattr(vips, "status_get", mock_status_get)

    response = client.get('/api_v2/search', query_string=get_search_payload(), headers=get_oauth_auth_header(token))
    logging.warning("search: {}".format(response.json))
    assert "The Notice of Prohibition was issued more than 7 days ago." in response.json['error']
    assert response.status_code == 200


def test_applicant_search_successful_if_a_ul_review_older_than_7_days(token, client, monkeypatch):
    iso_format = "%Y-%m-%d"
    tz = pytz.timezone('America/Vancouver')
    date_served = (datetime.datetime.now(tz) - datetime.timedelta(days=8)).strftime(iso_format)

    def mock_status_get(*args, **kwargs):
        return status_get(True, "UL", date_served, "Gordon", False, True)

    monkeypatch.setattr(vips, "status_get", mock_status_get)

    response = client.get('/api_v2/search', query_string=get_search_payload(), headers=get_oauth_auth_header(token))
    logging.warning("search: {}".format(response.json))
    assert "error" not in response.json
    assert "https://localhost/api_v2/invoice/20123456" in response.json['items'][0]['selected_invoice']['$ref']
    assert response.status_code == 200


@pytest.mark.parametrize("prohibition_number", ['20123456', '20123457'])
def test_successful_search_response_includes_url_to_invoice_endpoint(prohibition_number, token, client, monkeypatch):
    iso_format = "%Y-%m-%d"
    tz = pytz.timezone('America/Vancouver')
    date_served = (datetime.datetime.now(tz) - datetime.timedelta(days=6)).strftime(iso_format)

    def mock_status_get(*args, **kwargs):
        return status_get(True, "IRP", date_served, "Gordon", False, True)

    monkeypatch.setattr(vips, "status_get", mock_status_get)

    response = client.get('/api_v2/search',
                          query_string=get_search_payload(prohibition_number),
                          headers=get_oauth_auth_header(token))
    logging.warning("search: {}".format(response.json))
    endpoint = "https://localhost/api_v2/invoice/{}".format(prohibition_number)
    assert "error" not in response.json
    assert endpoint in response.json['items'][0]['selected_invoice']['$ref']
    assert response.status_code == 200


def test_invoice_endpoint_requires_an_access_token(token, client, monkeypatch):
    response = client.get('/api_v2/invoice/20123456')
    logging.warning("invoice: {}".format(response.json))
    assert response.status_code == 401


@pytest.mark.parametrize("prohibition_types", ['IRP', 'ADP', 'UL'])
def test_applicant_invoice_returns_error_if_already_paid(prohibition_types, token, client, monkeypatch):

    def mock_status_get(*args, **kwargs):
        return status_get(True, prohibition_types, "2020-09-01", "Gordon", True, True)

    monkeypatch.setattr(vips, "status_get", mock_status_get)

    response = client.get('/api_v2/invoice/20123456', headers=get_oauth_auth_header(token))
    logging.warning("invoice: {}".format(response.json))
    assert "The application review fee has already been paid." in response.json['error']
    assert response.status_code == 200


@pytest.mark.parametrize("prohibition_types", ['IRP', 'ADP', 'UL'])
def test_applicant_invoice_returns_error_if_not_found_in_vips(prohibition_types, token, client, monkeypatch):

    def mock_status_get(*args, **kwargs):
        return status_get(False, prohibition_types, "2020-09-01", "Gordon", True, True)

    monkeypatch.setattr(vips, "status_get", mock_status_get)

    response = client.get('/api_v2/invoice/20123456', headers=get_oauth_auth_header(token))
    logging.warning("invoice: {}".format(response.json))
    assert "The driving prohibition isn't in the system." in response.json['error']
    assert response.status_code == 200


@pytest.mark.parametrize("prohibition_type", ['IRP', 'ADP'])
def test_applicant_invoice_returns_error_if_irp_or_adp_older_than_7_days(prohibition_type, token, client, monkeypatch):
    iso_format = "%Y-%m-%d"
    tz = pytz.timezone('America/Vancouver')
    date_served = (datetime.datetime.now(tz) - datetime.timedelta(days=8)).strftime(iso_format)

    def mock_status_get(*args, **kwargs):
        return status_get(True, prohibition_type, date_served, "Gordon", False, True)

    monkeypatch.setattr(vips, "status_get", mock_status_get)

    response = client.get('/api_v2/invoice/20123456', headers=get_oauth_auth_header(token))
    logging.warning("invoice: {}".format(response.json))
    assert "The Notice of Prohibition was issued more than 7 days ago." in response.json['error']
    assert response.status_code == 200


def test_applicant_invoice_successful_if_a_ul_review_older_than_7_days(token, client, monkeypatch):
    iso_format = "%Y-%m-%d"
    tz = pytz.timezone('America/Vancouver')
    date_served = (datetime.datetime.now(tz) - datetime.timedelta(days=8)).strftime(iso_format)

    def mock_status_get(*args, **kwargs):
        return status_get(True, "UL", date_served, "Gordon", False, True)

    def mock_application_get(*args, **kwargs):
        return application_get()

    monkeypatch.setattr(vips, "status_get", mock_status_get)
    monkeypatch.setattr(vips, "application_get", mock_application_get)

    response = client.get('/api_v2/invoice/20123456', headers=get_oauth_auth_header(token))
    logging.warning("invoice: {}".format(response.json))
    assert "error" not in response.json
    assert "20123456" == response.json["invoice_number"]
    assert "10008" == response.json["pbc_ref_number"]
    assert 50 == response.json["total"]
    assert 50 == response.json["amount_due"]
    assert 0 == response.json["party_number"]
    assert response.status_code == 200


@pytest.mark.parametrize("prohibition_type", ['IRP', 'ADP'])
def test_successful_invoice_response_includes_url_to_invoice_endpoint(prohibition_type, token, client, monkeypatch):
    iso_format = "%Y-%m-%d"
    tz = pytz.timezone('America/Vancouver')
    date_served = (datetime.datetime.now(tz) - datetime.timedelta(days=6)).strftime(iso_format)

    def mock_status_get(*args, **kwargs):
        return status_get(True, prohibition_type, date_served, "Gordon", False, True)

    def mock_application_get(*args, **kwargs):
        return application_get("ORAL")

    monkeypatch.setattr(vips, "status_get", mock_status_get)
    monkeypatch.setattr(vips, "application_get", mock_application_get)

    response = client.get('/api_v2/invoice/20123456', headers=get_oauth_auth_header(token))
    logging.warning("invoice: {}".format(response.json))
    assert "error" not in response.json
    assert "20123456" == response.json["invoice_number"]
    assert "10008" == response.json["pbc_ref_number"]
    assert 200 == response.json["total"]
    assert 200 == response.json["amount_due"]
    assert 0 == response.json["party_number"]
    assert response.status_code == 200


@pytest.mark.parametrize("presentation_type", [['ORAL', 200],  ['WRIT', 100]])
def test_invoice_amount_is_determined_by_review_presentation_type(presentation_type, token, client, monkeypatch):
    iso_format = "%Y-%m-%d"
    tz = pytz.timezone('America/Vancouver')
    date_served = (datetime.datetime.now(tz) - datetime.timedelta(days=6)).strftime(iso_format)

    def mock_status_get(*args, **kwargs):
        return status_get(True, "IRP", date_served, "Gordon", False, True)

    def mock_application_get(*args, **kwargs):
        return application_get(presentation_type[0])

    monkeypatch.setattr(vips, "status_get", mock_status_get)
    monkeypatch.setattr(vips, "application_get", mock_application_get)

    response = client.get('/api_v2/invoice/20123456', headers=get_oauth_auth_header(token))
    logging.warning("invoice: {}".format(response.json))
    assert "error" not in response.json
    assert "20123456" == response.json["invoice_number"]
    assert "10008" == response.json["pbc_ref_number"]
    assert presentation_type[1] == response.json["total"]
    assert presentation_type[1] == response.json["amount_due"]
    assert 0 == response.json["party_number"]
    assert response.status_code == 200


def test_receipt_endpoint_requires_an_access_token(token, client, monkeypatch):
    response = client.post('/api_v2/receipt')
    logging.warning("receipt: {}".format(response.json))
    assert response.status_code == 401


@pytest.mark.parametrize("prohibition_types", ['IRP', 'ADP', 'UL'])
def test_receipt_endpoint_returns_error_if_prohibition_not_found(prohibition_types, token, client, monkeypatch):

    def mock_status_get(*args, **kwargs):
        return status_get(False, prohibition_types, "2020-09-01", "Gordon", True, False)

    class MockRabbitMQ:

        def __init__(self, config):
            pass

    monkeypatch.setattr(vips, "status_get", mock_status_get)
    monkeypatch.setattr(routes, "RabbitMQ", MockRabbitMQ)

    response = client.post('/api_v2/receipt',
                           headers=get_oauth_auth_header(token),
                           json=get_receipt_payload())
    logging.warning("receipt: {}".format(response.json))
    assert "INCMP" in response.json['status']  # INCMP == INCOMPLETE
    assert response.status_code == 400


@pytest.mark.parametrize("prohibition_types", ['IRP', 'ADP', 'UL'])
def test_receipt_endpoint_returns_error_if_application_not_saved(prohibition_types, token, client, monkeypatch):

    def mock_status_get(*args, **kwargs):
        return status_get(True, prohibition_types, "2020-09-01", "Gordon", False, False)

    class MockRabbitMQ:

        def __init__(self, config):
            pass

    monkeypatch.setattr(vips, "status_get", mock_status_get)
    monkeypatch.setattr(routes, "RabbitMQ", MockRabbitMQ)

    response = client.post('/api_v2/receipt',
                           headers=get_oauth_auth_header(token),
                           json=get_receipt_payload())
    logging.warning("receipt: {}".format(response.json))
    assert "INCMP" in response.json['status']  # INCMP == INCOMPLETE
    assert response.status_code == 400


@pytest.mark.parametrize("prohibition_types", ['IRP', 'ADP', 'UL'])
def test_receipt_endpoint_returns_error_if_application_data_not_returned(prohibition_types, token, client, monkeypatch):

    def mock_status_get(*args, **kwargs):
        return status_get(True, prohibition_types, "2020-09-01", "Gordon", False, False)

    def mock_application_get(*args, **kwargs):
        return False, dict()

    class MockRabbitMQ:

        def __init__(self, config):
            pass

    monkeypatch.setattr(vips, "status_get", mock_status_get)
    monkeypatch.setattr(routes, "RabbitMQ", MockRabbitMQ)
    monkeypatch.setattr(vips, "application_get", mock_application_get)

    response = client.post('/api_v2/receipt',
                           headers=get_oauth_auth_header(token),
                           json=get_receipt_payload())
    logging.warning("receipt: {}".format(response.json))
    assert "INCMP" in response.json['status']  # INCMP == INCOMPLETE
    assert response.status_code == 400


@pytest.mark.parametrize("prohibition_types", ['IRP', 'ADP', 'UL'])
def test_receipt_endpoint_returns_success_if_prohibition_already_paid(prohibition_types, token, client, monkeypatch):
    """
    In the event that VIPS status says the application for review has already been paid, return a successful
    response to PayBC.  If we don't send a successful response, PayBC will try again and again indefinitely.
    PayBC likely didn't receive the initial successful response, so is trying again.
    """

    def mock_status_get(*args, **kwargs):
        return status_get(True, prohibition_types, "2020-09-01", "Gordon", True, True)

    def mock_application_get(*args, **kwargs):
        return application_get()

    def mock_send_email(*args, **kwargs):
        return True

    class MockRabbitMQ:

        def __init__(self, config):
            pass

        @staticmethod
        def publish(*args):
            assert "DF.Hold" in args[0]
            return True

    monkeypatch.setattr(routes, "RabbitMQ", MockRabbitMQ)
    monkeypatch.setattr(vips, "status_get", mock_status_get)
    monkeypatch.setattr(vips, "application_get", mock_application_get)
    monkeypatch.setattr(common_email, "send_email", mock_send_email)

    response = client.post('/api_v2/receipt',
                           headers=get_oauth_auth_header(token),
                           json=get_receipt_payload())
    logging.warning("receipt: {}".format(response.json))
    assert "APP" in response.json['status']  # APP == APPROVED
    assert response.status_code == 200


@pytest.mark.parametrize("prohibition_types", ['IRP', 'ADP', 'UL'])
def test_receipt_endpoint_returns_success_and_sends_schedule_email(prohibition_types, token, client, monkeypatch):

    def mock_status_get(*args, **kwargs):
        return status_get(True, prohibition_types, "2020-09-01", "Gordon", False, True)

    def mock_application_get(*args, **kwargs):
        return application_get()

    def mock_patch_payment(*args, **kwargs):
        return True, dict({})

    def mock_send_email(*args, **kwargs):
        assert "applicant@gov.bc.ca" == args[0][0]
        assert "Dear Charlie Brown," in args[3]
        assert "Select Review Date - Driving Prohibition 21-123456 Review" == args[1]
        return True

    class MockRabbitMQ:

        def __init__(self, config):
            pass

        @staticmethod
        def publish(*args):
            message = args[1].decode("utf-8")
            assert "Charlie Brown" in message
            assert "DF.Hold" in args[0]
            return True

    monkeypatch.setattr(routes, "RabbitMQ", MockRabbitMQ)
    monkeypatch.setattr(vips, "status_get", mock_status_get)
    monkeypatch.setattr(vips, "application_get", mock_application_get)
    monkeypatch.setattr(vips, "payment_patch", mock_patch_payment)
    monkeypatch.setattr(common_email, "send_email", mock_send_email)

    response = client.post('/api_v2/receipt',
                           headers=get_oauth_auth_header(token),
                           json=get_receipt_payload())
    logging.warning("receipt: {}".format(response.json))
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
        "invoices": [
            {
                "trx_number": "21123456",
                "amount_to_apply": receipt_amount
            }
        ]
    })


def get_oauth_auth_header(token) -> dict:
    return dict({"Authorization": "Bearer {}".format(token)})


def status_get(is_success, prohibition_type, date_served, last_name, is_paid, application_saved):
    if is_success:
        status = {
            "noticeTypeCd": prohibition_type,
            "noticeServedDt": date_served + " 00:00:00 -07:00",
            "reviewFormSubmittedYn": "N",
            "reviewCreatedYn": "N",
            "originalCause": "N/A",
            "surnameNm": last_name,
            "driverLicenceSeizedYn": "Y",
            "disclosure": []
        }
        if is_paid:
            status['receiptNumberTxt'] = "ABC"
        if application_saved:
            status['applicationId'] = "ABC-ABC-ABC"
        return True, {
                "resp": "success",
                "data": {
                    "status": status
                }
            }
    else:
        return True, {
                  "resp": "fail",
                  "error": {
                    "message": "Record not found",
                    "httpStatus": 404
                  }
               }


def application_get(presentation_type="ORAL"):
    return True, {
          "data": {
                "applicationInfo": {
                      "email": "applicant@gov.bc.ca",
                      "firstGivenNm": "Charlie",
                      "manualEntryYN": "N",
                      "noticeSubjectCd": "string",
                      "noticeTypeCd": "string",
                      "phoneNo": "string",
                      "presentationTypeCd": presentation_type,
                      "prohibitionNoticeNo": "string",
                      "reviewApplnTypeCd": "string",
                      "reviewRoleTypeCd": "string",
                      "secondGivenNm": "string",
                      "surnameNm": "Brown"
                }
          },
          "resp": "success"
          }
