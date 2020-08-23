from python.form_verifier.config import Config
from python.common.rabbitmq import RabbitMQ
from python.common.vips_api import status_get
from python.common.message import encode_message, decode_message
from python.common.helper import middle_logic
import python.form_verifier.middleware as rules
import logging
import uuid
import json

logging.basicConfig(level=Config.LOG_LEVEL)


class Listener:
    """
        This listener watches the RabbitMQ WATCH_QUEUE defined in the
        Config.  When a message appears in the queue the Listener:
         - invokes callback(),
         - calls out to the VIPS API and, if successful, copies the status into the message
         - invokes middleware to determine the appropriate event
    """
    def __init__(self, config, rabbit_writer, rabbit_listener):
        self.config = config
        self.writer = rabbit_writer
        self.listener = rabbit_listener
        logging.warning('*** form verifier initialized  ***')

    def main(self):
        """
            Start listening for messages on the WATCH_QUEUE
            when a message arrives invoke the callback()
        :return:
        """
        self.listener.consume(self.config.WATCH_QUEUE, self.callback)

    def callback(self, ch, method, properties, body):
        logging.info('message received; callback invoked')

        message_dict = decode_message(body, self.config.ENCRYPT_KEY)
        prohibition_number = message_dict['form_submission']['form']['prohibition-information']['control-prohibition-number']
        message_dict['correlation_id'] = str(uuid.uuid4())

        is_get_success, vips_response = status_get(prohibition_number, self.config, message_dict['correlation_id'])
        if is_get_success:
            message_dict['form_submission']['vips_response'] = vips_response

            # invoke middleware chain to determine which event to generate
            # each pair of functions below represents (success, failure)
            middle_logic([
                (rules.prohibition_should_have_been_entered_in_vips, rules.not_yet_in_vips_event),
                (rules.prohibition_exists_in_vips, rules.prohibition_not_found_event),
                (rules.user_submitted_last_name_matches_vips, rules.last_name_mismatch_event),
                (rules.date_served_not_older_than_one_week, rules.prohibition_older_than_7_days_event),
                (rules.has_drivers_licence_been_seized, rules.licence_not_seized_event)

            ], message=message_dict, delay_days=self.config.DAYS_TO_DELAY_FOR_VIPS_DATA_ENTRY)

            # Acknowledge the message add to the WRITE queue
            logging.info('middleware logic complete; returning event: %s', message_dict['event_type'])
            if self.writer.publish(
                    self.config.WRITE_QUEUE,
                    encode_message(message_dict, self.config.ENCRYPT_KEY)):
                ch.basic_ack(delivery_tag=method.delivery_tag)

        else:
            logging.warning('Bad response from VIPS API: {}'.format(json.dumps(vips_response)))
            if self.writer.publish(
                    self.config.WATCH_QUEUE,
                    encode_message(message_dict, self.config.ENCRYPT_KEY)):
                ch.basic_ack(delivery_tag=method.delivery_tag)


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
