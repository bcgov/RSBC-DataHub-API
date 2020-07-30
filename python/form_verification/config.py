import os
from python.common.config import Config as BaseConfig


class Config(BaseConfig):
    WATCH_QUEUE                         = os.getenv('WATCH_QUEUE', 'DF.valid')
    WRITE_QUEUE                         = os.getenv('WRITE_QUEUE', 'validated')
    VIPS_API_ROOT_URI                   = os.getenv('VIPS_API_ROOT_URI')
    RABBITMQ_USER                       = os.getenv('RABBITMQ_USER')
    RABBITMQ_PASS                       = os.getenv('RABBITMQ_PASS')
    DAYS_TO_DELAY_FOR_VIPS_DATA_ENTRY   = os.getenv('DAYS_TO_DELAY_FOR_VIPS_DATA_ENTRY', 3)

