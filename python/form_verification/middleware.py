from datetime import datetime, timedelta
import logging


def middle_logic(functions: list, **args):
    """
    Recursive function that calls each middleware function in the list.
    The list of functions past in are in pairs -- a success function and
    a failure function.  If the success function is successful, the next
    success function is called, otherwise the failure function is called.

    The middleware is called like this:

    middleware_to_test = [(success1, failure1)
                          (success2, failure2)]
    middle_logic(middleware_to_test)

    """
    if functions:
        success_function, failure_function = functions.pop(0)
        logging.debug('calling success function: ' + success_function.__name__)
        flag, args = success_function(**args)
        print("Flag is", flag)
        if flag:
            logging.debug('calling middleware logic recursively')
            middle_logic(functions, **args)
        else:
            logging.debug('calling failure function: ' + failure_function.__name__)
            failure_function(**args)


def user_submitted_last_name_matches_vips(**args):
    """
    Check that last name retrieved from the VIPS API matches the
    last name entered by the applicant via the form.
    """
    message = args.get('message')
    last_name_as_submitted = message['form_submission']['form']['section-identification-information']['control-driver-last-name']
    last_name_from_vips = message['form_submission']['vips_response']['surnameNm']
    logging.debug('compare last name: %s and %s', last_name_as_submitted, last_name_from_vips)
    # TODO - normalize and capitalize both last names before comparison
    is_last_name_match = bool(last_name_from_vips == last_name_as_submitted)
    return is_last_name_match, args


def prohibition_should_have_been_entered_in_vips(**args):
    """
    Returns False if the application should be placed in a hold queue until
    VIPS has more time to enter the paper prohibition into the database
    """
    message = args.get('message')
    date_served_string = message['form_submission']['form']['section-irp-information']['control-date-served']
    today = datetime.today()
    date_served = datetime.strptime(date_served_string, '%Y-%m-%d')
    very_recently_served = (today - date_served).days < args.get('delay_days')
    is_not_holdable = not(bool("vips_response" not in message['form_submission'] and very_recently_served))
    logging.debug('Prohibition should already be entered in VIPS: %s and %s', is_not_holdable, date_served_string)
    return is_not_holdable, args


def prohibition_exists_in_vips(**args):
    message = args.get('message')
    result = "vips_response" in message['form_submission']['form']
    logging.debug('Prohibition exists in VIPS: %s', result)
    return result, args


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
    create prohibition not found event
    """
    logging.debug('create prohibition not found event')
    message = args.get('message')
    message['event_type'] = 'prohibition_not_found'
    return args


def last_name_mismatch_event(**args):
    """
    create last name mismatch event
    """
    logging.debug('create last name mismatch event')
    message = args.get('message')
    message['event_type'] = 'last_name_mismatch'
    return args


def not_yet_in_vips_event(**args):
    """
    create not yet in vips event
    """
    logging.debug('create prohibition not yet entered in VIPS event')
    message = args.get('message')
    message['event_type'] = 'prohibition_not_yet_in_vips'
    # TODO - determine appropriate hold period so we don't query the api multiple times per second
    logging.critical('TODO - hard coded value needs to be replaced')
    message['hold_until'] = '2020-01-01'
    return args


def prohibition_older_than_7_days_event(**args):
    """
    create prohibition older than 7 days event
    """
    logging.debug('create prohibition served more than 7 days ago event')
    message = args.get('message')
    message['event_type'] = 'prohibition_served_more_than_7_days_ago'
    return args
