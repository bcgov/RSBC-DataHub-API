import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    RABBITMQ_URL                = os.getenv('RABBITMQ_URL', 'localhost')
    RABBITMQ_EXCHANGE           = os.getenv('RABBITMQ_EXCHANGE', '')
    MAX_CONNECTION_RETRIES      = os.getenv('MAX_CONNECTION_RETRIES', 25)
    RETRY_DELAY                 = os.getenv('RETRY_DELAY', 30)
    LOG_LEVEL                   = os.environ.get('LOG_LEVEL', 'INFO').upper()
    RABBITMQ_MESSAGE_ENCODE     = os.getenv('RABBITMQ_MESSAGE_ENCODE', 'utf-8')
    ENCRYPT_KEY                 = os.getenv('ENCRYPT_KEY')



