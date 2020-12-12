import pytest
import pytz
import datetime
import logging
import base64
import python.common.helper as helper
import python.common.middleware as middleware
import python.paybc_api.business as business
from python.paybc_api.website.config import Config
import python.paybc_api.website.app as app
import python.common.vips_api as vips


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


def get_oauth_auth_header(token) -> dict:
    return dict({"Authorization": "Bearer {}".format(token)})


test_show_method_data = [
    # Type, Application  Error
    ('IRP', True,        None),
    ('IRP', False,       "You must submit an application before you can pay."),

]


@pytest.mark.parametrize("prohibition_type, application_created, error", test_show_method_data)
def test_pay_bc_generate_invoice_method(prohibition_type, application_created, error, monkeypatch):
    is_in_vips = True
    prohibition_type = "ADP"
    today_is = "2020-09-14"
    last_name = "Gordon"
    date_served = "2020-09-10"
    is_paid = False

    def mock_status_get(*args, **kwargs):
        print('inside mock_status_get()')
        return status_get(is_in_vips, prohibition_type, date_served, last_name, is_paid, application_created)

    def mock_application_get(*args, **kwargs):
        print('inside mock_application_get()')
        return application_get()

    def mock_datetime_now(**args):
        args['today_date'] = helper.localize_timezone(datetime.datetime.strptime(today_is, "%Y-%m-%d"))
        print('inside mock_datetime_now: {}'.format(args.get('today_date')))
        return True, args

    monkeypatch.setattr(middleware, "determine_current_datetime", mock_datetime_now)
    monkeypatch.setattr(vips, "status_get", mock_status_get)
    monkeypatch.setattr(vips, "application_get", mock_application_get)

    results = helper.middle_logic(business.generate_invoice(),
                                  prohibition_number="20-123456",
                                  config=Config)

    print(results.get('error_string'))
    if error is None:
        assert "error_string" not in results
    else:
        assert "error_string" in results
        assert results.get('error_string') == error





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


def application_get():
    return True, {
          "data": {
                "applicationInfo": {
                      "email": "string",
                      "firstGivenNm": "string",
                      "manualEntryYN": "N",
                      "noticeSubjectCd": "string",
                      "noticeTypeCd": "string",
                      "phoneNo": "string",
                      "presentationTypeCd": "string",
                      "prohibitionNoticeNo": "string",
                      "reviewApplnTypeCd": "string",
                      "reviewRoleTypeCd": "string",
                      "secondGivenNm": "string",
                      "surnameNm": "string"
                }
          },
          "resp": "success"
          }
