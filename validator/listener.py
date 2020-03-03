from config import Config
from validator import Validate
import logging
import pika
import time
import json
from cerberus import Validator as Cerberus


class Listener():

    maximumConnectionRetries = 250
    
    def __init__(self, config, validator):
        url = self.getAmqpUrl(config.VALIDATOR_USER, config.VALIDATOR_PASS, config.RABBITMQ_URL)
        parameters = pika.URLParameters(url)
        self.connection = pika.BlockingConnection(parameters)
        self.validator = validator
        self.config = config
        logging.basicConfig(level=config.VALIDATOR_LOG_LEVEL)
        logging.warning('*** validator initialized  ***')

    def main(self):
        channel = self.connection.channel()
        self._verifyOrCreate(channel, self.config.RABBITMQ_VALID_QUEUE)
        self._verifyOrCreate(channel, self.config.RABBITMQ_FAIL_QUEUE)
        channel.basic_qos(prefetch_count=1)
        channel.basic_consume(queue=self.config.RABBITMQ_WATCH_QUEUE, on_message_callback=self.callback)
        channel.start_consuming()


    def callback(self, ch, method, properties, body):
        logging.warning('message received; callback invoked')
        # convert body (in bytes) to string 
        
        message = body.decode(self.config.RABBITMQ_MESSAGE_ENCODE)
        messageDict = json.loads(message)
        
        if(self.validator.validate(messageDict)):
            queue = self.config.RABBITMQ_VALID_QUEUE
        else:
            queue = self.config.RABBITMQ_FAIL_QUEUE

        logging.info("write to: " + queue)

        # only remove the message from the ingested queue if it has 
        # successfully been writen to a `valid` or `not-valid` queue
        if(self._publish(ch, queue, message )):
            ch.basic_ack(delivery_tag=method.delivery_tag)


    def getAmqpUrl(self, user: str, passwd: str, host: str):
        return "amqp://{}:{}@{}:5672/%2F?connection_attempts=250&heartbeat=3600".format(user, passwd, host)


    def _publish(self, channel, queue_name, message):
    
        tries = Listener.maximumConnectionRetries 
        while tries > 0:
            tries -= 1

            try:
                channel.basic_publish( exchange='', routing_key=queue_name, body=message, mandatory=True)
                return True

            except Exception as error:
                logging.warning("Could not publish message to queue ... trying to reestablish the connection")
        
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
    Listener(Config(),Validate(Config())).main()


