from python.writer.config import Config
from python.writer.database import write as database_writer
from python.common.vips_api import store as save_to_vips
import python.common.email as email
from python.common.helper import middle_logic
from python.common.rabbitmq import RabbitMQ
from python.common.message import decode_message
import python.writer.actions as actions

import logging


class Listener:
    """
        This listener watches the RabbitMQ WATCH_QUEUE defined in the
        Config.  When a message appears in the queue the Listener:
         - invokes callback(),
         - transforms the message using the Mapper class,
         - finally passing a dict to the Database class for writing
    """
    
    def __init__(self, config, rabbit_writer, rabbit_listener):
        self.config = config
        self.listener = rabbit_listener
        self.writer = rabbit_writer
        logging.basicConfig(level=config.LOG_LEVEL)
        logging.warning('*** writer initialized ***')

    def main(self):
        # start listening for messages on the WATCH_QUEUE
        # when a message arrives invoke the callback()
        self.listener.consume(self.config.WATCH_QUEUE, self.callback)

    def callback(self, ch, method, properties, body):
        logging.info('message received; callback invoked')

        # convert body (in bytes) to string
        message_dict = decode_message(body, self.config.ENCRYPT_KEY)

        middle_logic(self.get_listeners(message_dict['event_type']),
                     message=message_dict, config=self.config, writer=self.writer, channel=ch, method=method)

        # if we get here the middle_logic functions were all successful so we
        # can acknowledge the message and delete it from the WRITE_WATCH_QUEUE
        ch.basic_ack(delivery_tag=method.delivery_tag)

    def get_listeners(self, event_type: str) -> list:
        """
        Get the list of (success, failure) function pairs to invoke
         for a particular event type
        """
        if event_type in self.listeners():
            return self.listeners()[event_type]
        else:
            # TODO - replace empty list with at least one default function
            logging.critical('Unknown event_type: ' + event_type)
            return [
                (actions.unknown_event_type, email.administrator)
            ]

    @staticmethod
    def listeners() -> dict:
        return {
            "evt_issuance": [
                (database_writer, actions.add_to_failed_write_queue)
            ],
            "vt_dispute_finding": [
                (database_writer, actions.add_to_failed_write_queue)
            ],
            "vt_dispute_status_update": [
                (database_writer, actions.add_to_failed_write_queue)
            ],
            "vt_dispute": [
                (database_writer, actions.add_to_failed_write_queue)
            ],
            "vt_payment": [
                (database_writer, actions.add_to_failed_write_queue)
            ],
            "vt_query": [
                (database_writer, actions.add_to_failed_write_queue)
            ],
            "form_submission": [
                (save_to_vips, actions.unable_to_save_to_vips_api),
                (email.invoice_to_applicant, actions.unable_to_send_email)
            ]
        }


if __name__ == "__main__":
    Listener(
        Config(),
        RabbitMQ(
            Config.RABBITMQ_USER,
            Config.RABBITMQ_PASS,
            Config.RABBITMQ_URL,
            Config.LOG_LEVEL,
            Config.MAX_CONNECTION_RETRIES,
            Config.RETRY_DELAY),
        RabbitMQ(
            Config.RABBITMQ_USER,
            Config.RABBITMQ_PASS,
            Config.RABBITMQ_URL,
            Config.LOG_LEVEL,
            Config.MAX_CONNECTION_RETRIES,
            Config.RETRY_DELAY)
    ).main()
