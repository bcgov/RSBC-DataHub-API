from python.form_handler.config import Config
import python.common.helper as helper
import python.form_handler.business as business
from python.common.rabbitmq import RabbitMQ
from python.common.message import decode_message
import logging
import logging.config
import json

logging.config.dictConfig(Config.LOGGING)


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
        # convert body (in bytes) to string
        message_dict = decode_message(body, self.config.ENCRYPT_KEY)

        logging.info("callback() invoked: {}".format(json.dumps(message_dict)))
        helper.middle_logic(helper.get_listeners(business.process_incoming_form(), message_dict['event_type']),
                            message=message_dict,
                            config=self.config,
                            writer=self.writer)

        # Regardless of whether the process above follows the happy path or not,
        # we need to acknowledge receipt of the message to RabbitMQ below. This
        # acknowledgement deletes it from the queue. The logic above
        # must have saved / handled the message before we get here.

        ch.basic_ack(delivery_tag=method.delivery_tag)


if __name__ == "__main__":
    Listener(
        Config(),
        RabbitMQ(Config()),
        RabbitMQ(Config())
    ).main()
