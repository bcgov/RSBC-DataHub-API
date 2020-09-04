import logging
from python.common.message import encode_message
from python.form_handler.config import Config
import python.common.email as email
import json

logging.basicConfig(level=Config.LOG_LEVEL)


def update_vips_status(**args) -> tuple:
    # TODO - complete this method
    return True, args


def has_hold_expired(**args) -> tuple:
    # TODO - complete this method
    logging.info('has hold expired - method not implemented')
    return True, args


def add_do_not_process_until_attribute(**args) -> tuple:
    # TODO - complete this method
    return True, args


def save_application_to_vips(**args) -> tuple:
    # TODO - complete this method
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


def add_to_watch_queue(**args) -> tuple:
    config = args.get('config')
    message = args.get('message')
    writer = args.get('writer')
    logging.warning('writing back to watch queue')
    is_successful = writer.publish(config.WATCH_QUEUE, encode_message(message, config.ENCRYPT_KEY))
    if not is_successful:
        logging.critical('unable to write to RabbitMQ {} queue'.format(config.WATCH_QUEUE))
        return False, args
    return True, args


def unable_to_send_email(**args) -> tuple:
    logging.critical('unable to send email')
    return args


def unable_to_acknowledge_receipt(**args) -> tuple:
    logging.critical('unable to acknowledge receipt to RabbitMQ')
    config = args.get('config')
    title = 'Critical Error: Unable to acknowledge receipt to RabbitMQ'
    body = 'Unable to acknowledge receipt to RabbitMQ'
    return email.send_email_to_admin(config=config, title=title, body=body), args


def unable_to_save_to_vips_api(**args) -> tuple:
    logging.critical('inside unable_to_save_to_vips_api()')
    config = args.get('config')
    message = args.get('message')
    title = 'Critical Error: Unable to save to VIPS'
    body_text = 'While attempting to save an application to VIPS, an error was returned. ' + \
                'We will save the record to a failed write queue in RabbitMQ.'
    logging.critical('unable to save to VIPS: {}'.format(json.dumps(message)))
    return email.send_email_to_admin(config=config, title=title, body=body_text), args


def unknown_event_type(**args) -> tuple:
    message = args.get('message')
    config = args.get('config')
    title = 'Critical Error: Unknown Event Type'
    body_text = "An unknown event has been received: " + message['event_type']
    logging.critical('unknown event type: {}'.format(message['event_type']))
    return email.send_email_to_admin(config=config, title=title, body=body_text), args


