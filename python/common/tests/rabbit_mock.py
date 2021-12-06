import logging


class MockRabbitMQ:

    def __init__(self, config):
        pass

    def publish(self, queue_name: str, payload: bytes):
        logging.warning('queue: ' + queue_name)
        logging.warning('payload: ' + payload.decode('utf-8'))
        return True


class MockRabbitPublishFail:

    def __init__(self, config):
        pass

    def publish(self, queue_name: str, payload: bytes):
        logging.warning('queue: ' + queue_name)
        logging.warning('payload: ' + payload.decode('utf-8'))
        return False

