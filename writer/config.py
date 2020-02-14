import os


basedir = os.path.abspath(os.path.dirname(__file__))

class Config():
    
    #RABBITMQ
    MQ_URL                  = os.getenv('RABBITMQ_URL', 'localhost')
    MQ_WATCH_QUEUE          = os.getenv('RABBITMQ_WATCH_QUEUE', 'ETK.valid')
    MQ_WRITER_USER          = os.getenv('VALIDATOR_USER', 'jlonge')
    MQ_WRITER_PASS          = os.getenv('VALIDATOR_PASS', '***REMOVED***')
    MQ_MESSAGE_ENCODE       = os.getenv('MQ_MESSAGE_ENCODE', 'utf-8')

    #DATABASE
    DB_HOST                 = os.getenv('DB_HOST', 'clockwork.idir.bcgov')
    DB_NAME                 = os.getenv('DB_NAME', 'rsbcodw')
    DB_SCHEMA               = os.getenv('DB_SCHEMA', 'rsi')
    DB_USERNAME             = os.getenv('DB_USERNAME', 'rsbcdataapi')
    DB_PASSWORD             = os.getenv('DB_PASSWORD', 'secret')

    MAPPER_CONFIG_FILENAME  = os.getenv('MAPPER_CONFIG_FILENAME', 'mapper.json')


