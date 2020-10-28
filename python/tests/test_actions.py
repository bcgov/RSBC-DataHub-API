import pytest
import python.common.actions as actions
from python.form_handler.config import Config
from datetime import datetime, timedelta
import json


class TestActions:

    @staticmethod
    def test_add_hold_until_attribute():
        message = dict()
        is_success, args = actions.add_hold_before_trying_vips_again(message=message, config=Config)
        modified_message = args.get('message')
        print(json.dumps(modified_message))
        today = datetime.today()
        hold_hours = int(Config.HOURS_TO_HOLD_BEFORE_TRYING_VIPS)
        assert is_success
        assert 'hold_until' in modified_message
        expected = (today + timedelta(hours=hold_hours)).isoformat()
        assert modified_message['hold_until'][0:20] == expected[0:20]

    # set the hold_time to +x hours from now
    hours_from_now = [
        (1, False),
        (2, False),
        (3, False),
        (-1, True),
        (-2, True),
        (-3, True),
    ]

    @pytest.mark.parametrize("offset_hours, expected", hours_from_now)
    def test_is_not_on_hold_method(self, offset_hours, expected):
        message = dict()
        now = datetime.now()
        message['hold_until'] = (now + timedelta(hours=offset_hours)).isoformat()
        is_not_on_hold, args = actions.is_not_on_hold(message=message, config=Config)
        print("is on hold: {}, now, {}, hold until: {}".format(not is_not_on_hold, now.isoformat(), message['hold_until']))
        assert is_not_on_hold == expected

    @staticmethod
    def test_is_on_hold_method_with_no_hold_until_attribute():
        message = dict()
        is_success, args = actions.is_not_on_hold(message=message, config=Config)
        assert is_success is True

    @staticmethod
    def test_add_unknown_event_error_to_message():
        message = dict()
        message['event_type'] = 'fake_event'
        success, args = actions.add_unknown_event_error_to_message(message=message)
        assert success is True
        assert 'errors' in args.get('message')
