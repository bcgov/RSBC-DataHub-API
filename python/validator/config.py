import os
from python.common.config import Config as BaseConfig


class Config(BaseConfig):
    WATCH_QUEUE                 = os.getenv('WATCH_QUEUE', 'ingested')
    SCHEMA_PATH                 = os.getenv('SCHEMA_PATH', 'python/validator/')
    SCHEMA_FILENAME             = os.getenv('SCHEMA_FILENAME', 'schema.json')
