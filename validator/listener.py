from config import Config
from validator import Validate
import logging
import pika
import time
import json
from cerberus import Validator as Cerberus


class Listener():

    
    def __init__(self, config, validator):
        url = self.getAmqpUrl(config.VALIDATOR_USER, config.VALIDATOR_PASS, config.RABBITMQ_URL)
        parameters = pika.URLParameters(url)
        self.connection = pika.BlockingConnection(parameters)
        self.validator = validator
        logging.warning('*** validator initialized  ***')

    def main(self):
        channel = self.connection.channel()
        channel.basic_qos(prefetch_count=1)
        channel.basic_consume(queue=Config.RABBITMQ_WATCH_QUEUE, on_message_callback=self.callback)
        channel.start_consuming()
        logging.warning('*** validator listening  ***')


    def callback(self, ch, method, properties, body):
        # convert body (in bytes) to string 
        message = body.decode(Config.RABBITMQ_MESSAGE_ENCODE)
        
        ch.basic_ack(delivery_tag=method.delivery_tag)
        if(self.validator.validate(json.loads(message))):
            self._publish(ch, Config.RABBITMQ_VALID_QUEUE, message )
        else:
            self._publish(ch, Config.RABBITMQ_FAIL_QUEUE, message )


    def getAmqpUrl(self, user: str, passwd: str, host: str):
        return "amqp://{}:{}@{}:5672/%2F?connection_attempts=250&heartbeat=3600".format(user, passwd, host)


    def _publish(self, channel, queue_name, message):
        channel.basic_publish(exchange='', routing_key=queue_name, body=message)

    
if __name__ == "__main__":
    Listener(Config(),Validate(Config())).main()


