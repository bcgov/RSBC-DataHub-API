from python.writer.config import Config
from python.writer.database import MsSQL
from python.writer.mapper import Mapper
from python.common.rabbitmq import RabbitMQ
from python.common.message import Message
import logging


class Listener:
    """
        This listener watches the RabbitMQ WATCH_QUEUE defined in the
        Config.  When a message appears in the queue the Listener:
         - invokes callback(),
         - transforms the message using the Mapper class,
         - finally passing a dict to the Database class for writing
    """
    
    def __init__(self, config, database, mapper, rabbit_writer, rabbit_listener, message):
        self.config = config
        self.database = database
        self.mapper = mapper
        self.listener = rabbit_listener
        self.writer = rabbit_writer
        self.message = message
        logging.basicConfig(level=config.LOG_LEVEL)
        logging.warning('*** writer initialized ***')

    def main(self):
        # start listening for messages on the WATCH_QUEUE
        # when a message arrives invoke the callback()
        self.listener.consume(self.config.WATCH_QUEUE, self.callback)

    def callback(self, ch, method, properties, body):
        logging.info('message received; callback invoked')

        # convert body (in bytes) to string
        message_dict = self.message.decode_message(body, self.config.ENCRYPT_KEY)

        # The Mapper is responsible for converting the message into a 
        # list of tables for insertion into a database.  Each table includes
        # data record(s) to be inserted.
        tables_for_insert = self.mapper.convert_to_tables(message_dict)

        # The database insert method is responsible for connecting to the 
        # database, adding records to one or more tables and closing the 
        # connection.
        result = self.database.insert(tables_for_insert)

        if result['isSuccessful']:
            # acknowledge that the message was written to the database
            # remove the message from RabbitMQs WRITE_WATCH_QUEUE
            ch.basic_ack(delivery_tag=method.delivery_tag)
        else:
            message_with_errors_appended = Message.add_error_to_message(message_dict, result)
            if self.writer.publish(
                    self.config.FAIL_QUEUE,
                    self.message.encode_message(message_with_errors_appended, self.config.ENCRYPT_KEY)):
                ch.basic_ack(delivery_tag=method.delivery_tag)


if __name__ == "__main__":
    Listener(
        Config(),
        MsSQL(Config()),
        Mapper(Config()),
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
