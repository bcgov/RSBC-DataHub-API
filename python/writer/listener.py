from python.writer.config import Config
import python.common.helper as helper
import python.writer.business as business
from python.common.rabbitmq import RabbitMQ
from python.common.message import decode_message, encode_message
import logging

logging.basicConfig(level=Config.LOG_LEVEL, format=Config.LOG_FORMAT)


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

        helper.middle_logic(helper.get_listeners(business.process_ekt_events(), message_dict['event_type']),
                            message=message_dict,
                            config=self.config,
                            writer=self.writer)

        # Regardless of whether the write above is successful we need to
        # acknowledge receipt of the message to RabbitMQ. This acknowledgement
        # deletes it from the queue so the logic above must have saved or
        # handled the message before we get here.

        ch.basic_ack(delivery_tag=method.delivery_tag)


if __name__ == "__main__":
    Listener(
        Config(),
        RabbitMQ(Config()),
        RabbitMQ(Config())
    ).main()
