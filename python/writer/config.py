import os
from python.common.config import Config as BaseConfig


class Config(BaseConfig):
    # RABBITMQ
    WATCH_QUEUE                 = os.getenv('WATCH_QUEUE', 'ETK.valid')
    FAIL_QUEUE                  = os.getenv('FAIL_QUEUE', 'ETK.fail-write')

    # BI DATABASE
    DB_HOST                     = os.getenv('DB_HOST')
    DB_NAME                     = os.getenv('DB_NAME')
    DB_USERNAME                 = os.getenv('DB_USERNAME')
    DB_PASSWORD                 = os.getenv('DB_PASSWORD')

    # GEOCODER
    GEOCODER_API_URI            = os.getenv('GEOCODER_API_URI')
    GEOCODE_BASIC_AUTH_USER     = os.getenv('GEOCODE_BASIC_AUTH_USER')
    GEOCODE_BASIC_AUTH_PASS     = os.getenv('GEOCODE_BASIC_AUTH_PASS')

    # THE ODBC DRIVER MUST BE INSTALLED IN THE CONTAINER
    ODBC_DRIVER                 = os.getenv('ODBC_DRIVER', 'ODBC Driver 17 for SQL Server')
    MAPPER_CONFIG_FILENAME      = os.getenv('MAPPER_CONFIG_FILENAME', 'python/writer/mapper.json')
