from datetime import datetime, timedelta, timezone
from python.common.vips_api import vips_str_to_datetime
import python.common.prohibitions as pro
import logging
from python.form_handler.config import Config
from python.common.vips_api import is_last_name_match
import pytz

logging.basicConfig(level=Config.LOG_LEVEL)


def user_submitted_last_name_matches_vips(**args):
    """
    Check that last name retrieved from the VIPS API matches the
    last name entered by the applicant via the form.
    """
    message = args.get('message')
    last_name_as_submitted = message['form_submission']['form']['identification-information']['driver-last-name']
    return is_last_name_match(message['form_submission']['vips_response'], last_name_as_submitted), args


def prohibition_should_have_been_entered_in_vips(**args):
    """
    Returns False if the application should be placed on hold until
    VIPS has more time to enter the paper prohibition into the database
    """
    message = args.get('message')
    # Note: we have to rely on the date_served as submitted by the user -- not the date in VIPS
    date_served_string = message['form_submission']['form']['prohibition-information']['date-of-service']
    today = datetime.today()
    date_served = datetime.strptime(date_served_string, '%Y-%m-%d')
    very_recently_served = (today - date_served).days < int(args.get('delay_days'))
    record_not_found_in_vips = message['form_submission']['vips_response']['resp'] == 'fail'
    is_holdable = record_not_found_in_vips and very_recently_served
    print(date_served, very_recently_served, record_not_found_in_vips, is_holdable)
    logging.debug('Prohibition should already be entered in VIPS: {} and {}'.format(not is_holdable, date_served_string))
    return not is_holdable, args


def prohibition_exists_in_vips(**args):
    message = args.get('message')
    result = message['form_submission']['vips_response']['resp'] == 'success'
    logging.info('Prohibition exists in VIPS: {}'.format(result))
    return result, args


def date_served_not_older_than_one_week(**args):
    """
    If the prohibition type is ADP or IRP then check
    that the date served is no older than 7 days.
    Prohibitions may not be appealed after 7 days.
    """
    message = args.get('message')
    prohibition = pro.prohibition_factory(message['form_submission']['vips_response']['noticeTypeCd'])
    if prohibition.MUST_APPLY_FOR_REVIEW_WITHIN_7_DAYS:
        days_in_week = 7
        date_served_string = message['form_submission']['vips_response']['effectiveDt']
        tz = pytz.timezone('America/Vancouver')
        today = datetime.now(tz)
        date_served = vips_str_to_datetime(date_served_string)
        return bool((today - date_served).days < days_in_week), args
    else:
        return True, args


def has_drivers_licence_been_seized(**args):
    """
    Returns true if VIPS indicates the driver's licence has been seized
    """
    message = args.get('message')
    prohibition = pro.prohibition_factory(message['form_submission']['vips_response']['noticeTypeCd'])
    if prohibition.DRIVERS_LICENCE_MUST_BE_SEIZED_BEFORE_APPLICATION_ACCEPTED:
        return message['form_submission']['vips_response']['driverLicenceSeizedYn'] == "Y", args
    return True, args


def is_driver_the_applicant(**args):
    """
    Returns true if the driver is the applicant. Returns false if the
    driver is being represented by a lawyer or authorized person
    """
    message = args.get('message')
    return message['form_submission']['form']['identification-information']['driver-last-name'] == 'Y', args