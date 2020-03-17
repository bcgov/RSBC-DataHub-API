from python.writer.config import Config
from python.writer.database import MsSQL
from python.writer.mapper import Mapper
import logging
import pika
import json

# This listener watches the RabbitMQ queue defined in the 
# Config.  When a message appears in the queue the Listener:
#  - invokes callback(),
#  - transforms the message using the Mapper class,
#  - finally passing a dict to the Database class for writing


class Listener:

    maximumConnectionRetries = 250  
    
    def __init__(self, config, database):
        url = self.getAmqpUrl(config)
        parameters = pika.URLParameters(url)
        self.connection = pika.BlockingConnection(parameters)
        self.config = config
        self.database = database
        logging.basicConfig(level=config.LOG_LEVEL)
        logging.warning('*** Writer: listener initiallized ***')

    def getAmqpUrl(self, config):
        return "amqp://{}:{}@{}:5672/%2F?connection_attempts=250&heartbeat=3600".format(
            config.MQ_WRITER_USER,
            config.MQ_WRITER_PASS, 
            config.RABBITMQ_URL
            )

    def main(self):
        channel = self.connection.channel()
        self._verifyOrCreate(channel, self.config.FAIL_QUEUE)
        channel.basic_qos(prefetch_count=1)
        channel.basic_consume(queue=self.config.WATCH_QUEUE, on_message_callback=self.callback)
        channel.start_consuming()
        logging.warning('*** Writer: listening for valid messages ***')

    def callback(self, ch, method, properties, body):
        # convert body (in bytes) to string 
        message = body.decode(self.config.RABBITMQ_MESSAGE_ENCODE)
        dictMessage = json.loads(message)

        # The Mapper is responsible for converting the message into a 
        # list of tables for insertion into a database.  Each table includes
        # data record(s) to be inserted.
        tablesForInsert = Mapper(self.config).convertToTables(dictMessage)

        # The database insert method is responsible for connecting to the 
        # database, adding records to one or more tables and closing the 
        # connection.  The database class can be extended to allow for
        # writing to different databases. For example, the syntax to insert 
        # records into a MSSQL database is slightly different than the 
        # syntax to used to insert records into a Postgress database
        result = self.database.insert(tablesForInsert)

        if result['isSuccessful']:
            # acknowledge that the message was written to the database
            # remove the message from RabbitMQs WRITE_WATCH_QUEUE
            ch.basic_ack(delivery_tag=method.delivery_tag)
        else:
            errorMessage = self._addErrorToMessage(dictMessage, result)
            jsonErrorMessage = json.dumps(errorMessage)
            
            if(self._publish(ch, self.config.FAIL_QUEUE, jsonErrorMessage )):
                ch.basic_ack(delivery_tag=method.delivery_tag)

    def _addErrorToMessage(self, message: dict, error: dict) -> dict:
        # We add 'errors' as a message attribute so as to keep a
        # history of events in case it fails repeatedly.  
        
        if 'errors' not in message:
            message['errors'] = []
        
        message['errors'].append(error)
            
        return message

    def _publish(self, channel, queue_name: str, message: str):
        tries = Listener.maximumConnectionRetries 
        while tries > 0:
            tries -= 1

            try:
                channel.basic_publish( exchange='', routing_key=queue_name, body=message, mandatory=True)
                return True

            except Exception as error:
                logging.warning("Could not write to queue: " + str(error))
        
        return False

    def _verifyOrCreate(self, channel, queue_name: str):
       
        logging.info('verify or create: ' + queue_name)
        tries = Listener.maximumConnectionRetries 
        while tries > 0:
            tries -= 1

            try:
                channel.queue_declare(queue=queue_name, durable=True)
                logging.info('Confirmed, there is a queue called: ' + queue_name )
                return True

            except Exception as error:
                logging.warning("Error: could not create " + queue_name )
                
        return False


if __name__ == "__main__":
    Listener( Config(), MsSQL( Config() ) ).main()
