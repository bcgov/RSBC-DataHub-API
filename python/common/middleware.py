from datetime import datetime, timedelta, timezone
from python.common.vips_api import vips_str_to_datetime
import python.common.prohibitions as pro
import logging
from python.common.config import Config
import python.common.vips_api as vips
import pytz
import re
import json

logging.basicConfig(level=Config.LOG_LEVEL)


def create_correlation_id(**args) -> tuple:
    correlation_id = vips.generate_correlation_id()
    args['correlation_id'] = correlation_id
    logging.info('CorrelationID: {}'.format(correlation_id))
    return True, args


def get_data_from_prohibition_review_form(**args) -> tuple:
    """
    Get key data from the message.  We can be sure the keys are in the message
    because the validator checks for all these message attributes.
    """
    m = args.get('message')
    event_type = m['event_type']
    args['applicant_role'] = m[event_type]['form']['identification-information']['applicant-role']
    first_name = m[event_type]['form']['identification-information']['driver-first-name']
    last_name = m['prohibition_review']['form']['identification-information']['driver-last-name']
    args['driver_last_name'] = last_name
    args['driver_full_name'] = "{} {}".format(first_name, last_name)
    args['applicant_first_name'] = m[event_type]['form']['identification-information']['first-name-applicant']
    args['applicant_last_name'] = m[event_type]['form']['identification-information']['last-name-applicant']
    args['applicant_email_address'] = m[event_type]['form']['identification-information']['applicant-email-address']
    args['prohibition_number'] = m[event_type]['form']['prohibition-information']['prohibition-number-clean']
    args['date_of_service'] = m['prohibition_review']['form']['prohibition-information']['date-of-service']
    return True, args


def validate_prohibition_number(**args) -> tuple:
    prohibition_number = args.get('prohibition_number')
    if re.match(r"^\d{8}$", prohibition_number) is None:
        error = 'prohibition number failed validation: {}'.format(prohibition_number)
        logging.info(error)
        args['error_string'] = error
        return False, args
    return True, args


def update_vips_status(**args) -> tuple:
    """
    Return True if the VIPS API responds to the get status request
    Further middleware required to determine if the query found a prohibition
    """
    config = args.get('config')
    prohibition_number = args.get('prohibition_number')
    correlation_id = args.get('correlation_id')
    is_api_callout_successful, vips_status_data = vips.status_get(prohibition_number, config, correlation_id)
    if is_api_callout_successful:
        args['vips_status'] = vips_status_data
        return True, args
    error = 'the VIPS get_status operation returned an invalid response'
    args['error_string'] = error
    logging.info(error)
    return False, args


def get_application_details(**args) -> tuple:
    """
    Return True if the VIPS API responds to the get application request
    Further middleware required to determine if the application is valid
    """
    config = args.get('config')
    correlation_id = args.get('correlation_id')
    guid = args.get('application_id')
    is_api_callout_successful, vips_application_data = vips.application_get(guid, config, correlation_id)
    if is_api_callout_successful:
        args['vips_application_data'] = vips_application_data
        return True, args
    error = 'the VIPS get_application operation returned an invalid response'
    args['error_string'] = error
    logging.info(error)
    return False, args


def valid_application_received_from_vips(**args) -> tuple:
    """
    Returns TRUE if the response from VIPS indicates a valid
    application was returned from VIPS
    """
    vips_application_data = args.get('vips_application_data')
    if 'resp' in vips_application_data and vips_application_data['resp'] == "success":
        args['vips_application'] = vips_application_data['data']['applicationInfo']
        return True, args
    error = 'a valid application was not returned from VIPS'
    args['error_string'] = error
    logging.info(error)
    return False, args


def get_invoice_details(**args) -> tuple:
    vips_application = args.get('vips_application')
    vips_data = args.get('vips_data')
    prohibition = pro.prohibition_factory(vips_data['noticeTypeCd'])
    presentation_type = vips_application['presentationTypeCd']
    args['amount_due'] = prohibition.amount_due(presentation_type)
    args['presentation_type'] = presentation_type
    args['service_date'] = vips.vips_str_to_datetime(vips_data['effectiveDt'])
    args['prohibition'] = prohibition
    return True, args


def prohibition_exists_in_vips(**args) -> tuple:
    """
    Returns TRUE if the response from VIPS indicates a prohibition
    was found that matches the prohibition_number provided
    """
    vips_status = args.get('vips_status')
    if 'resp' in vips_status and vips_status['resp'] == "success":
        args['vips_data'] = vips_status['data']['status']
        return True, args
    error = 'the prohibition does not exist in VIPS'
    args['error_string'] = error
    logging.info(error)
    return False, args


def user_submitted_last_name_matches_vips(**args) -> tuple:
    """
    Check that last name retrieved from the VIPS API matches the
    last name entered by the applicant via the form.
    """
    vips_data = args.get('vips_data')
    driver_last_name = args.get('driver_last_name')
    logging.info("vips DATA: {}".format(json.dumps(vips_data)))
    if vips.is_last_name_match(vips_data, driver_last_name):
        return True, args
    error = 'the last name submitted does not match VIPS'
    args['error_string'] = error
    logging.info(error)
    return False, args


def application_has_been_paid(**args) -> tuple:
    """
    Check that application has been paid
    """
    vips_data = args.get('vips_data')
    if 'receiptNumberTxt' in vips_data:
        return True, args
    error = 'the application has not been paid'
    logging.info(error)
    args['error_string'] = error
    return False, args


def application_not_paid(**args) -> tuple:
    """
    Check that application has NOT been paid
    """
    vips_data = args.get('vips_data')
    if 'receiptNumberTxt' not in vips_data:
        return True, args
    error = 'the application has previously been paid'
    logging.info(error)
    args['error_string'] = error
    return False, args


def application_has_been_submitted(**args) -> tuple:
    """
    Check that application has been paid
    """
    vips_data = args.get('vips_data')
    if 'applicationId' in vips_data:
        args['application_id'] = vips_data['applicationId']
        return True, args
    error = 'the application has not been submitted'
    logging.info(error)
    args['error_string'] = error
    return False, args


def prohibition_served_recently(**args) -> tuple:
    """
    Returns TRUE if the prohibition was served within the previous 3 days;
    otherwise returns FALSE
    """
    date_served_string = args.get('date_of_service')
    config = args.get('config')
    delay_days = int(config.DAYS_TO_DELAY_FOR_VIPS_DATA_ENTRY)

    # Note: we have to rely on the date_served as submitted by the user -- not the date in VIPS
    # Check to see if enough time has elapsed to enter the prohibition into VIPS
    today = datetime.today()
    date_served = datetime.strptime(date_served_string, '%Y-%m-%d')
    very_recently_served = (today - date_served).days < delay_days
    if very_recently_served:
        return True, args
    error = 'prohibition not served within the past {} days'.format(delay_days)
    args['error_string'] = error
    logging.info(error)
    print("date_served: {}, very_recently_served: {}".format(date_served, very_recently_served))
    return False, args


def date_served_not_older_than_one_week(**args) -> tuple:
    """
    If the prohibition type is ADP or IRP then check
    that the date served is no older than 7 days.
    Prohibitions may not be appealed after 7 days.
    """
    vips_data = args.get('vips_data')
    prohibition = pro.prohibition_factory(vips_data['noticeTypeCd'])
    if prohibition.MUST_APPLY_FOR_REVIEW_WITHIN_7_DAYS:
        days_in_week = 7
        date_served_string = vips_data['effectiveDt']
        tz = pytz.timezone('America/Vancouver')
        today = datetime.now(tz)
        date_served = vips_str_to_datetime(date_served_string)
        if (today - date_served).days < days_in_week:
            return True, args
        error = 'the prohibition is older than one week'
        args['error_string'] = error
        logging.info(error)
        return False, args
    return True, args


def has_drivers_licence_been_seized(**args) -> tuple:
    """
    Returns TRUE if VIPS indicates the driver's licence has been seized
    and the notice type (IRP & ADP) requires the licence to be taken.
    """
    vips_data = args.get('vips_data')
    prohibition = pro.prohibition_factory(vips_data['noticeTypeCd'])
    if prohibition.DRIVERS_LICENCE_MUST_BE_SEIZED_BEFORE_APPLICATION_ACCEPTED:
        if vips_data['driverLicenceSeizedYn'] == "Y":
            return True, args
        error = 'drivers licence has not been seized'
        args['error_string'] = error
        logging.info(error)
        return False, args
    return True, args
