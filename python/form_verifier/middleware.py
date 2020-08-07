from datetime import datetime, timedelta
from dateutil import parser
from unicodedata import normalize
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
    last_name_as_submitted = remove_accents(message['form_submission']['form']['identification-information']['driver-last-name'])
    last_name_from_vips = remove_accents(message['form_submission']['vips_response']['data']['status']['surnameNm'])
    logging.debug('compare last name: {} and {}'.format(last_name_as_submitted, last_name_from_vips))
    is_last_name_match = bool(last_name_from_vips.upper() == last_name_as_submitted.upper())
    return is_last_name_match, args


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
    logging.debug('Prohibition exists in VIPS: {}'.format(result))
    return result, args


def date_served_not_older_than_one_week(**args):
    """
    Check that the date served is no older than 7 days.
    """
    days_in_week = 7
    message = args.get('message')
    date_served_string = message['form_submission']['vips_response']['data']['status']['effectiveDt']
    today = datetime.today()
    date_served = parser.isoparse(date_served_string)
    # In legislation, prohibitions cannot be appealed after one week
    return bool((today - date_served).days <= days_in_week), args


def prohibition_not_found_event(**args):
    """
    create prohibition not found event
    """
    event = "prohibition_not_found"
    logging.debug('create {} event'.format(event))
    message = args.get('message')
    args['message'] = modify_event(message, event)
    return args


def last_name_mismatch_event(**args):
    """
    create last name mismatch event
    """
    event = "last_name_mismatch"
    logging.debug('create {} event'.format(event))
    message = args.get('message')
    args['message'] = modify_event(message, event)
    return args


def not_yet_in_vips_event(**args):
    """
    create not yet in vips event
    """
    event = 'prohibition_not_yet_in_vips'
    logging.debug('create {} event'.format(event))
    message = args.get('message')
    args['message'] = modify_event(message, event)
    # TODO - determine appropriate hold period so we don't query the api multiple times per second
    logging.critical('TODO - hard coded hold_until value needs to be replaced')
    message['do_not_process_until'] = '2020-01-01'
    return args


def prohibition_older_than_7_days_event(**args):
    """
    create prohibition older than 7 days event
    """
    event = 'prohibition_served_more_than_7_days_ago'
    logging.debug('create {} event'.format(event))
    message = args.get('message')
    args['message'] = modify_event(message, event)
    return args


def modify_event(message: dict, new_event_type: str):
    """
    Replace the current event_type with new_event_type and rename
    corresponding event_type attribute
    """
    current_event_type = message['event_type']
    message[new_event_type] = message.pop(current_event_type)
    message['event_type'] = new_event_type
    return message


def remove_accents(input_str):
    nfkd_form = normalize('NFKD', input_str)
    only_ascii = nfkd_form.encode('ASCII', 'ignore')
    return only_ascii
