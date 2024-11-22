import python.common.tests.vips_mock as vips_mock
import datetime
import responses
import pytz
import python.common.helper as helper
import python.form_handler.business as business
from python.form_handler.config import Config as BaseConfig
import python.common.vips_api as vips
import python.common.common_email_services as common_email_services


@responses.activate
def test_applicant_sent_email_confirming_evidence_received(monkeypatch):
    tz = pytz.timezone('America/Vancouver')
    review_start_date = vips.vips_datetime(datetime.datetime.now(tz) + datetime.timedelta(days=1))

    responses.add(responses.GET,
                  '{}/{}/status/{}'.format(Config.VIPS_API_ROOT_URL, "20123456", "20123456"),
                  json=vips_mock.status_applied_paid_and_scheduled("IRP", review_start_date),
                  status=200, match_querystring=True)

    responses.add(responses.GET,
                  '{}/{}/application/{}'.format(
                      Config.VIPS_API_ROOT_URL, "bb71037c-f87b-0444-e054-00144ff95452", "20123456"),
                  json=vips_mock.application_get(),
                  status=200)

    def mock_send_email(*args, **kwargs):
        print('inside mock_send_email()')
        assert "me@gov.bc.ca" in args[0]
        print("Subject: {}".format(args[1]))
        assert "Documents Received - Driving Prohibition 20-123456 Review" in args[3]
        assert "we received the evidence that will be considered for your review." in args[3]
        assert "http://link-to-evidence-form" in args[3]
        return True

    monkeypatch.setattr(common_email_services, "send_email", mock_send_email)

    message_dict = helper.load_json_into_dict('python/common/tests/sample_data/form/document_submission.json')

    results = helper.middle_logic(helper.get_listeners(business.process_incoming_form(), message_dict['event_type']),
                                  message=message_dict,
                                  config=Config,
                                  writer=None)

    if "error_string" in results:
        print(results.get('error_string'))
    assert 'error_string' not in results


class Config(BaseConfig):
    LINK_TO_PAYBC = 'http://link-to-paybc'
    LINK_TO_SCHEDULE_FORM = 'http://link-to-schedule-form'
    LINK_TO_EVIDENCE_FORM = 'http://link-to-evidence-form'
    LINK_TO_APPLICATION_FORM = 'http://link-to-application-form'
    LINK_TO_ICBC ='http://link-to-icbc'
    LINK_TO_SERVICE_BC = 'http://link-to-service-bc'