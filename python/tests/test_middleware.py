import pytz
import logging
import os
from python.form_handler.config import Config
import python.common.vips_api as vips
from datetime import datetime
import python.common.middleware as middleware
from python.common.helper import load_json_into_dict, load_xml_to_string, localize_timezone
import pytest
import flask
import json
from python.ingestor.routes import application

os.environ['TZ'] = 'UTC'

date_served_data = [
    ('IRP', "2020-09-10", "2020-09-11", True),
    ('IRP', "2020-09-10", "2020-09-16", True),
    ('IRP', "2020-09-10", "2020-09-16", True),
    ('IRP', "2020-09-10", "2020-09-17", True),
    ('IRP', "2020-09-10", "2020-09-18", False),
    ('IRP', "2020-09-10", "2020-09-19", False),

    ('UL',  "2020-09-10", "2020-09-11", True),
    ('UL',  "2020-09-10", "2020-09-16", True),
    ('UL',  "2020-09-10", "2020-09-17", True),
    ('UL',  "2020-09-10", "2020-09-18", True),
    ('UL',  "2020-09-10", "2020-09-19", True),

    ('ADP', "2020-09-10", "2020-09-10", True),
    ('ADP', "2020-09-10", "2020-09-11", True),
    ('ADP', "2020-09-10", "2020-09-16", True),
    ('ADP', "2020-09-10", "2020-09-17", True),
    ('ADP', "2020-09-10", "2020-09-18", False),
    ('ADP', "2020-09-10", "2020-09-19", False),
]


@pytest.mark.parametrize("prohibition_type, notice_serve_date, today_is, expected", date_served_data)
def test_date_served_not_older_than_one_week_method(prohibition_type, notice_serve_date, today_is, expected):
    today_unaware = datetime.strptime(today_is + " 00:00:00", "%Y-%m-%d %H:%M:%S")
    today_date = localize_timezone(today_unaware)
    vips_data = dict()
    vips_data['noticeTypeCd'] = prohibition_type
    vips_data['noticeServedDt'] = notice_serve_date + " 00:00:00 -08:00"
    (result, args) = middleware.is_applicant_within_window_to_apply(vips_data=vips_data, today_date=today_date)
    assert result is expected


last_name_match_data = [
    ('Jones', 'Jones', True),
    ('Jones', 'JONES', True),
    ('Coté', 'Cote', True),  # note the accent on the "e"
    ('Jones', 'Other', False)
]


@pytest.mark.parametrize("user_entered_last_name, last_name_from_vips, expected", last_name_match_data)
def test_user_submitted_last_name_matches_vips_method(user_entered_last_name, last_name_from_vips, expected):
    vips_status = load_json_into_dict("python/tests/sample_data/vips/vips_query_200.json")
    vips_status['data']['status']['surnameNm'] = last_name_from_vips
    result, args = middleware.user_submitted_last_name_matches_vips(
        driver_last_name=user_entered_last_name,
        vips_data=vips_status['data']['status'])
    assert result is expected


served_recently_data = [
    ["2020-09-11", "2020-09-11", True],
    ["2020-09-11", "2020-09-10", True],
    ["2020-09-11", "2020-09-09", True],
    ["2020-09-11", "2020-09-08", True],
    ["2020-09-11", "2020-09-07", True],
    ["2020-09-11", "2020-09-06", True],
    ["2020-09-11", "2020-09-05", True],
    ["2020-09-11", "2020-09-04", False],
    ["2020-09-11", "2020-09-03", False],
]


@pytest.mark.parametrize("today_is, date_served, expected", served_recently_data)
def test_prohibition_served_within_past_week_method(today_is, date_served, expected):
    today_unaware = datetime.strptime(today_is, "%Y-%m-%d")
    today_date = localize_timezone(today_unaware)
    result, args = middleware.prohibition_served_within_past_week(today_date=today_date, date_of_service=date_served,
                                                                  config=Config)
    assert result is expected


exists_in_vips_data = [
    ("vips_query_404.json", False),
    ("vips_query_200.json", True)
]


@pytest.mark.parametrize("response_from_vips, expected", exists_in_vips_data)
def test_prohibition_exists_in_vips_method(response_from_vips, expected):
    vips_status = load_json_into_dict("python/tests/sample_data/vips/{}".format(response_from_vips))
    result, data = middleware.prohibition_exists_in_vips(vips_status=vips_status)
    assert result is expected
    if result:
        assert 'vips_data' in data


licence_seized = [
    ("UL", "Y", True),
    ("UL", "N", True),
    ("IRP", "Y", True),
    ("IRP", "N", False),
    ("ADP", "Y", True),
    ("ADP", "N", False)
]


@pytest.mark.parametrize("prohibition_type, test_condition, expected", licence_seized)
def test_has_drivers_licence_been_seized_method(prohibition_type, test_condition, expected):
    sample_data = load_json_into_dict('python/tests/sample_data/form/irp_form_submission.json')
    response_from_api = load_json_into_dict('python/tests/sample_data/vips/vips_query_200.json')
    response_from_api['data']['status']['driverLicenceSeizedYn'] = test_condition
    response_from_api['data']['status']['noticeTypeCd'] = prohibition_type
    vips_data = response_from_api['data']['status']
    result, args = middleware.has_drivers_licence_been_seized(message=sample_data, vips_data=vips_data)
    assert result is expected


vips_date_strings = [
    ("20-JUN-2017", "2017-06-20 00:00:00 -07:00", False),
    ("2020-09-15T16:59:04Z", "2020-09-15 16:59:04 +00:00", True),
]


@pytest.mark.parametrize("pay_bc_date, expected, result", vips_date_strings)
def test_pay_bc_date_transformation(pay_bc_date, expected, result):
    payload = dict()
    payload['receipt_date'] = pay_bc_date
    is_success, args = middleware.transform_receipt_date_from_pay_bc_format(payload=payload)
    date_object = args.get('receipt_date')
    if is_success:
        actual = vips.vips_datetime(date_object)
        assert actual == expected
        assert is_success == result
    assert is_success == result
    

hearing_request_types = [
    (None, "WRIT"),
    ('', "WRIT"),
    ("oral", "ORAL"),
    ("written", "WRIT")
]


@pytest.mark.parametrize("hearing_type, expected", hearing_request_types)
def test_transform_hearing_request_types(hearing_type, expected):
    response, args = middleware.transform_hearing_request_type(hearing_request_type=hearing_type)
    assert response is True
    assert args['presentation_type'] == expected
    

def test_null_json_values_convert_to_none_types():
    # check that json attributes with null values are converted to None type
    sample_data = load_json_into_dict('python/tests/sample_data/form/irp_form_submission.json')
    assert sample_data['prohibition_review']['form']['review-information']['ul-grounds'] is None


applicant_role_types = [
    ("driver", "APPNT", True),
    ("lawyer", "LWYR", True),
    ("advocate", "AUTHPERS", True),
    ("", None, False)
]


@pytest.mark.parametrize("role_type, expected, is_success", applicant_role_types)
def test_transform_applicant_role_types(role_type, expected, is_success):
    response, args = middleware.transform_applicant_role_type(applicant_role_raw=role_type)
    assert response is is_success
    assert args['applicant_role'] == expected


def test_create_correlation_id():
    response, args = middleware.create_correlation_id()
    assert 'correlation_id' in args
    assert len(args['correlation_id']) == 36


prohibition_numbers = [
    ("1234", False),
    ("21900055", True),
    ("00900055", True),
    ("30900055", True),
    ("2100055", False),
    ("21-900055", False),
    ("30900055X", False),
]


@pytest.mark.parametrize("number_under_test, is_valid", prohibition_numbers)
def test_validate_prohibition_number(number_under_test, is_valid):
    response, args = middleware.validate_prohibition_number(prohibition_number=number_under_test)
    assert response is is_valid


clean_prohibition_numbers = [
    ("21-9000552", "21900055"),
    ("219000552", "21900055"),
    ("40-9000552", "40900055"),
    ("40-9000552", "40900055"),
    ("40-900055", "40900055"),
    ("40-900055", "40900055"),
    ("303456789", "30345678"),
    ("30-3456789", "30345678"),
    ("21900055", "21900055"),
    ("00900055", "00900055"),
    ("00-900055", "00900055"),
    ("21-900055", "21900055"),
    ("30900055X", "30900055"),
]


@pytest.mark.parametrize("before, after", clean_prohibition_numbers)
def test_clean_prohibition_number(before, after):
    response, args = middleware.clean_prohibition_number(prohibition_number=before)
    clean_prohibition_number = args.get('prohibition_number')
    assert response is True
    assert clean_prohibition_number == after


applications = [
    ({"resp": "fail"}, False),
    ({"resp": "success"}, False),
    ({"resp": "success", "data": {"applicationInfo": {}}}, True),
]


@pytest.mark.parametrize("response_under_test, is_valid", applications)
def test_validate_application_received_from_vips(response_under_test, is_valid):
    response, args = middleware.valid_application_received_from_vips(vips_application_data=response_under_test)
    assert response is is_valid


prohibitions_paid = [
    ({"receiptNumberTxt": "1234"}, True),
    ({"receiptNumberTxt": ""}, True),
    ({"otherAttribute": "1234"}, False),
    ({}, False),
]


@pytest.mark.parametrize("response_under_test, is_valid", prohibitions_paid)
def test_application_paid(response_under_test, is_valid):
    response, args = middleware.application_has_been_paid(vips_data=response_under_test)
    assert response is is_valid


@pytest.mark.parametrize("response_under_test, is_valid", prohibitions_paid)
def test_application_not_paid(response_under_test, is_valid):
    response, args = middleware.application_not_paid(vips_data=response_under_test)
    assert response is not is_valid


status_responses = [
    ({"applicationId": "1234"}, True),
    ({"applicationId": ""}, True),
    ({"otherAttribute": "1234"}, False),
    ({}, False),
]


@pytest.mark.parametrize("response_under_test, is_valid", status_responses)
def test_application_saved_to_vips(response_under_test, is_valid):
    response, args = middleware.application_has_been_saved_to_vips(vips_data=response_under_test)
    assert response is is_valid


@pytest.mark.parametrize("response_under_test, is_valid", status_responses)
def test_application_not_saved_to_vips(response_under_test, is_valid):
    response, args = middleware.application_not_previously_saved_to_vips(vips_data=response_under_test)
    assert response is not is_valid


form_names = [
    ("Document_submission", True),
    ("prohibtion_review", True),
    ("abc_dde", True),
    ("abcdefg", True),
    ("abc123", False),
    ("ab", False),
]


@pytest.mark.parametrize("string_under_test, is_valid", form_names)
def test_application_saved_to_vips(string_under_test, is_valid):
    response, args = middleware.validate_form_name(form_name=string_under_test)
    assert response is is_valid


payloads_test = [
    ('prohibition_review', '{"attribute": "value"}', "=xmlstre", True)
]


@pytest.mark.parametrize("form_name, json_data, xml, is_valid", payloads_test)
def test_create_payload(form_name, json_data, xml, is_valid):
    xml_as_dict = json.loads(json_data)
    assert isinstance(xml_as_dict, dict)
    response, args = middleware.create_form_payload(
        form_name=form_name, xml_as_dict=xml_as_dict, xml_base64=xml, config=Config)
    assert args['payload']['event_type'] == form_name
    assert args['payload'][form_name]['xml'] == xml
    assert args['payload'][form_name] == xml_as_dict
    assert response is is_valid


form_parameters_test = [
    (dict({"encrypt_at_rest": False}), False),
    (dict({"encrypt_at_rest": True}), True),
]


@pytest.mark.parametrize("record_under_test, is_valid", form_parameters_test)
def test_add_encrypt_at_rest_attribute(record_under_test, is_valid):
    payload = dict()
    response, args = middleware.add_encrypt_at_rest_attribute(
        form_parameters=record_under_test, payload=payload)
    assert args['payload']['encrypt_at_rest'] == is_valid
    assert response is True


example_form_names = [
    ("abc_dde", True),
    ("abcdefg", True),
    ("", False),
]


@pytest.mark.parametrize("string_under_test, is_valid", example_form_names)
def test_form_name_provided(string_under_test, is_valid):
    with application.test_request_context('/v1/publish/event/form?form={}'.format(string_under_test)):
        response, args = middleware.form_name_provided(request=flask.request)
        assert response is is_valid
        if is_valid:
            assert args['form_name'] == string_under_test


content_types = [
    ("application/json", False),
    ("application/xml", True),
    ("", False),
]


@pytest.mark.parametrize("string_under_test, is_valid", content_types)
def test_content_type_is_xml(string_under_test, is_valid):
    with application.test_request_context('/v1/publish/event/form', content_type=string_under_test):
        response, args = middleware.content_type_is_xml(request=flask.request)
        assert response is is_valid


xml_data = [
    ("<xml>okay</xml>", True),
    ("<data><attrib>one</attrib><attrib_2>two</attrib_2></data>", True),
    ("<xml>not okay<xml>", False),
]


@pytest.mark.parametrize("string_under_test, is_valid", xml_data)
def test_convert_xml_to_dict(string_under_test, is_valid):
    with application.test_request_context('/v1/publish/event/form', data=string_under_test):
        response, args = middleware.convert_xml_to_dictionary_object(request=flask.request)
        assert response is is_valid
        if is_valid:
            assert isinstance(args['xml_as_dict'], dict)


@pytest.mark.parametrize("string_under_test, is_valid", xml_data)
def test_get_xml_from_request(string_under_test, is_valid):
    form_name = 'sample_form_name'
    with application.test_request_context('/v1/publish/event/form', data=string_under_test):
        response, args = middleware.get_xml_from_request(
            request=flask.request, payload=dict({form_name: {}}), form_name=form_name)
        assert response is True
        assert 'xml_bytes' in args
        assert len(args['xml_bytes']) > 0


form_parameters_test_queue = [
    (dict({"queue": "ingested"}), 'ingested'),
    (dict({"queue": "other"}), 'other'),
]


@pytest.mark.parametrize("record_under_test, queue", form_parameters_test_queue)
def test_add_encrypt_at_rest_attribute(record_under_test, queue):
    payload = dict()
    response, args = middleware.get_queue_name_from_parameters(
        form_parameters=record_under_test, payload=payload)
    assert args['queue'] == queue
    assert response is True


vips_payment_dates = [
    ("2020-09-10 20:59:45 -07:00", "2020-09-11 13:31:22", True),
    ("2020-09-10 20:59:45 -07:00", "2020-09-11 20:59:22", True),
    ("2020-09-10 20:59:45 -07:00", "2020-09-11 20:24:00", True),
    ("2020-09-10 20:59:45 -07:00", "2020-09-10 21:00:22", True),
    ("2020-09-10 20:59:45 -07:00", "2020-09-11 21:00:22", False),
    ("2020-09-10 20:59:45 -07:00", "2020-09-12 13:31:22", False),
]


@pytest.mark.parametrize("payment_date, current_time_is, expected", vips_payment_dates)
def test_paid_not_more_than_24hrs_ago(payment_date, current_time_is, expected):
    payment_data = dict()
    payment_data['paymentDate'] = payment_date
    tz = pytz.timezone('America/Vancouver')
    today_unaware = datetime.strptime(current_time_is, "%Y-%m-%d %H:%M:%S")
    today_date = tz.localize(today_unaware, is_dst=False)
    print('today date is: {}'.format(today_date.isoformat()))
    response, args = middleware.paid_not_more_than_24hrs_ago(
        today_date=today_date, payment_data=payment_data)
    assert response is expected


def test_get_data_from_schedule_form():
    # check that json attributes with null values are converted to None type
    sample_data = load_json_into_dict('python/tests/sample_data/form/schedule_picker_submission.json')
    response, args = middleware.get_data_from_schedule_form(message=sample_data)
    assert args.get('requested_time_code') == 'MjAyMC0xMC0wNyAwOTozMDowMCAtMDc6MDB8MjAyMC0xMC0wNyAxMDowMDowMCAtMDc6MDA='
    assert args.get('prohibition_number') == '21-900040'
    assert args.get('driver_last_name') == 'Gordon'


example_last_names = [
    ("abc++dde", False),
    ("$abcdde", False),
    ("abcdefg", True),
    ("Coté", True),
    ("", False),
]


@pytest.mark.parametrize("last_name, expected", example_last_names)
def test_validate_driver_last_name(last_name, expected):
    response, args = middleware.validate_drivers_last_name(driver_last_name=last_name)
    assert response is expected


presentation_types = [
    # type  cause     requested  gets
    ("IRP", "IRP90FAIL",  "ORAL",    "ORAL"),
    ("IRP", "IRP90FAIL",  "WRIT",    "WRIT"),
    ("IRP", "IRP30WARN",  "ORAL",    "ORAL"),
    ("IRP", "IRP30WARN",  "WRIT",    "WRIT"),
    ("IRP", "IRP3",       "ORAL",    "WRIT"),
    ("IRP", "IRP3",       "WRIT",    "WRIT"),
    ("IRP", "IRP7",       "ORAL",    "WRIT"),
    ("IRP", "IRP7",       "WRIT",    "WRIT"),

    ("UL",  "",           "ORAL",    "WRIT"),
    ("UL",  "",           "WRIT",    "WRIT"),
    ("ADP", "BREATH",     "ORAL",    "ORAL"),
    ("ADP", "BREATH",     "WRIT",    "WRIT"),

]


@pytest.mark.parametrize("notice_type, cause, requested_type, expected", presentation_types)
def test_change_presentation_type_to_written_if_not_eligible(notice_type, cause, requested_type, expected):
    vips_data = {
        "originalCause": cause,
        "noticeTypeCd": notice_type
    }
    response, args = middleware.force_presentation_type_to_written_if_ineligible_for_oral(
        presentation_type=requested_type, vips_data=vips_data)
    assert response is True
    assert args['presentation_type'] == expected


def test_decode_compress_encode_xml():
    string_under_test = load_xml_to_string('python/tests/sample_data/form/form_submission.xml')
    bytes_under_test = string_under_test.encode()
    response, args = middleware.base_64_encode_xml(xml_bytes=bytes_under_test)
    response, args = middleware.compress_form_data_xml(xml_base64=args['xml_base64'])
    assert 'xml' in args


def test_get_human_friendly_time_slot_string_for_oral_review():
    time_slot = {
        "reviewStartDtm": "2020-09-04 10:00:00 -07:00",
        "reviewEndDtm": "2020-09-04 10:30:00 -07:00"
    }
    friendly_string = vips.time_slot_to_friendly_string(time_slot, "ORAL")
    assert friendly_string['label'] == 'Fri, Sep 4, 2020 - 10:00AM to 10:30AM'


def test_get_human_friendly_time_slot_string_for_written_review():
    time_slot = {
        "reviewStartDtm": "2020-09-04 10:00:00 -07:00",
        "reviewEndDtm": "2020-09-04 10:30:00 -07:00"
    }
    friendly_string = vips.time_slot_to_friendly_string(time_slot, "WRIT")
    assert friendly_string['label'] == 'Fri, Sep 4, 2020 at 9:30AM'


review_date_in_the_future = [
    ("2020-09-10 20:59:45 -07:00", "2020-09-11 13:31:22", False),
    ("2020-09-10 13:59:45 -07:00", "2020-09-10 13:31:22", True),
]


@pytest.mark.parametrize("review_date, current_time_is, expected", review_date_in_the_future)
def test_review_date_in_the_future(review_date, current_time_is, expected):
    vips_data = dict({'reviewStartDtm': review_date})
    tz = pytz.timezone('America/Vancouver')
    today_unaware = datetime.strptime(current_time_is, "%Y-%m-%d %H:%M:%S")
    today_date = tz.localize(today_unaware, is_dst=False)
    print('today date is: {}'.format(today_date.isoformat()))
    response, args = middleware.is_review_in_the_future(
        today_date=today_date, vips_data=vips_data)
    assert response is expected


disclosure_data = [
    {
        "disclosedDtm": "2020-09-10 20:59:45 -07:00",
        "documentId": "123"
    },
    {
        "documentId": "124"
    },
{
        "documentId": "127"
    }
]


def test_is_any_unsent_disclosure_method():
    vips_data = dict({
        "disclosure": disclosure_data
    })
    response, args = middleware.is_any_unsent_disclosure(vips_data=vips_data)
    assert response is True
    assert len(args.get('disclosures')) == 2


additional_review_times = [
    ("2020-11-02", "2020-11-09", 3, 3, 2),
    ("2020-11-02", "2020-11-09", 2, 3, 3),
    ("2020-11-02", "2020-11-09", 1, 3, 4),
]


@pytest.mark.parametrize("min_review_date, max_review_date, initial_days_offered, expected_days, expected_time_slots",
                         additional_review_times)
def test_query_for_additional_review_times(min_review_date, max_review_date,
                                           initial_days_offered, expected_days, expected_time_slots, monkeypatch):
    iso = "%Y-%m-%d"
    first_date = vips.next_business_date(datetime.strptime(max_review_date, iso))
    end_date = vips.next_business_date(datetime.strptime(min_review_date, iso))

    class MockConfig:
        MIN_REVIEW_DAYS_OFFERED = 3
        ADDITIONAL_DAYS_TO_QUERY = 4

    def mock_schedule_get(*args) -> tuple:
        return True, dict({
            "time_slots": [
                {
                    "reviewStartDtm": end_date.strftime(iso) + " 09:00:00 -08:00",
                    "reviewEndDtm": end_date.strftime(iso) + " 09:30:00 -08:00",
                }
            ],
            "number_review_days_offered": 1
        })

    monkeypatch.setattr(vips, "schedule_get", mock_schedule_get)

    is_success, args = middleware.query_for_additional_review_times(
        correlation_id="abcde",
        number_review_days_offered=initial_days_offered,
        presentation_type="ORAL",
        max_review_date=end_date,
        min_review_date=first_date,
        config=MockConfig,
        vips_data={
            "noticeTypeCd": "IRP"
        },
        time_slots=list([
            {
                "reviewStartDtm": first_date.strftime(iso) + " 11:00:00 -08:00",
                "reviewEndDtm": first_date.strftime(iso) + " 11:30:00 -08:00",
            },
            {
                "reviewStartDtm": first_date.strftime(iso) + " 10:00:00 -08:00",
                "reviewEndDtm": first_date.strftime(iso) + " 10:30:00 -08:00",
            }
        ])
    )

    logging.info(json.dumps(args.get('time_slots')))
    assert args['number_review_days_offered'] == expected_days
    assert len(args['time_slots']) == expected_time_slots
    for slot in args.get('time_slots'):
        assert isinstance(slot, dict)
        assert "reviewStartDtm" in slot
        assert "reviewEndDtm" in slot


def test_create_send_disclosure_method():
    event_type_string = "send_disclosure"
    class FakeConfig:
        PAYLOAD_VERSION_NUMBER = "1.5"

    data = dict({
        "firstGivenNm": "First",
        "surnameNm": "Last",
        "email": "applicant@gov.bc.ca"
    })
    response, args = middleware.create_disclosure_event(
        vips_application=data,
        config=FakeConfig,
        prohibition_number="20123456"
    )
    message_dict = args.get('message')
    assert response is True
    assert "1.5" in message_dict["event_version"]
    assert event_type_string in message_dict["event_type"]
    assert "First Last" in message_dict[event_type_string]["applicant_name"]
    assert "applicant@gov.bc.ca" in message_dict[event_type_string]["email"]
    assert "20123456" in message_dict[event_type_string]["prohibition_number"]


def test_create_verify_schedule_method():
    event_type_string = "verify_schedule"
    tz = pytz.timezone("America/Vancouver")
    class FakeConfig:
        PAYLOAD_VERSION_NUMBER = "1.5"

    data = dict({
        "receipt_number": "ABC-123",
        "receipt_amount": "50"
    })
    response, args = middleware.create_verify_schedule_event(
        receipt_date=datetime.now(tz),
        payload=data,
        config=FakeConfig,
        prohibition_number="20123456"
    )
    message_dict = args.get('message')
    assert response is True
    assert "1.5" in message_dict["event_version"]
    assert event_type_string in message_dict["event_type"]
    assert "ABC-123" in message_dict[event_type_string]["receipt_number"]
    assert datetime.now(tz).strftime("%Y-%m-%d") in message_dict[event_type_string]["receipt_date"]
    assert "50" in message_dict[event_type_string]["receipt_amount"]
    assert "20123456" in message_dict[event_type_string]["prohibition_number"]


def test_query_on_a_stat_holiday(monkeypatch):
    iso = "%Y-%m-%d"
    first_date = vips.next_business_date(datetime.strptime("2020-12-28", iso))
    end_date = vips.next_business_date(datetime.strptime("2020-12-28", iso))

    from python.ingestor.config import Config as IngestorConfig

    def mock_schedule_get(*args) -> tuple:
        return True, dict({
            "time_slots": [],
            "number_review_days_offered": 0
        })

    monkeypatch.setattr(vips, "schedule_get", mock_schedule_get)

    is_success, args = middleware.query_for_additional_review_times(
        correlation_id="abcde",
        number_review_days_offered=1,
        presentation_type="ORAL",
        max_review_date=end_date,
        min_review_date=first_date,
        config=IngestorConfig,
        vips_data={
            "noticeTypeCd": "IRP"
        },
        time_slots=list([])
    )

    logging.info(json.dumps(args.get('time_slots')))
    assert args['number_review_days_offered'] == 1
    assert args['time_slots'] == []


@pytest.mark.parametrize("presentation_type", ["ORAL", "WRIT"])
def test_query_for_additional_dates_method_checks_3_consecutive_dates(presentation_type, monkeypatch):
    iso = "%Y-%m-%d"
    first_date = datetime.strptime("2020-12-27", iso)
    end_date = datetime.strptime("2020-12-28", iso)

    expected_dates_queried = ['2020-12-29', '2020-12-30', '2020-12-31']

    from python.ingestor.config import Config as IngestorConfig

    def mock_schedule_get(*args) -> tuple:
        actual_date_string = args[2].strftime(iso)
        expected_date_string = expected_dates_queried.pop(0)
        assert actual_date_string == expected_date_string
        assert args[1] == presentation_type
        return True, dict({
            "time_slots": [],
            "number_review_days_offered": 0
        })

    monkeypatch.setattr(vips, "schedule_get", mock_schedule_get)

    is_success, args = middleware.query_for_additional_review_times(
        correlation_id="abcde",
        number_review_days_offered=0,
        presentation_type=presentation_type,
        max_review_date=end_date,
        min_review_date=first_date,
        config=IngestorConfig,
        vips_data={
            "noticeTypeCd": "IRP"
        },
        time_slots=list([])
    )

    assert len(expected_dates_queried) == 0
    assert args['number_review_days_offered'] == 0
    assert args['time_slots'] == []


def test_query_for_additional_dates_method_counts_stat_holidays_in_maximum_days(monkeypatch):
    iso = "%Y-%m-%d"
    first_date = datetime.strptime("2020-12-27", iso)
    end_date = datetime.strptime("2020-12-29", iso)

    expected_dates_queried = ['2020-12-30', '2020-12-31']

    from python.ingestor.config import Config as IngestorConfig

    def mock_schedule_get(*args) -> tuple:
        actual_date_string = args[2].strftime(iso)
        expected_date_string = expected_dates_queried.pop(0)
        assert actual_date_string == expected_date_string
        assert args[1] == "ORAL"
        return True, dict({
            "time_slots": [],
            "number_review_days_offered": 0
        })

    monkeypatch.setattr(vips, "schedule_get", mock_schedule_get)

    is_success, args = middleware.query_for_additional_review_times(
        correlation_id="abcde",
        number_review_days_offered=0,
        presentation_type="ORAL",
        max_review_date=end_date,
        min_review_date=first_date,
        config=IngestorConfig,
        vips_data={
            "noticeTypeCd": "IRP"
        },
        time_slots=list([])
    )

    assert len(expected_dates_queried) == 0
    assert args['number_review_days_offered'] == 0
    assert args['time_slots'] == []


