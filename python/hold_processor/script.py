from python.hold_processor.config import Config
import requests
import logging
import json
import time

logging.basicConfig(level=Config.LOG_LEVEL)


def create_shovel(config):
    """
    Creates a shovel on RabbitMQ that transfers all messages from
    the source queue to the destination queue. After the messages
    are transferred, the shovel is deleted.
    """
    endpoint = get_endpoint(config)
    connection_string = get_connection_string(config)
    payload = get_payload(config, connection_string)

    logging.info('create endpoint: {}'.format(endpoint))
    logging.info('create payload: {}'.format(json.dumps(payload)))
    logging.info('create connection: {}'.format(connection_string))

    logging.info("waiting ...")
    time.sleep(30)

    try:
        response = requests.put(endpoint, json=payload, auth=(config.RABBITMQ_USER, config.RABBITMQ_PASS))
    except AssertionError as error:
        logging.warning('no response from the RabbitMQ API')
        return False, error

    logging.info('RabbitMQ API response: {}'.format(response.status_code))


def get_endpoint(config) -> str:
    return "/".join([
        'http:/',
        config.RABBITMQ_URL + ":15672",
        "api",
        "parameters",
        "shovel",
        "%2F",
        "hold-shoveler"])


def get_payload(config, connection_string) -> dict:
    return dict({
        "value": {
            "src-protocol": "amqp091",
            "src-uri": connection_string,
            "src-queue": config.SOURCE_QUEUE,
            "dest-protocol": "amqp091",
            "dest-uri": connection_string,
            "dest-queue": config.DESTINATION_QUEUE,
            "src-delete-after": "queue-length"
        }
    })


def get_connection_string(config):
    string = "amqp://{}:{}@{}:{}".format(
        config.RABBITMQ_USER,
        config.RABBITMQ_PASS,
        config.RABBITMQ_URL,
        config.RABBITMQ_PORT
    )
    logging.info(string)
    return string


if __name__ == "__main__":
    create_shovel(Config)
