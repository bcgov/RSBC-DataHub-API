from config import Config
from validator import Validate
import logging
import pika
import time
import json
from cerberus import Validator as Cerberus


class Listener():

    maximumConnectionRetries = 5
    
    def __init__(self, config, validator):
        url = self.getAmqpUrl(config.VALIDATOR_USER, config.VALIDATOR_PASS, config.RABBITMQ_URL)
        parameters = pika.URLParameters(url)
        self.connection = pika.BlockingConnection(parameters)
        self.validator = validator
        self.availableQueues = []
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
        messageDict = json.loads(message)
        
        queue = self._getWriteQueue(self.validator.validate(messageDict),messageDict)
        logging.warning("write to: " + queue)

        # only remove the message from the ingested queue if
        # if it's successfully been writen to another queue
        if(self._publish(ch, queue, message )):
            ch.basic_ack(delivery_tag=method.delivery_tag)


    def getAmqpUrl(self, user: str, passwd: str, host: str):
        return "amqp://{}:{}@{}:5672/%2F?connection_attempts=250&heartbeat=3600".format(user, passwd, host)


    def _publish(self, channel, queue_name, message):
        self._createQueueIfNotExists(channel, self.availableQueues, queue_name)
        tries = Listener.maximumConnectionRetries 
        while tries > 0:
            tries -= 1;

            try:
                channel.basic_publish( exchange='', routing_key=queue_name, body=message)
                return True

            except Exception as error:
                logging.warning(error)
        
        return False
        

    def _getWriteQueue(self, isValid: bool, message: dict):

        if 'event_type' not in message:
            # if the message_type attribute doesn't exist in the
            # message, write the message to a miscelllaneous error queue
            return Config.RABBITMQ_MISC_ERROR_QUEUE

        # otherwise write the message to an event-type specific queue
        if(isValid):
            return message['event_type'] + ".valid"
        else:
            return message['event_type'] + ".not-valid"


    def _createQueueIfNotExists(self, channel, queuesAlreadyDeclared, currentQueue):
        if currentQueue not in queuesAlreadyDeclared:
            logging.warning('creating a new queue: ' + currentQueue)
            channel.queue_declare(queue=currentQueue, durable=True)
            self.availableQueues.append(currentQueue)

        return

        

        

       

        
if __name__ == "__main__":
    Listener(Config(),Validate(Config())).main()


