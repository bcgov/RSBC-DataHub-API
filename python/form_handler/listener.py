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
                     writer=self.writer)

        # Regardless of whether the process above follows the happy path or not,
        # we need to acknowledge receipt of the message to RabbitMQ below. This
        # acknowledgement deletes it from the WATCH queue so the logic above
        # must have saved / handled the message before we get here.

        ch.basic_ack(delivery_tag=method.delivery_tag)

    def get_listeners(self, event_type: str) -> list:
        """
        Get the list of nested list of functions to invoke
        for a particular form type
        """
        if event_type in self.listeners():
            return self.listeners()[event_type]
        else:
            return self.listeners()['unknown_event']

    @staticmethod
    def listeners() -> dict:
        return {
            "unknown_event": [
                {
                    "try": actions.add_unknown_event_error_to_message,
                    "fail": []
                },
                {
                    "try": actions.add_to_failed_queue,
                    "fail": []
                },
                {
                    "try": email.admin_unknown_event_type,
                    "fail": []
                }
            ],
            "form_submission": [
                { 
                    "try": actions.is_not_on_hold,
                    "fail": [
                        {"try": actions.add_to_hold_queue, "fail": []}
                    ]
                },
                {
                    "try": actions.update_vips_status,
                    "fail": [
                        {"try": actions.add_to_hold_queue, "fail": []}
                    ]
                },
                {
                    "try": rules.prohibition_should_have_been_entered_in_vips,
                    "fail": [
                        {"try": email.applicant_prohibition_not_yet_in_vips, "fail": []},
                        {"try": actions.add_hold_until_attribute, "fail": []},
                        {"try": actions.add_to_hold_queue, "fail": []}
                    ]
                },
                {
                    "try": rules.prohibition_exists_in_vips,
                    "fail": [
                        {"try": email.applicant_prohibition_not_found, "fail": []}
                    ]
                },
                {
                    "try": rules.user_submitted_last_name_matches_vips,
                    "fail": [
                        {"try": email.applicant_last_name_mismatch, "fail": []}
                    ]
                },
                {
                    "try": rules.date_served_not_older_than_one_week,
                    "fail": [
                        {"try": email.applicant_prohibition_served_more_than_7_days_ago(), "fail": []}
                    ]
                },
                {
                    "try": rules.has_drivers_licence_been_seized,
                    "fail": [
                        {"try": email.applicant_licence_not_seized, "fail": []}
                    ]
                },
                {
                    "try": actions.save_application_to_vips,
                    "fail": [
                        {"try": actions.add_to_failed_queue, "fail": []},
                        {"try": email.admin_unable_to_save_to_vips, "fail": []}
                    ]
                },
                {
                    "try": email.application_accepted,
                    "fail": []
                }
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
