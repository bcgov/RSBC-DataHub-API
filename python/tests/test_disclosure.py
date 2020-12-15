import pytest
import datetime
import python.common.helper as helper
import python.common.middleware as middleware
import python.form_handler.business as business
from python.form_handler.config import Config as BaseConfig
import python.common.vips_api as vips
import python.common.common_email_services as common_email_services
from python.common.rabbitmq import RabbitMQ


class Config(BaseConfig):
    VIPS_API_ROOT_URL = 'https://vips_url'


def test_disclosure_that_has_not_reached_the_hold_until_datetime_is_placed_back_on_hold(monkeypatch):
    message_dict = helper.load_json_into_dict('python/tests/sample_data/form/disclosure_payload.json')
    message_dict['hold_until'] = (datetime.datetime.now() + datetime.timedelta(hours=1)).isoformat()

    def mock_publish(queue_name: str, payload: bytes):
        assert queue_name == "DF.hold"

    monkeypatch.setattr(Config, "ENCRYPT_KEY", "something-secret")
    monkeypatch.setattr(RabbitMQ, "publish", mock_publish)

    results = helper.middle_logic(helper.get_listeners(business.process_incoming_form(), message_dict['event_type']),
                                  message=message_dict,
                                  config=Config,
                                  writer=RabbitMQ)


def test_when_an_applicants_review_has_concluded_the_disclosure_event_is_deleted(monkeypatch):
    message_dict = helper.load_json_into_dict('python/tests/sample_data/form/disclosure_payload.json')
    message_dict['hold_until'] = (datetime.datetime.now() - datetime.timedelta(hours=1)).isoformat()

    def mock_status_get(*args, **kwargs):
        review_start_date = (datetime.date.today() - datetime.timedelta(days=1)).strftime("%Y-%m-%d")
        return status_gets(True, "IRP", review_start_date, "No")

    def mock_any_disclosure(*args, **kwargs):
        # We should never call this method
        assert False

    monkeypatch.setattr(vips, "status_get", mock_status_get)
    monkeypatch.setattr(middleware, "is_any_unsent_disclosure", mock_any_disclosure)

    results = helper.middle_logic(helper.get_listeners(business.process_incoming_form(), message_dict['event_type']),
                                  message=message_dict,
                                  config=Config,
                                  writer=RabbitMQ)


def test_if_no_disclosure_add_back_to_hold_queue(monkeypatch):
    message_dict = helper.load_json_into_dict('python/tests/sample_data/form/disclosure_payload.json')
    message_dict['hold_until'] = (datetime.datetime.now() - datetime.timedelta(hours=1)).isoformat()

    def mock_status_get(*args, **kwargs):
        review_start_date = (datetime.date.today() - datetime.timedelta(days=1)).strftime("%Y-%m-%d")
        return status_gets(True, "IRP", review_start_date, "No")

    def mock_publish(queue_name: str, payload: bytes):
        assert queue_name == "DF.hold"

    monkeypatch.setattr(Config, "ENCRYPT_KEY", "something-secret")
    monkeypatch.setattr(RabbitMQ, "publish", mock_publish)
    monkeypatch.setattr(vips, "status_get", mock_status_get)

    results = helper.middle_logic(helper.get_listeners(business.process_incoming_form(), message_dict['event_type']),
                                  message=message_dict,
                                  config=Config,
                                  writer=RabbitMQ)


def test_disclosure_documents_marked_sent_are_not_sent_again(monkeypatch):
    message_dict = helper.load_json_into_dict('python/tests/sample_data/form/disclosure_payload.json')
    message_dict['hold_until'] = (datetime.datetime.now() - datetime.timedelta(hours=1)).isoformat()

    def mock_status_get(*args, **kwargs):
        review_start_date = (datetime.date.today() - datetime.timedelta(days=1)).strftime("%Y-%m-%d")
        return status_gets(True, "IRP", review_start_date, "none-unsent")

    def mock_publish(queue_name: str, payload: bytes):
        assert queue_name == "DF.hold"

    monkeypatch.setattr(Config, "ENCRYPT_KEY", "something-secret")
    monkeypatch.setattr(RabbitMQ, "publish", mock_publish)
    monkeypatch.setattr(vips, "status_get", mock_status_get)

    results = helper.middle_logic(helper.get_listeners(business.process_incoming_form(), message_dict['event_type']),
                                  message=message_dict,
                                  config=Config,
                                  writer=RabbitMQ)


@pytest.mark.parametrize("document_count", ['1', '2'])
def test_disclosure_documents_are_emailed_to_applicant(document_count, monkeypatch):
    message_dict = helper.load_json_into_dict('python/tests/sample_data/form/disclosure_payload.json')
    message_dict['hold_until'] = (datetime.datetime.now() - datetime.timedelta(hours=1)).isoformat()

    def mock_status_get(*args, **kwargs):
        review_start_date = (datetime.date.today() + datetime.timedelta(days=2)).strftime("%Y-%m-%d")
        return status_gets(True, "IRP", review_start_date, document_count)

    def mock_publish(queue_name: str, payload: bytes):
        assert queue_name == "DF.hold"

    def mock_send_email(*args, **kwargs):
        print('inside mock_send_email()')
        assert "me@gov.bc.ca" in args[0]
        assert "Disclosure Documents Attached - Driving Prohibition 21258852 Review" in args[1]
        assert int(document_count) == len(args[4])
        return True

    def mock_disclosure_get(*args):
        print("inside mock_disclosure_get()")
        data = dict({
                "resp": "success",
                "data": {
                    "document": {
                        "document": "base64_string_of_encoded_document",
                        "mimeType": "application/pdf"
                    }
                }
            })
        return True, data

    def mock_patch(*args):
        return True, dict({})

    monkeypatch.setattr(Config, "ENCRYPT_KEY", "something-secret")
    monkeypatch.setattr(RabbitMQ, "publish", mock_publish)
    monkeypatch.setattr(vips, "status_get", mock_status_get)
    monkeypatch.setattr(vips, "patch", mock_patch)
    monkeypatch.setattr(common_email_services, "send_email", mock_send_email)
    monkeypatch.setattr(vips, "disclosure_get", mock_disclosure_get)

    results = helper.middle_logic(helper.get_listeners(business.process_incoming_form(), message_dict['event_type']),
                                  message=message_dict,
                                  config=Config,
                                  writer=RabbitMQ)


@pytest.mark.parametrize("document_count", ['1', '2'])
def test_adp_disclosure_includes_an_additional_static_document(document_count, monkeypatch):
    message_dict = helper.load_json_into_dict('python/tests/sample_data/form/disclosure_payload.json')
    message_dict['hold_until'] = (datetime.datetime.now() - datetime.timedelta(hours=1)).isoformat()

    def mock_status_get(*args, **kwargs):
        review_start_date = (datetime.date.today() + datetime.timedelta(days=2)).strftime("%Y-%m-%d")
        return status_gets(True, "ADP", review_start_date, document_count)

    def mock_publish(queue_name: str, payload: bytes):
        assert queue_name == "DF.hold"

    def mock_send_email(*args, **kwargs):
        print('inside mock_send_email()')
        assert "me@gov.bc.ca" in args[0]
        assert "Disclosure Documents Attached - Driving Prohibition 21258852 Review" in args[1]
        assert int(document_count) + 1 == len(args[4])
        return True

    def mock_disclosure_get(*args):
        print("inside mock_disclosure_get()")
        data = dict({
                "resp": "success",
                "data": {
                    "document": {
                        "document": "base64_string_of_encoded_document",
                        "mimeType": "application/pdf"
                    }
                }
            })
        return True, data

    def mock_patch(*args):
        return True, dict({})

    monkeypatch.setattr(Config, "ENCRYPT_KEY", "something-secret")
    monkeypatch.setattr(RabbitMQ, "publish", mock_publish)
    monkeypatch.setattr(vips, "status_get", mock_status_get)
    monkeypatch.setattr(vips, "patch", mock_patch)
    monkeypatch.setattr(common_email_services, "send_email", mock_send_email)
    monkeypatch.setattr(vips, "disclosure_get", mock_disclosure_get)

    results = helper.middle_logic(helper.get_listeners(business.process_incoming_form(), message_dict['event_type']),
                                  message=message_dict,
                                  config=Config,
                                  writer=RabbitMQ)


def status_gets(is_success, prohibition_type, review_start_date, disclosure):
    data = {
            "resp": "success",
            "data": {
                "status": {
                    "noticeTypeCd": prohibition_type,
                    "noticeServedDt": "2020-09-10 00:00:00 -08:00",
                    "reviewStartDtm": review_start_date + ' 09:30:00 -07:00',
                    "reviewFormSubmittedYn": "N",
                    "reviewCreatedYn": "Y",
                    "originalCause": "IRP7",
                    "surnameNm": "Gordon",
                    "driverLicenceSeizedYn": "Y",
                    "receiptNumberTxt": "AAABBB123",
                    "applicationId": 'GUID-GUID-GUID-GUID',
                }
            }
        }
    if disclosure == "No":
        data['data']['status']['disclosure'] = []
    elif disclosure == "2":
        data['data']['status']['disclosure'] = [
            {
                "documentId": "1491"
            },
            {
                "documentId": "1490"
            }
        ]
    elif disclosure == "1":
        data['data']['status']['disclosure'] = [
            {
                "documentId": "1491",
                "disclosedDtm": "some-date",
            },
            {
                "documentId": "1490"
            }
        ]
    elif disclosure == "none-unsent":
        data['data']['status']['disclosure'] = [
            {
                "documentId": "1491",
                "disclosedDtm": "some-date",
            },
            {
                "documentId": "1490",
                "disclosedDtm": "some-date",
            }
        ]
    return is_success, data
