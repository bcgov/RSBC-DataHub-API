import logging
import pika


class RabbitMQ:

    def __init__(self, username, password, host_url, log_level = 'INFO', maximum_connection_retries = 250):
        self.maximumConnectionRetries = maximum_connection_retries
        self.amqp_connection = self._get_connection_url(username, password, host_url)
        self.connection = self._get_connection(self.amqp_connection)
        self.channel = self._get_channel(self.connection)
        logging.basicConfig(level=log_level)

    @staticmethod
    def _get_connection_url(user: str, password: str, host: str) -> str:
        return "amqp://{}:{}@{}:5672/%2F?connection_attempts=250&heartbeat=3600".format(
            user,
            password,
            host)

    def consume(self, queue_name: str, callback ):
        self.verify_or_create(queue_name)
        self.channel.basic_qos(prefetch_count=1)
        self.channel.basic_consume(queue=queue_name, on_message_callback=callback)
        self.channel.start_consuming()

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
                self.connection = self._get_connection(self.amqp_connection)
                self.channel = self._get_channel(self.connection)
        
        return False

    def verify_or_create(self, queue_name: str):
       
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