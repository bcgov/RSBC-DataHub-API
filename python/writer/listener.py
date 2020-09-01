from python.writer.config import Config
from python.writer.database import write as database_writer
from python.common.rabbitmq import RabbitMQ
from python.common.message import decode_message, encode_message
import logging

logging.basicConfig(level=Config.LOG_LEVEL)


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
        logging.warning('*** writer initialized ***')

    def main(self):
        # start listening for messages on the WATCH_QUEUE
        # when a message arrives invoke the callback()
        self.listener.consume(self.config.WATCH_QUEUE, self.callback)

    def callback(self, ch, method, properties, body):
        logging.info('message received; callback invoked')

        # convert body (in bytes) to string
        message_dict = decode_message(body, self.config.ENCRYPT_KEY)

        is_success, args = database_writer(message=message_dict, config=Config)
        if not is_success:
            self.writer.publish(Config.FAIL_QUEUE, encode_message(message_dict, Config.ENCRYPT_KEY))

        # Regardless of whether the write above is successful we need to
        # acknowledge receipt of the message to RabbitMQ. This acknowledgement
        # deletes it from the queue so the logic above must have saved or
        # handled the message before we get here.

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
