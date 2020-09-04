from python.form_handler.config import Config
import python.common.email as email
from python.common.helper import middle_logic
import python.form_handler.middleware as rules
from python.common.rabbitmq import RabbitMQ
from python.common.message import decode_message
import python.form_handler.actions as actions
import logging

logging.basicConfig(level=Config.LOG_LEVEL)


class Listener:
    """
        This listener watches the RabbitMQ WATCH_QUEUE defined in the
        Config.  When a message appears in the queue the Listener:
         - invokes callback(),
         - invokes middleware to determine the appropriate event
    """
    def __init__(self, config, rabbit_writer, rabbit_listener):
        self.config = config
        self.listener = rabbit_listener
        self.writer = rabbit_writer
        logging.warning('*** form verifier initialized  ***')

    def main(self):
        """
            Start listening for messages on the WATCH_QUEUE
            when a message arrives invoke the callback()
        """
        self.listener.consume(self.config.WATCH_QUEUE, self.callback)

    def callback(self, ch, method, properties, body):
        logging.info('message received; callback invoked')

        # convert body (in bytes) to string
        message_dict = decode_message(body, self.config.ENCRYPT_KEY)

        # invoke listener functions
        middle_logic(self.get_listeners(message_dict['event_type']),
                     message=message_dict,
                     config=self.config,
                     writer=self.writer,
                     channel=ch,
                     method=method,
                     logger=logging)

        # Regardless of whether the process above follows the happy path or not,
        # we need to acknowledge receipt of the message to RabbitMQ below. This
        # acknowledgement deletes it from the queue so the logic above must have
        # saved / handled the message before we get here.

        ch.basic_ack(delivery_tag=method.delivery_tag)

    def get_listeners(self, event_type: str) -> list:
        """
        Get the list of (success, failure) function pairs to invoke
         for a particular event type
        """
        if event_type in self.listeners():
            return self.listeners()[event_type]
        else:
            return [
                # TODO - add error to payload
                (actions.add_to_failed_queue, actions.do_nothing),
                # (actions.write_to_fail_queue, actions.unable_to_write_to_RabbitMQ),
            ]

    @staticmethod
    def listeners() -> dict:
        return {
            "form_submission": [
                (actions.has_hold_expired, actions.add_to_watch_queue),
                (actions.update_vips_status, actions.add_to_watch_queue),
                (rules.prohibition_should_have_been_entered_in_vips, actions.add_to_watch_queue),
                (rules.prohibition_exists_in_vips, email.applicant_prohibition_not_found),
                (rules.user_submitted_last_name_matches_vips, email.applicant_last_name_mismatch),
                (rules.date_served_not_older_than_one_week, email.applicant_prohibition_served_more_than_7_days_ago),
                (rules.has_drivers_licence_been_seized, email.applicant_licence_not_seized),
                (rules.is_driver_the_applicant, actions.accepted_driver_is_represented),
                (actions.accepted_driver_is_applicant, actions.unable_to_save_to_vips_api),
            ],
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
