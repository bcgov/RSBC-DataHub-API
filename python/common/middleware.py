from datetime import datetime, timedelta
import python.common.calculating_blood_alcohol as static_file
from python.common.vips_api import vips_str_to_datetime
import python.common.helper as helper
import python.common.prohibitions as pro
import logging
from cerberus import Validator as Cerberus
from python.common.config import Config
import python.common.vips_api as vips
from python.common.message import encode_message
import pytz
import re
import json
import xmltodict
import base64
import zlib


logging.basicConfig(level=Config.LOG_LEVEL, format=Config.LOG_FORMAT)


def create_correlation_id(**args) -> tuple:
    correlation_id = vips.generate_correlation_id()
    args['correlation_id'] = correlation_id
    logging.info('CorrelationID: {}'.format(correlation_id))
    return True, args


def get_data_from_application_form(**args) -> tuple:
    """
    Get key data from the prohibition_review form.  We can be sure
    the keys are in the message because the validator checks for
    these message attributes.
    """
    m = args.get('message')
    event_type = m['event_type']
    args['xml_base64'] = m[event_type]['xml']
    args['applicant_role_raw'] = m[event_type]['form']['identification-information']['applicant-role']
    args['applicant_first_name'] = m[event_type]['form']['identification-information']['first-name-applicant']
    args['applicant_last_name'] = m[event_type]['form']['identification-information']['last-name-applicant']
    args['applicant_email_address'] = m[event_type]['form']['identification-information']['applicant-email-address']
    args['applicant_phone_number'] = m[event_type]['form']['identification-information']['applicant-phone-number']
    args['prohibition_number'] = m[event_type]['form']['prohibition-information']['control-prohibition-number']
    args['date_of_service'] = m[event_type]['form']['prohibition-information']['date-of-service']
    args['hearing_request_type'] = m[event_type]['form']['review-information']['hearing-request-type']
    return True, args


def get_user_entered_notice_type_from_message(**args) -> tuple:
    """
    From the form, determine if the user has entered and IRP, ADP or UL prohibition
    """
    m = args.get('message')
    event_type = m['event_type']
    if m[event_type]['form']['prohibition-information']['control-is-adp'] == "true":
        args['user_entered_notice_type'] = "ADP"
    if m[event_type]['form']['prohibition-information']['control-is-irp'] == "true":
        args['user_entered_notice_type'] = "IRP"
    if m[event_type]['form']['prohibition-information']['control-is-ul'] == "true":
        args['user_entered_notice_type'] = "UL"
    return True, args


def populate_driver_name_fields_if_null(**args) -> tuple:
    """
    When driver is also the applicant, Orbeon doesn't fill in the driver's first
    and last name fields. This function populates the driver name fields.
    """
    m = args.get('message')
    event_type = m['event_type']
    if args.get('applicant_role_raw') == 'driver':
        first_name = m[event_type]['form']['identification-information']['first-name-applicant']
        last_name = m[event_type]['form']['identification-information']['last-name-applicant']
    else:
        # applicant is either a lawyer or advocate
        first_name = m[event_type]['form']['identification-information']['driver-first-name']
        last_name = m[event_type]['form']['identification-information']['driver-last-name']
    args['driver_last_name'] = last_name
    args['driver_full_name'] = "{} {}".format(first_name, last_name)
    return True, args


def validate_prohibition_number(**args) -> tuple:
    prohibition_number = args.get('prohibition_number')
    if re.match(r"^\d{8}$", prohibition_number) is None:
        logging.info('prohibition number failed validation: {}'.format(prohibition_number))
        args['error_string'] = "You have entered an invalid prohibition number, please try again."
        return False, args
    return True, args


def clean_prohibition_number(**args) -> tuple:
    """
    Remove any non-digits from the prohibition number
    and take only the first 8 digits
    """
    prohibition_number = args.get('prohibition_number')
    prohibition_number = re.sub(r"\D", "", prohibition_number)
    args['prohibition_number'] = prohibition_number[0:8]
    return True, args


def get_vips_status(**args) -> tuple:
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
    args['error_string'] = "The system is down, please try again later."
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
    args['error_string'] = "The system is down, please try again later."
    logging.info(error)
    return False, args


def valid_application_received_from_vips(**args) -> tuple:
    """
    Returns TRUE if the response from VIPS indicates a valid
    application was returned from VIPS
    """
    data = args.get('vips_application_data')
    if 'resp' in data and data['resp'] == "success" and 'data' in data:
        args['vips_application'] = data['data']['applicationInfo']
        return True, args
    logging.info(json.dumps(data))
    error = 'a valid application was not returned from VIPS'
    args['error_string'] = "The system is down, please try again later."
    logging.info(error)
    return False, args


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
    args['error_string'] = "The driving prohibition isn't in the system."
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
    args['error_string'] = "The last name doesn’t match a driving prohibition in the system."
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
    args['error_string'] = "The application review fee must be paid to continue."
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
    args['error_string'] = "The application review fee has already been paid."
    return False, args


def application_has_been_saved_to_vips(**args) -> tuple:
    """
    Check that application has been saved to VIPS
    """
    vips_data = args.get('vips_data')
    if 'applicationId' in vips_data:
        args['application_id'] = vips_data['applicationId']
        return True, args
    error = 'the application has not been submitted'
    logging.info(error)
    args['error_string'] = "You must submit an application before you can pay."
    return False, args


def application_not_previously_saved_to_vips(**args) -> tuple:
    """
    Check that application has NOT been saved to VIPS
    """
    vips_data = args.get('vips_data')
    if 'applicationId' not in vips_data:
        return True, args
    error = 'this prohibition already has an application on file'
    logging.info(error)
    args['error_string'] = "An application to review this prohibition has already been submitted."
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
    today = args.get('today_date')
    date_served = helper.localize_timezone(datetime.strptime(date_served_string, '%Y-%m-%d'))
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
    today = args.get('today_date')
    prohibition = pro.prohibition_factory(vips_data['noticeTypeCd'])
    if prohibition.MUST_APPLY_FOR_REVIEW_WITHIN_7_DAYS:
        days_in_week = 7
        date_served_string = vips_data['noticeServedDt']
        date_served = vips_str_to_datetime(date_served_string)
        if (today.date() - date_served.date()).days < days_in_week:
            return True, args
        error = 'the prohibition is older than one week'
        args['error_string'] = "The Notice of Prohibition was issued more than 7 days ago."
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
        args['error_string'] = "You can't proceed as your driver's licence was not surrendered to police."
        logging.info(error)
        return False, args
    return True, args


def save_application_to_vips(**args) -> tuple:
    vips_data = args.get('vips_data')
    is_save_successful, vips_response = vips.application_create(vips_data['noticeTypeCd'], **args)
    if is_save_successful:
        args['vips_application_data'] = vips_response
        return True, args
    error = 'the VIPS save_application operation returned an invalid response'
    args['error_string'] = "The system is down, please try again later."
    logging.info(error)
    return False, args


def get_invoice_details(**args) -> tuple:
    vips_application = args.get('vips_application')
    vips_data = args.get('vips_data')
    prohibition = pro.prohibition_factory(vips_data['noticeTypeCd'])
    presentation_type = vips_application['presentationTypeCd']
    args['amount_due'] = prohibition.amount_due(presentation_type)
    args['presentation_type'] = presentation_type
    args['service_date'] = vips.vips_str_to_datetime(vips_data['noticeServedDt'])
    args['prohibition'] = prohibition
    args['notice_type_verbose'] = prohibition.type_verbose()
    args['applicant_name'] = "{} {}".format(vips_application['firstGivenNm'], vips_application['surnameNm'])
    return True, args


def calculate_schedule_window(**args) -> tuple:
    service_date = args.get('service_date')
    prohibition = args.get('prohibition')
    args['min_review_date'], args['max_review_date'] = prohibition.get_min_max_review_dates(service_date)
    return True, args


def query_review_times_available(**args) -> tuple:
    vips_data = args.get('vips_data')
    min_review_date = args.get('min_review_date')
    max_review_date = args.get('max_review_date')
    review_type = args.get('presentation_type')
    config = args.get('config')
    logging.info('query review times available')
    time_slots = list()
    for query_date in vips.list_of_weekdays_dates_between(min_review_date, max_review_date):
        query_date_string = query_date.strftime("%Y-%m-%d")
        logging.info('check VIPS for time slots available on: {}'.format(query_date_string))
        is_successful, data = vips.schedule_get(vips_data['noticeTypeCd'], review_type, query_date_string, config)
        if data['resp'] == 'success' and len(data['data']['timeSlots']) > 0:
            time_slots += vips.time_slots_to_friendly_times(data['data']['timeSlots'], review_type)
    logging.debug(json.dumps(time_slots))
    args['time_slots'] = time_slots
    return True, args


def transform_receipt_date_from_pay_bc_format(**args) -> tuple:
    """
    Transform PayBC date format: 2020-09-15T16:59:04Z to datetime object
    """
    payload = args.get('payload')
    tz = pytz.timezone('UTC')
    try:
        date_object = datetime.strptime(payload['receipt_date'], "%Y-%m-%dT%H:%M:%SZ")
        args['receipt_date'] = tz.localize(date_object)
    except ValueError:
        error = 'receipt_date not formatted as expected'
        args['error_string'] = error
        logging.info(error)
        return False, args
    return True, args


def save_payment_to_vips(**args) -> tuple:
    payload = args.get('payload')
    config = args.get('config')
    # PayBC has the ability to pay multiple invoices in a single transaction
    # however we can assume there is only one transaction because this API only
    # returns a single invoice per prohibition number.
    prohibition_number = args.get('prohibition_number')
    correlation_id = args.get('correlation_id')
    is_successful, data = vips.payment_patch(prohibition_number,
                                             config,
                                             correlation_id,
                                             card_type=payload['cardtype'],
                                             receipt_amount=payload['receipt_amount'],
                                             receipt_date=args.get('receipt_date'),
                                             receipt_number=payload['receipt_number'])
    return is_successful, args


def validate_pay_bc_post_receipt(**args) -> tuple:
    config = args.get('config')
    payload = args.get('payload')
    method_name = 'receipt'
    schemas = helper.load_json_into_dict(config.SCHEMA_PATH + config.SCHEMA_FILENAME)

    # check that that the method_name has an associated validation schema
    if method_name not in schemas:
        logging.critical('{} does not have an associated validation schema'.format(method_name))

    # return the validation error message from the associated schema
    schema = schemas[method_name]
    logging.debug('schema: {}'.format(json.dumps(schema)))
    logging.debug('payload: {}'.format(payload))
    cerberus = Cerberus(schema['cerberus_rules'])
    cerberus.allow_unknown = schema['allow_unknown']
    if cerberus.validate(payload):
        args['prohibition_number'] = payload['invoices'][0]["trx_number"]
        logging.info('payload passed validation')
        return True, args
    else:
        logging.warning('payload failed validation: {}'.format(json.dumps(cerberus.errors)))
        return False, args


def transform_hearing_request_type(**args) -> tuple:
    hearing_request_type = args.get('hearing_request_type')
    if hearing_request_type is None or hearing_request_type == '':
        args['presentation_type'] = "WRIT"
    else:
        print('test: ' + hearing_request_type)
        args['presentation_type'] = hearing_request_type[:4].upper()
    return True, args


def transform_applicant_role_type(**args) -> tuple:
    role = args.get('applicant_role_raw')
    if role == 'driver':
        args['applicant_role'] = "APPNT"
    elif role == 'lawyer':
        args['applicant_role'] = "LWYR"
    elif role == 'advocate':
        args['applicant_role'] = "AUTHPERS"
    else:
        args['applicant_role'] = None
        return False, args
    return True, args


def content_type_is_xml(**args) -> tuple:
    request = args.get('request')
    if request.content_type == 'application/xml':
        return True, args
    error = 'received content type is not XML'
    args['error_string'] = error
    logging.info(error)
    return False, args


def content_type_is_json(**args) -> tuple:
    request = args.get('request')
    if request.content_type == 'application/json':
        return True, args
    error = 'received content type is not JSON'
    args['error_string'] = error
    logging.info(error)
    return False, args


def form_name_provided(**args) -> tuple:
    request = args.get('request')
    not_provided = 'unknown'
    args['form_name'] = request.args.get('form', not_provided)
    if args['form_name'] == not_provided or len(args['form_name']) == 0:
        error = 'missing key query parameter: form'
        args['error_string'] = error
        logging.info(error)
        return False, args
    return True, args


def validate_form_name(**args) -> tuple:
    form_name = args.get('form_name')
    if re.match(r"^[A-Za-z_]{3,30}$", form_name) is None:
        error = 'form_name failed validation: {}'.format(form_name)
        logging.info(error)
        args['error_string'] = error
        return False, args
    return True, args


def create_form_payload(**args) -> tuple:
    config = args.get('config')
    form_name = args.get('form_name')
    form_data = args.get('xml_as_dict')
    xml = args.get('xml_base64')
    form_data['xml'] = xml
    args['payload'] = dict({
            "event_version": config.PAYLOAD_VERSION_NUMBER,
            "event_date_time": datetime.now().isoformat(),
            "event_type": form_name,
            form_name: form_data
        })
    return True, args


def add_encrypt_at_rest_attribute(**args) -> tuple:
    parameters = args.get('form_parameters')
    args['encrypt_at_rest'] = parameters['encrypt_at_rest']
    return True, args


def convert_xml_to_dictionary_object(**args) -> tuple:
    request = args.get('request')
    try:
        args['xml_as_dict'] = xmltodict.parse(request.get_data())
    except xmltodict.expat.ExpatError:
        error = 'unable to convert XML to a dict'
        logging.info(error)
        args['error_string'] = error
        return False, args
    return True, args


def get_xml_from_request(**args) -> tuple:
    request = args.get('request')
    args['xml_bytes'] = request.get_data()
    return True, args


def base_64_encode_xml(**args) -> tuple:
    xml_raw = args.get('xml_bytes')
    args['xml_base64'] = base64.b64encode(xml_raw).decode()
    return True, args


def compress_form_data_xml(**args) -> tuple:
    xml_base64 = args.get('xml_base64')
    original_len = len(xml_base64)
    xml_bytes = base64.b64decode(xml_base64)
    xml_compressed = zlib.compress(xml_bytes)
    xml_encoded = base64.b64encode(xml_compressed).decode()
    args['xml'] = xml_encoded
    compressed_len = len(xml_encoded)
    percent_change = int((compressed_len - original_len)/original_len * 100)
    logging.info("compressing form XML using zlib has reduced string length by: {}%".format(percent_change))
    return True, args


def get_queue_name_from_parameters(**args) -> tuple:
    parameters = args.get('form_parameters')
    args['queue'] = parameters['queue']
    return True, args


def encode_payload(**args) -> tuple:
    payload = args.get('payload')
    config = args.get('config')
    args['encoded_message'] = encode_message(payload, config.ENCRYPT_KEY)
    return True, args


def content_length_within_bounds(**args) -> tuple:
    request = args.get('request')
    config = args.get('config')
    some_arbitrary_byte_value = config.MAX_FORM_SUBMISSION_BYTES
    return request.content_length < some_arbitrary_byte_value, args


def paid_not_more_than_24hrs_ago(**args) -> tuple:
    today_date = args.get('today_date')
    payment_data = args.get('payment_data')
    print(today_date)
    if 'paymentDate' not in payment_data:
        return True, args
    payment_date = vips_str_to_datetime(payment_data['paymentDate'])
    print(payment_date)
    if (today_date - payment_date).days < 1:
        return True, args
    error = 'the payment is older than 24 hours'
    args['error_string'] = "You are outside the 24-hour time allowed to schedule the review."
    logging.info(error)
    return False, args


def get_payment_status(**args) -> tuple:
    """
    Return True if the VIPS API responds to the get payment status
    Further middleware required to determine if the query found a prohibition
    """
    config = args.get('config')
    prohibition_number = args.get('prohibition_number')
    correlation_id = args.get('correlation_id')
    is_api_callout_successful, payment_data = vips.payment_get(prohibition_number, config, correlation_id)
    if is_api_callout_successful:
        args['vips_payment_data'] = payment_data
        return True, args
    error = 'the VIPS payment_get operation returned an invalid response'
    args['error_string'] = "The system is down, please try again later."
    logging.info(error)
    return False, args


def received_valid_payment_status(**args) -> tuple:
    """
    Returns TRUE if the response from VIPS indicates a prohibition
    was found that matches the prohibition_number provided
    """
    vips_payment_data = args.get('vips_payment_data')
    if 'data' in vips_payment_data and 'transactionInfo' in vips_payment_data['data']:
        args['payment_data'] = vips_payment_data['data']['transactionInfo']
        return True, args
    error = 'the payment does not exist in VIPS'
    args['error_string'] = "You must pay before you can schedule a review"
    logging.info(error)
    return False, args


def determine_current_datetime(**args) -> tuple:
    """
    Return args['today_date'] as a timezone aware python datetime object
    """
    tz = pytz.timezone('America/Vancouver')
    args['today_date'] = datetime.now(tz)
    return True, args


def validate_drivers_last_name(**args) -> tuple:
    """
    Return False if the driver last name has characters that
    shouldn't appear in any name, regardless of nationality
    """
    last_name = args.get('driver_last_name')
    if re.match(r"^[^±!@£$%^&*_+§¡€#¢§¶•ªº«\\/<>?:;|=.,]{1,30}$", last_name):
        return True, args
    logging.info('Driver last name includes prohibited characters')
    return False, args


def get_data_from_schedule_form(**args) -> tuple:
    """
    Get key data from the schedule_review.  We can be sure
    the keys are in the message because the validator checks for
    these message attributes.
    """
    m = args.get('message')
    event_type = m['event_type']
    args['prohibition_number'] = m[event_type]['form']['schedule-review-section']['prohibition-number']
    args['driver_last_name'] = m[event_type]['form']['schedule-review-section']['last-name']
    args['requested_time_code'] = m[event_type]['form']['schedule-review-section']['timeslot-selected']
    return True, args


def decode_selected_timeslot(**args) -> tuple:
    coded_time_slot = args.get('requested_time_code')
    args['requested_time_slot'] = vips.decode_time_slot(coded_time_slot)
    return True, args


def get_human_friendly_time_slot_string(**args) -> tuple:
    vips_application = args.get('vips_application')
    presentation_type = vips_application['presentationTypeCd']
    time_slot = args.get('requested_time_slot')
    args['friendly_review_time_slot'] = vips.time_slot_to_friendly_string(time_slot, presentation_type)['label']
    return True, args


def is_decoded_time_slot_valid(**args) -> tuple:
    requested_time_slot = args.get('requested_time_slot')
    if "reviewStartDtm" in requested_time_slot and "reviewEndDtm" in requested_time_slot:
        return True, args
    error = 'decoded time slot not in expected format'
    logging.info(error)
    args['error_string'] = error
    return False, args


def is_selected_timeslot_inside_schedule_window(**args) -> tuple:
    requested_time_slot = args.get('requested_time_slot')
    requested_date_time = vips.vips_str_to_datetime(requested_time_slot['reviewStartDtm'])
    min_review_date = args['min_review_date']
    max_review_date = args['max_review_date']
    if min_review_date <= requested_date_time < max_review_date + timedelta(days=1):
        return True, args
    error = 'selected time slot not within schedule window'
    logging.info(error)
    args['error_string'] = error
    return False, args


def force_presentation_type_to_written_if_ineligible_for_oral(**args) -> tuple:
    """
    Only ADP and certain kinds of IRP prohibitions are eligible for an
    oral review.  If the user has requested an oral review when they're
    not eligible, change the presentation type to written.
    """
    vips_data = args.get('vips_data')
    presentation_type = args.get('presentation_type')
    prohibition = pro.prohibition_factory(vips_data['noticeTypeCd'])
    if not prohibition.is_eligible_for_oral_review(vips_data) and presentation_type == 'ORAL':
        args['force_to_written_review'] = True
        args['presentation_type'] = 'WRIT'
        error = "Applicant has selected an oral review but they're not eligible. Changing the presentation_type to WRIT"
        logging.info(error)
    return True, args


def save_schedule_to_vips(**args) -> tuple:
    is_save_successful, vips_response = vips.schedule_create(**args)
    if is_save_successful:
        args['vips_schedule_data'] = vips_response
        return True, args
    error = 'the VIPS save_schedule operation returned an invalid response'
    args['error_string'] = "The system is down, please try again later."
    logging.info(error)
    return False, args


def create_disclosure_event(**args) -> tuple:
    """
    After a review date is scheduled, the system will send disclosure
    (police documents) to the applicant.  Since a business rule states
    that disclosure cannot be sent immediately, we use this method to
    create a disclosure event that's added to the hold queue.
    """
    config = args.get('config')
    vips_application = args.get('vips_application')
    event_type = "send_disclosure"
    args['message'] = dict({
        "event_version": config.PAYLOAD_VERSION_NUMBER,
        "event_date_time": datetime.now().isoformat(),
        "event_type": event_type,
        event_type: {
            "applicant_name": "{} {}".format(vips_application['firstGivenNm'], vips_application['surnameNm']),
            "email": vips_application['email'],
            "prohibition_number": args.get('prohibition_number'),
        }
    })
    return True, args


def is_any_unsent_disclosure(**args) -> tuple:
    """
    Returns True if there is unsent disclosure to send to applicant
    """
    vips_data = args.get('vips_data')
    unsent_disclosure = list()
    if 'disclosure' in vips_data:
        for item in vips_data['disclosure']:
            if 'disclosedDtm' not in item:
                unsent_disclosure.append(item)
        if len(unsent_disclosure) > 0:
            args['disclosures'] = unsent_disclosure
            return True, args
    return False, args


def retrieve_unsent_disclosure(**args) -> tuple:
    """
    Retrieve disclosure files from VIPS and format as attachments
    in a format for the Common Services API.
    """
    disclosures = args.get('disclosures')
    correlation_id = args.get('correlation_id')
    config = args.get('config')
    disclosure_for_applicant = list()
    error = False
    for disclosure in disclosures:
        is_successful, data = vips.disclosure_get(disclosure['documentId'], config, correlation_id)
        if is_successful and data['resp'] == "success" and 'data' in data:
            mine_type = data['data']['document']['mimeType']
            file_extension = mine_type[-3:]
            disclosure_for_applicant.append(dict(
                {
                    "content": data['data']['document']['document'],
                    "contentType": "string",
                    "encoding": "base64",
                    "filename": "disclosure_{}.{}".format(disclosure['documentId'], file_extension)
                }
            ))
        else:
            error = True
    if error is True:
        return False, args
    args['disclosure_for_applicant'] = disclosure_for_applicant
    return True, args


def if_required_add_adp_disclosure(**args) -> tuple:
    """
    ADP's require a static PDF file to be included with all disclosure
    that describes how blood alcohol values are calculated.
    """
    vips_data = args.get('vips_data')
    if vips_data['noticeTypeCd'] == 'ADP':
        disclosure_for_applicant = args.get('disclosure_for_applicant')
        disclosure_for_applicant.append(static_file.superintendents_report_calculating_bac())
        args['disclosure_for_applicant'] = disclosure_for_applicant
    return True, args


def mark_disclosure_as_sent(**args) -> tuple:
    disclosures = args.get('disclosures')
    correlation_id = args.get('correlation_id')
    config = args.get('config')
    disclosure_for_applicant = list()
    error = False
    for disclosure in disclosures:
        successful, data = vips.disclosure_patch(disclosure['documentId'], config, correlation_id, **args)
        if not successful:
            error = True
    if error is True:
        return False, args
    args['disclosure_for_applicant'] = disclosure_for_applicant
    return True, args


def get_data_from_disclosure_event(**args) -> tuple:
    m = args.get('message')
    event_type = m['event_type']
    args['applicant_name'] = m[event_type]['applicant_name']
    args['applicant_email_address'] = m[event_type]['email']
    args['prohibition_number'] = m[event_type]['prohibition_number']
    return True, args


def is_review_in_the_future(**args) -> tuple:
    """
    Get review date start time from VIPS and compare it with today's
    date.  If the review is in the future, return True; otherwise
    False
    """
    vips_data = args.get('vips_data')
    review_start_datetime = vips_str_to_datetime(vips_data['reviewStartDtm'])
    today_date = args.get('today_date')
    return today_date < review_start_datetime, args


def review_has_not_been_scheduled(**args) -> tuple:
    """
    Check that review has not previously been scheduled
    """
    vips_data = args.get('vips_data')
    if 'reviewStartDtm' not in vips_data:
        return True, args
    error = 'A review has already been scheduled for this prohibition.'
    logging.info(error)
    args['error_string'] = error
    return False, args


def review_has_been_scheduled(**args) -> tuple:
    """
    Check that review has been scheduled
    """
    vips_data = args.get('vips_data')
    if 'reviewStartDtm' in vips_data:
        return True, args
    error = 'A review has not been scheduled'
    logging.info(error)
    args['error_string'] = "You must book a review date before you can submit evidence for the review."
    return False, args


def is_applicant_ineligible_for_oral_review_but_requested_oral(**args) -> tuple:
    if args.get('force_to_written_review'):
        return True, args
    return False, args


def get_data_from_document_submission_form(**args) -> tuple:
    """
    Get key data from the Document_submission form.  We can be sure
    the keys are in the message because the validator checks for
    these message attributes.
    """
    m = args.get('message')
    event_type = m['event_type']
    args['prohibition_number'] = m[event_type]['form']['applicant-information-section']['control-prohibition-number']
    args['driver_last_name'] = m[event_type]['form']['applicant-information-section']['control-driver-last-name']
    args['email_address'] = m[event_type]['form']['applicant-information-section']['applicant-email-address']
    return True, args


def payment_success(**args) -> tuple:
    args['payment_success'] = True
    return True, args
