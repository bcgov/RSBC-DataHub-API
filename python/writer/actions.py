import logging
from python.common.message import encode_message


def add_to_failed_write_queue(**args):
    config = args.get('config')
    message = args.get('message')
    writer = args.get('writer')
    channel = args.get('channel')
    method = args.get('method')
    logging.warning('writing to failed write queue')
    if writer.publish(config.FAIL_QUEUE, encode_message(message, config.ENCRYPT_KEY)):
        channel.basic_ack(delivery_tag=method.delivery_tag)
    else:
        logging.critical('unable to write to RabbitMQ {} queue'.format(config.FAIL_QUEUE))
    return args


def unable_to_send_email(**args):
    logging.warning('unable to send email')
    return args


def unable_to_save_to_vips_api(**args):
    logging.critical('unable to save to the vips API')
    return args


def unknown_event_type(**args) -> tuple:
    message = args.get('message')
    logging.critical('unknown event type: {}'.format(message['event_type']))
    return False, args

