import os


basedir = os.path.abspath(os.path.dirname(__file__))

class Config():

    RABBITMQ_URL                = os.getenv('RABBITMQ_URL', 'localhost')
    RABBITMQ_WATCH_QUEUE        = os.getenv('RABBITMQ_WATCH_QUEUE', 'ingested')
    RABBITMQ_MISC_ERROR_QUEUE   = os.getenv('RABBITMQ_VALID_QUEUE', 'misc.error')
    RABBITMQ_MESSAGE_ENCODE     = os.getenv('RABBITMQ_MESSAGE_ENCODE', 'utf-8')

    SCHEMA_FILENAME             = os.getenv('SCHEMA_FILENAME', 'schemas.json')

    VALIDATOR_USER              = os.getenv('VALIDATOR_USER')
    VALIDATOR_PASS              = os.getenv('VALIDATOR_PASS')

    # The validator automatically creates destination valid and not valid queues
    # as needed.  The destination queues follow the format 'ETK.valid' and 
    # 'ETK.not-valid' where 'ETK' is taken from the 'event_source' attribute in 
    # the message but can be configured to any message attribute by overriding 
    # the 'MESSAGE_QUEUE_ATTRIBUTE' variable below.
    MESSAGE_QUEUE_ATTRIBUTE     = os.getenv('MESSAGE_QUEUE_ATTRIBUTE', 'event_source')

