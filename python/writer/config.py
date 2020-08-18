import os
from python.common.config import Config as BaseConfig


class Config(BaseConfig):
    # RABBITMQ
    WATCH_QUEUE                 = os.getenv('WATCH_QUEUE', 'validated')
    FAIL_QUEUE                  = os.getenv('FAIL_QUEUE', 'ETK.fail-write')

    # BI DATABASE
    DB_HOST                     = os.getenv('DB_HOST')
    DB_NAME                     = os.getenv('DB_NAME')
    DB_USERNAME                 = os.getenv('DB_USERNAME')
    DB_PASSWORD                 = os.getenv('DB_PASSWORD')

    # THE ODBC DRIVER MUST BE INSTALLED IN THE CONTAINER
    ODBC_DRIVER                 = os.getenv('ODBC_DRIVER', 'ODBC Driver 17 for SQL Server')
    MAPPER_CONFIG_FILENAME      = os.getenv('MAPPER_CONFIG_FILENAME', 'python/writer/mapper.json')

    VIPS_API_ROOT_URL           = os.getenv('VIPS_API_ROOT_URL')
    VIPS_API_USERNAME           = os.getenv('VIPS_API_USERNAME')
    VIPS_API_PASSWORD           = os.getenv('VIPS_API_PASSWORD')

    # Common Services API for sending email
    COMM_SERV_AUTH_URL          = os.getenv('COMM_SERV_AUTH_URL')
    COMM_SERV_API_ROOT_URL      = os.getenv('COMM_SERV_API_ROOT_URL')
    COMM_SERV_REALM             = os.getenv('COMM_SERV_REALM')
    COMM_SERV_CLIENT_ID         = os.getenv('COMM_SERV_CLIENT_ID')
    COMM_SERV_CLIENT_SECRET     = os.getenv('COMM_SERV_CLIENT_SECRET')

    ADMIN_EMAIL_ADDRESS         = os.getenv('ADMIN_EMAIL_ADDRESS')
