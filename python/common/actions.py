import logging
from datetime import datetime, timedelta
from python.common.message import encode_message, add_error_to_message
from python.common.config import Config
import iso8601

logging.basicConfig(level=Config.LOG_LEVEL, format=Config.LOG_FORMAT)


def is_not_on_hold(**args) -> tuple:
    """
    Returns true if the message is not on hold -- either
    there is no 'hold_until' attribute OR there is a
    hold_unit attribute, but it's ISO datetime if
    greater than the current datetime.
    """
    message = args.get('message')
    if 'hold_until' not in message:
        return True, args
    now = datetime.now()
    hold_until = iso8601.parse_date(message['hold_until'], None)
    return now >= hold_until, args


def add_hold_before_trying_vips_again(**args) -> tuple:
    """
    Adds a do not process until attribute to the message
    """
    message = args.get('message')
    config = args.get('config')
    hold_hours = int(config.HOURS_TO_HOLD_BEFORE_TRYING_VIPS)
    message['hold_until'] = (datetime.today() + timedelta(hours=hold_hours)).isoformat()
    return True, args


def add_hold_before_sending_disclosure(**args) -> tuple:
    """
    Adds a do not process until attribute to the message
    """
    message = args.get('message')
    config = args.get('config')
    hold_hours = int(config.HOURS_TO_HOLD_BEFORE_DISCLOSURE)
    message['hold_until'] = (datetime.today() + timedelta(hours=hold_hours)).isoformat()
    return True, args


def add_hold_to_verify_schedule(**args) -> tuple:
    """
    Adds a do not process until attribute to the message
    """
    message = args.get('message')
    config = args.get('config')
    hold_hours = config.HOURS_APPLICANT_HAS_TO_SCHEDULE
    message['hold_until'] = (datetime.today() + timedelta(hours=hold_hours)).isoformat()
    return True, args


def add_to_failed_queue(**args) -> tuple:
    config = args.get('config')
    message = args.get('message')
    writer = args.get('writer')
    logging.warning('writing to failed write queue')
    if not writer.publish(config.FAIL_QUEUE, encode_message(message, config.ENCRYPT_KEY)):
        logging.critical('unable to write to RabbitMQ {} queue'.format(config.FAIL_QUEUE))
        return False, args
    return True, args


def add_to_hold_queue(**args) -> tuple:
    config = args.get('config')
    message = args.get('message')
    writer = args.get('writer')
    logging.warning('writing to hold queue')
    if not writer.publish(config.HOLD_QUEUE, encode_message(message, config.ENCRYPT_KEY)):
        logging.critical('unable to write to RabbitMQ {} queue'.format(config.HOLD_QUEUE))
        return False, args
    return True, args


def add_unknown_event_error_to_message(**args) -> tuple:
    message = args.get('message')
    event_type = '[ no event type attribute ]'
    if 'event_type' in message:
        event_type = message['event_type']
    error = dict({
        "error": "unknown event type: {}".format(event_type)
    })
    message = add_error_to_message(message, error)
    return True, args


def add_to_rabbitmq_queue(**args) -> tuple:
    encoded_message = args.get('encoded_message')
    queue = args.get('queue')
    writer = args.get('writer')
    logging.warning('writing to {} queue'.format(queue))
    if not writer.publish(queue, encoded_message):
        logging.critical('unable to write to RabbitMQ {} queue'.format(queue))
        return False, args
    return True, args
