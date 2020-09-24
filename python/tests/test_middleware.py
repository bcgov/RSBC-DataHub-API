import pytz
from python.form_handler.config import Config
import python.common.vips_api as vips
from datetime import datetime, timedelta
import python.common.middleware as middleware
from python.common.helper import load_json_into_dict
import pytest
import flask
import json
from python.ingestor.routes import application


date_served_data = [
    ('IRP', "2020-09-10 20:59:45 -08:00", "2020-09-11 13:31:22", True),
    ('IRP', "2020-09-10 20:59:45 -08:00", "2020-09-16 13:31:22", True),
    ('IRP', "2020-09-10 20:59:45 -08:00", "2020-09-17 13:31:22", False),
    ('IRP', "2020-09-10 20:59:45 -08:00", "2020-09-18 13:31:22", False),
    ('IRP', "2020-09-10 20:59:45 -08:00", "2020-09-19 13:31:22", False),

    ('UL', "2020-09-10 20:59:45 -08:00", "2020-09-11 13:31:22", True),
    ('UL', "2020-09-10 20:59:45 -08:00", "2020-09-16 13:31:22", True),
    ('UL', "2020-09-10 20:59:45 -08:00", "2020-09-17 13:31:22", True),
    ('UL', "2020-09-10 20:59:45 -08:00", "2020-09-18 13:31:22", True),
    ('UL', "2020-09-10 20:59:45 -08:00", "2020-09-19 13:31:22", True),

    ('ADP', "2020-09-10 20:59:45 -08:00", "2020-09-10 21:31:22", True),
    ('ADP', "2020-09-10 20:59:45 -08:00", "2020-09-11 13:31:22", True),
    ('ADP', "2020-09-10 20:59:45 -08:00", "2020-09-16 13:31:22", True),
    ('ADP', "2020-09-10 20:59:45 -08:00", "2020-09-17 13:31:22", False),
    ('ADP', "2020-09-10 20:59:45 -08:00", "2020-09-18 13:31:22", False),
    ('ADP', "2020-09-10 20:59:45 -08:00", "2020-09-19 13:31:22", False),
]


@pytest.mark.parametrize("prohibition_type, notice_serve_date, today_is, expected", date_served_data)
def test_date_served_not_older_than_one_week_method(prohibition_type, notice_serve_date, today_is, expected):
    tz = pytz.timezone('America/Vancouver')
    today_unaware = datetime.strptime(today_is, "%Y-%m-%d %H:%M:%S")
    today_date = today_unaware.replace(tzinfo=tz)
    vips_data = dict()
    vips_data['noticeTypeCd'] = prohibition_type
    vips_data['noticeServedDt'] = notice_serve_date
    (result, args) = middleware.date_served_not_older_than_one_week(vips_data=vips_data, today_date=today_date)
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
    (0, True),
    (1, True),
    (2, True),
    (3, False),
    (4, False)
]


@pytest.mark.parametrize("date_offset, expected", served_recently_data)
def test_prohibition_served_recently_method(date_offset, expected):
    days = timedelta(date_offset)
    new_date = datetime.today() - days
    date_under_test = new_date.strftime("%Y-%m-%d")
    result, args = middleware.prohibition_served_recently(
        date_of_service=date_under_test,
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
    response, args = middleware.create_payload(form_name=form_name, xml_as_dict=xml_as_dict, xml=xml)
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
def test_using_base_64_encode_xml(string_under_test, is_valid):
    form_name = 'sample_form_name'
    with application.test_request_context('/v1/publish/event/form', data=string_under_test):
        response, args = middleware.base_64_encode_xml(
            request=flask.request, payload=dict({form_name: {}}), form_name=form_name)
        assert response is True
        assert 'xml' in args
        assert len(args['xml']) > 0


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
