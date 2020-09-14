from python.common.config import Config as BaseConfig
import os


class Config(BaseConfig):
    PAYBC_FLASK_SECRET          = os.getenv('PAYBC_FLASK_SECRET')
    PAYBC_CLIENT_ID             = os.getenv('PAYBC_CLIENT_ID')
    PAYBC_CLIENT_SECRET         = os.getenv('PAYBC_CLIENT_SECRET')
    OAUTH2_USER                 = os.getenv('OAUTH2_USER', 'admin')

    VIPS_API_ROOT_URL           = os.getenv('VIPS_API_ROOT_URL')
    VIPS_API_USERNAME           = os.getenv('VIPS_API_USERNAME')
    VIPS_API_PASSWORD           = os.getenv('VIPS_API_PASSWORD')

    SCHEMA_PATH                 = os.getenv('SCHEMA_PATH', 'python/paybc_api/')
    SCHEMA_FILENAME             = os.getenv('SCHEMA_FILENAME', 'validation.json')

    ABSOLUTE_DB_PATH            = os.getenv('ABSOLUTE_DB_PATH', '/var/lib/sqlite')
    DB_NAME                     = os.getenv('DB_NAME', 'sqlite.db')
