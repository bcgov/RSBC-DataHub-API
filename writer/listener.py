from config import Config
from database import MsSQL
from mapper import Mapper
import logging
import pika
import time
import json

# This listener watches the RabbitMQ queue defined in the 
# Config.  When a message appears in the queue the Listener
# envokes callback() and then passes the message to the
# Mapper class
class Listener():

    
    def __init__(self, config, database):
        url = self.getAmqpUrl(
            config.MQ_WRITER_USER, 
            config.MQ_WRITER_PASS, 
            config.MQ_URL
            )
        parameters = pika.URLParameters(url)
        self.connection = pika.BlockingConnection(parameters)
        self.config = config
        self.database = database
        logging.warning('*** Writer: listener initiallized ***')


    def getAmqpUrl(self, user: str, passwd: str, host: str):
        return "amqp://{}:{}@{}:5672/%2F?connection_attempts=250&heartbeat=3600".format(user, passwd, host)


    def main(self):
        channel = self.connection.channel()
        channel.basic_qos(prefetch_count=1)
        channel.basic_consume(queue=self.config.MQ_WATCH_QUEUE, on_message_callback=self.callback)
        channel.start_consuming()
        logging.warning('*** Writer: listening for valid messages ***')

    def callback(self, ch, method, properties, body):
        # convert body (in bytes) to string 
        message = body.decode(self.config.MQ_MESSAGE_ENCODE)
        dictMessage = json.loads(message)

        # The Mapper is responsible for converting the message into a 
        # list of tables for insertion into a database.  Each table includes
        # a header record (list of fields names) and a data record (list of
        # data to be inserted)
        tablesForInsert = Mapper(self.config).convertToTables(dictMessage)

        # The database insert method is responsible for connecting to the 
        # database, adding records to one or more tables and closing the 
        # connection.  The database class can be extended to allow for
        # different database syntax. For example, the syntax to insert 
        # records into a MSSQL database is slightly different than the 
        # syntax to used to insert records into a Postgress database
        self.database.insert(tablesForInsert)

        ch.basic_ack(delivery_tag=method.delivery_tag)

    
    
if __name__ == "__main__":
    Listener(Config(), MsSQL(Config())).main()


