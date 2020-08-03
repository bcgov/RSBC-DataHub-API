from python.form_verification.config import Config
from python.common.rabbitmq import RabbitMQ
from python.common.vips_api import get_prohibition
from python.common.message import Message
import python.form_verification.middleware as mw
import logging
import json


class Listener:
    """
        This listener watches the RabbitMQ WATCH_QUEUE defined in the
        Config.  When a message appears in the queue the Listener:
         - invokes callback(),
         - calls out to the VIPS API and checks to see if the prohibition exists
         - invokes middleware to determine the appropriate event
    """
    def __init__(self, config, rabbit_writer, rabbit_listener, message):
        self.config = config
        self.writer = rabbit_writer
        self.listener = rabbit_listener
        self.message = message

        self.logger = logging.getLogger()
        self.logger.setLevel(level=config.LOG_LEVEL)
        self.logger.warning('*** validator initialized  ***')

    def main(self):
        """
            Start listening for messages on the WATCH_QUEUE
            when a message arrives invoke the callback()
        :return:
        """
        self.listener.consume(self.config.WATCH_QUEUE, self.callback)

    def callback(self, ch, method, properties, body):
        self.logger.info('message received; callback invoked')

        message_dict = self.message.decode_message(body, self.config.ENCRYPT_KEY)
        prohibition_number = message_dict['form_submission']['form']['section-irp-information']['control-prohibition-number']

        is_get_success, vips_response = get_prohibition(prohibition_number, self.config)
        if is_get_success:
            message_dict['form_submission']['vips_response'] = vips_response['data']['status']

            # invoke middleware chain to determine which event to generate
            # each pair of functions below represents (success, failure)
            mw.middle_logic([
                (mw.prohibition_should_have_been_entered_in_vips, mw.not_yet_in_vips_event),
                (mw.prohibition_exists_in_vips, mw.prohibition_not_found_event),
                (mw.user_submitted_last_name_matches_vips, mw.last_name_mismatch_event),
                (mw.date_served_not_older_than_one_week, mw.prohibition_older_than_7_days_event)

            ], message=message_dict, delay_days=self.config.DAYS_TO_DELAY_FOR_VIPS_DATA_ENTRY)

            # Acknowledge the message add to the WRITE queue
            self.logger.debug('middleware logic complete; returning event: %s', message_dict['event_type'])
            if self.writer.publish(
                    self.config.WRITE_QUEUE,
                    self.message.encode_message(message_dict, self.config.ENCRYPT_KEY)):
                ch.basic_ack(delivery_tag=method.delivery_tag)

        else:
            self.logger.warning('no response from the VIPS API')
            # TODO - write event back to the watch queue
            #  we can't proceed without access to VIPS


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
            Config.RETRY_DELAY),
        Message()
    ).main()
