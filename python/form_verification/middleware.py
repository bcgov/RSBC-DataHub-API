from datetime import datetime, timedelta
import logging


def middle_logic(functions: list, **args):
    """
    Recursive function that calls each middleware function in the list.
    The list of functions past in are in pairs -- a success function and
    a failure function.  If the success function is successful, the next
    success function is called, otherwise the failure function is called.

    The middleware is called like this:

    middleware_to_test = [(success1, failure1)]
    middle_logic(middleware_to_test)

    """
    if functions:
        success, failure = functions.pop(0)
        flag, args = success(**args)
        print("Flag is", flag)
        if flag:
            middle_logic(functions, **args)
        else:
            print("Calling failure...")
            failure(**args)


def user_submitted_last_name_matches_vips(**args):
    """
    Check that last name retrieved from the VIPS API matches the
    last name entered by the applicant via the form.
    Required arguments:
     - message=

    """
    message = args.get('message')
    last_name_as_submitted = message['form_submission']['form']['section-identification-information']['control-driver-last-name']
    last_name_from_vips = message['form_submission']['form']['vips_response']['prohibitionStatus']['surnameNm']
    print(last_name_as_submitted, last_name_from_vips)
    # TODO - normalize and capitalize both last names before comparison
    is_last_name_match = bool(last_name_from_vips == last_name_as_submitted)
    return is_last_name_match, args


def prohibition_should_have_been_entered_in_vips(**args):
    """
    Fails if the application should be placed in a hold queue until VIPS has more time
    to enter the paper prohibition into the database.
    Required arguments:
     - message=
     - delay_days=
    """
    message = args.get('message')
    date_served_string = message['form_submission']['form']['section-irp-information']['control-date-served']
    today = datetime.today()
    date_served = datetime.strptime(date_served_string, '%Y-%m-%d')

    is_holdable = bool("vips" not in message['form_submission']['form'] and (today - date_served).days < args.get('delay_days'))
    return not is_holdable, args


def prohibition_exists_in_vips(**args):
    message = args.get('message')
    return "vips" in message['form_submission']['form']


def date_served_not_older_than_one_week(**args):
    """
    Check that the date served ENTERED BY THE USER in no older than one week.
    Required arguments:
     - message=
    """
    days_in_week = 7
    message = args.get('message')
    # TODO - verify date served from VIPS, not user supplied date
    date_served_string = message['form_submission']['form']['section-irp-information']['control-date-served']
    today = datetime.today()
    date_served = datetime.strptime(date_served_string, '%Y-%m-%d')
    # In legislation, prohibitions cannot be appealed after one week
    return bool((today - date_served).days <= days_in_week), args


def prohibition_not_found_event(**args):
    """
    add event to queue to email applicant
    :param args:
    :return:
    """
    # TODO - create an event; write to VERIFIED queue
    logging.debug('prohibition not found')
    pass


def last_name_mismatch_event(**args):
    """
    add event to queue to email applicant
    :param args:
    :return:
    """
    # TODO - create an event; write to VERIFIED queue
    logging.debug('user entered last name does not match vips')
    pass


def not_yet_in_vips_event(**args):
    """
    add event to hold queue, check again later
    :param args:
    :return:
    """
    # TODO - create an event; write to VERIFIED queue
    logging.debug('prohibition not yet entered in VIPS')
    pass


def prohibition_older_than_7_days_event(**args):
    """
    add event to hold queue, check again later
    :param args:
    :return:
    """
    # TODO - create an event; write to VERIFIED queue
    logging.debug('prohibition served more than 7 days ago')
    pass
