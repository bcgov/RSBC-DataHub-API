import os


basedir = os.path.abspath(os.path.dirname(__file__))

class Config():
    SECRET_KEY              = os.getenv('SECRET_KEY', 'my_precious_secret_key')
    
    RABBITMQ_URL            = os.getenv('RABBITMQ_URL', 'localhost')
    RABBITMQ_EXCHANGE       = os.getenv('RABBITMQ_EXCHANGE', '')
    RABBITMQ_QUEUE          = os.getenv('RABBITMQ_QUEUE', 'ETK')
    MAX_CONNECTION_RETRIES  = os.getenv('MAX_CONNECTION_RETRIES', 250 )

    INGEST_USER             = os.getenv('INGEST_USER')
    INGEST_PASS             = os.getenv('INGEST_PASS')

    INGESTOR_LOG_LEVEL      = os.environ.get('INGESTOR_LOG_LEVEL','INFO').upper()
