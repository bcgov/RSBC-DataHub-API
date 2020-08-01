import os
from python.common.config import Config as BaseConfig


class Config(BaseConfig):
    # RABBITMQ
    WATCH_QUEUE                 = os.getenv('WATCH_QUEUE', 'validated')
    FAIL_QUEUE                  = os.getenv('FAIL_QUEUE', 'ETK.fail-write')

    # DATABASE
    DB_HOST                     = os.getenv('DB_HOST')
    DB_NAME                     = os.getenv('DB_NAME')
    DB_USERNAME                 = os.getenv('DB_USERNAME')
    DB_PASSWORD                 = os.getenv('DB_PASSWORD')

    # THE ODBC DRIVER MUST BE INSTALLED IN THE CONTAINER
    ODBC_DRIVER                 = os.getenv('ODBC_DRIVER', 'ODBC Driver 17 for SQL Server')
    MAPPER_CONFIG_FILENAME      = os.getenv('MAPPER_CONFIG_FILENAME', 'python/writer/mapper.json')
