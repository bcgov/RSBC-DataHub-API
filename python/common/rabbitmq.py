import logging
import pika
import pika.exceptions
import pika.adapters.utils.connection_workflow as workflow


class RabbitMQ:

    MaximumTriesAfterError = 5

    def __init__(self, username, password, host_url, log_level, retries=5, retry_delay=30):
        self.amqp_connection = self._get_connection_url(username, password, host_url, retries, retry_delay)
        self.connection = self._get_connection(self.amqp_connection)
        self.channel = self._get_channel(self.connection)
        logging.basicConfig(level=log_level)

    @staticmethod
    def _get_connection_url(user: str, password: str, host: str, retries: int, retry_delay: int) -> str:
        string = "amqp://{}:{}@{}:5672/%2F?connection_attempts={}&retry_delay={}".format(
            user,
            password,
            host,
            retries,
            retry_delay
        )
        logging.debug(string)
        return string

    def consume(self, queue_name: str, callback):
        self._verify_or_create(queue_name)
        self.channel.basic_qos(prefetch_count=1)
        self.channel.basic_consume(queue=queue_name, on_message_callback=callback)
        try:
            self.channel.start_consuming()
        except workflow.AMQPConnectorSocketConnectError as error:
            logging.info('SocketConnectionError - expected')
        except workflow.AMQPConnector as error:
            logging.info('AMQPConnector error - expected')

    def publish(self, queue_name: str, payload: bytes):
        logging.info('publish to: ' + queue_name)
        self._refresh_connection(queue_name)
        for tries in range(RabbitMQ.MaximumTriesAfterError):
            try:
                self.channel.basic_publish(  
                    exchange='', 
                    routing_key=queue_name, 
                    body=payload,
                    properties=pika.BasicProperties(delivery_mode=2, content_type='application/json'),
                    mandatory=True)
                return True

            except Exception as error:
                logging.warning("Could not publish message to queue ... trying to reestablish the connection")
                self._refresh_connection(queue_name)
        
        return False

    def _refresh_connection(self, queue_name):
        self.connection = self._get_connection(self.amqp_connection)
        self.channel = self._get_channel(self.connection)
        self.channel.queue_declare(queue=queue_name, durable=True)

    def _verify_or_create(self, queue_name: str):
       
        logging.info('verify or create: ' + queue_name)
        for tries in range(RabbitMQ.MaximumTriesAfterError):
            try:
                self.channel.queue_declare(queue=queue_name, durable=True)
                logging.info('Confirmed, there is a queue called: ' + queue_name)
                return True

            except Exception as error:
                logging.warning("Could not declare queue ... trying to reestablish the connection")
                self.connection = self._get_connection(self.amqp_connection)
                self.channel = self._get_channel(self.connection)
        
        return False

    @staticmethod
    def _get_connection(connection_url):
        logging.info('getting connection to RabbitMQ')
        parameters = pika.URLParameters(connection_url)
        return pika.BlockingConnection(parameters)

    @staticmethod
    def _get_channel(connection):
        logging.info('getting channel to RabbitMQ')
        return connection.channel()
