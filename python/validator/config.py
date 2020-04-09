import os
from python.common.config import Config as BaseConfig


class Config(BaseConfig):
    WATCH_QUEUE                 = os.getenv('WATCH_QUEUE', 'ETK')
    VALID_QUEUE                 = os.getenv('VALID_QUEUE', 'ETK.valid')
    FAIL_QUEUE                  = os.getenv('FAIL_QUEUE', 'ETK.not-valid')
    SCHEMA_PATH                 = os.getenv('SCHEMA_PATH', 'python/validator/')
    SCHEMA_FILENAME             = os.getenv('SCHEMA_FILENAME', 'schemas.json')
    VALIDATOR_USER              = os.getenv('VALIDATOR_USER')
    VALIDATOR_PASS              = os.getenv('VALIDATOR_PASS')

