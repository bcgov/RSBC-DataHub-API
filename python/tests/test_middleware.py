import pytest
from datetime import datetime, timedelta
import python.form_verifier.middleware as middleware
from python.common.helper import load_json_into_dict
import json

date_served_data = [
    ('IRP', 0, True),
    ('IRP', 1, True),
    ('IRP', 7, True),
    ('IRP', 8, False),
    ('UL', 0, True),
    ('UL', 1, True),
    ('UL', 7, True),
    ('UL', 8, True),
    ('ADP', 0, True),
    ('ADP', 1, True),
    ('ADP', 7, True),
    ('ADP', 8, False)
]


@pytest.mark.parametrize("prohibition_type, date_offset, expected", date_served_data)
def test_date_served_today_older_than_one_week_method(prohibition_type, date_offset, expected):
    sample_data = load_json_into_dict('python/tests/sample_data/irp_form_submission.json')
    date_under_test = (datetime.today() - timedelta(days=date_offset)).isoformat()
    response_from_api = load_json_into_dict('python/tests/sample_data/vips_response_success.json')
    sample_data['form_submission']['vips_response'] = response_from_api
    sample_data['form_submission']['vips_response']['data']['status']['noticeTypeCd'] = prohibition_type
    sample_data['form_submission']['vips_response']['data']['status']['effectiveDt'] = date_under_test
    (result, args) = middleware.date_served_not_older_than_one_week(message=sample_data)
    assert result is expected


last_name_match_data = [
    ('Jones', 'Jones', True),
    ('Jones', 'JONES', True),
    ('Coté', 'Cote', True),  # note the accent on the "e"
    ('Jones', 'Other', False)
]


@pytest.mark.parametrize("user_entered_last_name, last_name_from_vips, expected", last_name_match_data)
def test_user_submitted_last_name_matches_vips_method(user_entered_last_name, last_name_from_vips, expected):
    sample_data = load_json_into_dict('python/tests/sample_data/irp_form_submission.json')
    sample_data['form_submission']['form']['identification-information']['driver-last-name'] = user_entered_last_name
    response_from_api = load_json_into_dict('python/tests/sample_data/vips_response_success.json')
    response_from_api['data']['status']['surnameNm'] = last_name_from_vips
    sample_data['form_submission']['vips_response'] = response_from_api
    result, args = middleware.user_submitted_last_name_matches_vips(message=sample_data)
    assert result is expected


def test_modify_event_method():
    new_event_name = "new_event"
    event = load_json_into_dict('python/tests/sample_data/irp_form_submission.json')
    modified_event = middleware.modify_event(event, new_event_name)
    assert new_event_name in modified_event
    assert modified_event['event_type'] == new_event_name


should_have_been_entered_into_vips_data = [
    ('vips_response_404.json', 0, False),
    ('vips_response_404.json', 2, False),
    ('vips_response_404.json', 3, True),
    ('vips_response_success.json', 0, True),
    ('vips_response_success.json', 2, True),
    ('vips_response_success.json', 3, True)
]


@pytest.mark.parametrize("vips_response, date_offset, expected", should_have_been_entered_into_vips_data)
def test_prohibition_should_have_been_entered_in_vips_method(vips_response, date_offset, expected):
    days = timedelta(date_offset)
    new_date = datetime.today() - days
    date_under_test = new_date.strftime("%Y-%m-%d")
    sample_data = load_json_into_dict('python/tests/sample_data/irp_form_submission.json')
    sample_data['form_submission']['form']['prohibition-information']['date-of-service'] = date_under_test
    response_from_api = load_json_into_dict('python/tests/sample_data/' + vips_response)
    sample_data['form_submission']['vips_response'] = response_from_api
    print(json.dumps(sample_data))
    result, args = middleware.prohibition_should_have_been_entered_in_vips(message=sample_data, delay_days='3')
    assert result is expected


exists_in_vips_data = [
    ('vips_response_404.json', False),
    ('vips_response_success.json', True)
]


@pytest.mark.parametrize("vips_response, expected", exists_in_vips_data)
def test_prohibition_should_have_been_entered_in_vips_method(vips_response, expected):
    sample_data = load_json_into_dict('python/tests/sample_data/irp_form_submission.json')
    response_from_api = load_json_into_dict('python/tests/sample_data/' + vips_response)
    sample_data['form_submission']['vips_response'] = response_from_api
    result, args = middleware.prohibition_exists_in_vips(message=sample_data)
    assert result is expected


licence_seized = [
    ("Y", True),
    ("N", False)
]


@pytest.mark.parametrize("test_condition, expected", licence_seized)
def test_has_drivers_licence_been_seized_method(test_condition, expected):
    sample_data = load_json_into_dict('python/tests/sample_data/irp_form_submission.json')
    response_from_api = load_json_into_dict('python/tests/sample_data/vips_response_success.json')
    response_from_api['data']['status']['DriverLicenceSeizedYn'] = test_condition
    sample_data['form_submission']['vips_response'] = response_from_api
    result, args = middleware.has_drivers_licence_been_seized(message=sample_data)
    assert result is expected
