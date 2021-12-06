from python.validator.config import Config
from python.validator.validate import Validate
from python.common.rabbitmq import RabbitMQ
from python.common.message import encode_message, decode_message, add_error_to_message
import logging
import logging.config

logging.config.dictConfig(Config.LOGGING)


class Listener:
    """
        This listener watches the RabbitMQ WATCH_QUEUE defined in the
        Config.  When a message appears in the queue the Listener:
         - invokes callback(),
         - determines whether the message is valid or not valid,
         - writes the message to a valid or not valid queue
    """
    def __init__(self, config, validator, rabbit_writer, rabbit_listener):
        self.validator = validator
        self.config = config
        self.writer = rabbit_writer
        self.listener = rabbit_listener
        logging.warning('*** validator initialized  ***')

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

        result = self.validator.validate(message_dict)
        logging.info("write to: " + result['queue'])
        if result['isSuccess']:
            # Validation SUCCESSFUL
            if self.writer.publish(result['queue'], encode_message(message_dict, self.config.ENCRYPT_KEY)):
                ch.basic_ack(delivery_tag=method.delivery_tag)
        else:
            # Validation FAILED
            message_with_errors = add_error_to_message(message_dict, result)
            if self.writer.publish(
                    result['queue'], encode_message(message_with_errors, self.config.ENCRYPT_KEY)):
                ch.basic_ack(delivery_tag=method.delivery_tag)


if __name__ == "__main__":
    Listener(
        Config(),
        Validate(Config()),
        RabbitMQ(Config()),
        RabbitMQ(Config())
    ).main()
