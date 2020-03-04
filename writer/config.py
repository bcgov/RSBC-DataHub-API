import os


basedir = os.path.abspath(os.path.dirname(__file__))

class Config():
    
    #RABBITMQ
    MQ_URL                  = os.getenv('MQ_URL', 'localhost')
    WRITE_WATCH_QUEUE       = os.getenv('WRITE_WATCH_QUEUE', 'ETK.valid')
    WRITE_FAIL_QUEUE        = os.getenv('WRITE_FAIL_QUEUE', 'ETK.fail-write')
    MQ_WRITER_USER          = os.getenv('MQ_WRITER_USER', 'jlonge')
    MQ_WRITER_PASS          = os.getenv('MQ_WRITER_PASS', '***REMOVED***')
    MQ_MESSAGE_ENCODE       = os.getenv('MQ_MESSAGE_ENCODE', 'utf-8')

    #DATABASE
    DB_HOST                 = os.getenv('DB_HOST')
    DB_NAME                 = os.getenv('DB_NAME')
    DB_USERNAME             = os.getenv('DB_USERNAME')
    DB_PASSWORD             = os.getenv('DB_PASSWORD')

    #THE ODBC DRIVER MUST BE INSTALLED IN THE CONTAINER
    ODBC_DRIVER             = os.getenv('ODBC_DRIVER', 'ODBC Driver 17 for SQL Server')

    MAPPER_CONFIG_FILENAME  = os.getenv('MAPPER_CONFIG_FILENAME', 'mapper.json')


