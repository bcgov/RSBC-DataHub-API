from config import Config
import logging
import pika

class RabbitMQ():


    def __init__(self, config ):
        self.maximumConnectionRetries = config.MAX_CONNECTION_RETRIES
        self.amqp_connection = self._getConnectionURL(config.INGEST_USER, config.INGEST_PASS, config.RABBITMQ_URL)
        self.connection = self._getConnection(self.amqp_connection)
        self.channel = self._getChannel(self.connection)
        logging.basicConfig(level=config.INGESTOR_LOG_LEVEL)

    def _getConnectionURL(self, user: str, passwd: str, host: str) -> str:
        return "amqp://{}:{}@{}:5672/%2F?connection_attempts=250&heartbeat=3600".format(user, passwd, host)


    def publish(self, queue_name: str, payload: str):

        logging.info('publish to: ' + queue_name )
        tries = self.maximumConnectionRetries 
        while tries > 0:
            tries -= 1

            try:
                self.channel.basic_publish(  
                    exchange='', 
                    routing_key=queue_name, 
                    body=payload,
                    properties=pika.BasicProperties(
                        delivery_mode = 2,
                        content_type='application/json'),
                    mandatory=True
                    )

                return True

            except Exception as error:
                logging.warning("Could not publish message to queue ... trying to reestablish the connection")
                self.connection = self._getConnection(self.amqp_connection)
                self.channel = self._getChannel(self.connection)
        
        return False


    def verifyOrCreate(self, queue_name: str):
       
        logging.info('verify or create: ' + queue_name)
        tries = self.maximumConnectionRetries 
        while tries > 0:
            tries -= 1

            try:
                self.channel.queue_declare(queue=queue_name, durable=True)
                logging.info('Confirmed, there is a queue called: ' + queue_name )
                return True

            except Exception as error:
                logging.warning("Could not declare queue ... trying to reestablish the connection")
                self.connection = self._getConnection(self.amqp_connection)
                self.channel = self._getChannel(self.connection)
        
        return False


    def _getConnection(self, connectionURL):
        parameters = pika.URLParameters(connectionURL)
        return pika.BlockingConnection(parameters)

    def _getChannel(self, connection):
        return connection.channel()
        