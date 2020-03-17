from python.validator.config import Config
from python.validator.validator import Validate
from python.common.rabbitmq import RabbitMQ
import logging
import json

# This listener watches the RabbitMQ WATCH_QUEUE defined in the
# Config.  When a message appears in the queue the Listener:
#  - invokes callback(),
#  - determines whether the message is valid or not valid,
#  - writes the message to a valid or not valid queue

class Listener:

    def __init__(self, config, validator, rabbit_writer, rabbit_listener):
        self.validator = validator
        self.config = config
        self.writer = rabbit_writer
        self.listener = rabbit_listener

        logging.basicConfig(level=config.LOG_LEVEL)
        logging.warning('*** validator initialized  ***')

    def main(self):
        # start listening for messages on the WATCH_QUEUE
        # when a message arrives invoke the callback()
        self.listener.consume(self.config.WATCH_QUEUE, self.callback )


    def callback(self, ch, method, properties, body):
        logging.info('message received; callback invoked')

        # convert body (in bytes) to string
        message = body.decode(self.config.RABBITMQ_MESSAGE_ENCODE)
        message_dict = json.loads(message)

        self.writer.verify_or_create(self.config.VALID_QUEUE)
        self.writer.verify_or_create(self.config.FAIL_QUEUE)

        if self.validator.validate(message_dict):
            queue = self.config.VALID_QUEUE
        else:
            queue = self.config.FAIL_QUEUE

        logging.info("write to: " + queue)

        # only remove the message from the ingested queue if it has 
        # successfully been writen to a `valid` or `not-valid` queue
        if self.writer.publish(queue, message):
            ch.basic_ack(delivery_tag=method.delivery_tag)


if __name__ == "__main__":
    Listener(
        Config(),
        Validate(Config()),
        RabbitMQ(
            Config.VALIDATOR_USER,
            Config.VALIDATOR_PASS,
            Config.RABBITMQ_URL,
            Config.LOG_LEVEL,
            Config.MAX_CONNECTION_RETRIES),
        RabbitMQ(
            Config.VALIDATOR_USER,
            Config.VALIDATOR_PASS,
            Config.RABBITMQ_URL,
            Config.LOG_LEVEL,
            Config.MAX_CONNECTION_RETRIES)
    ).main()
