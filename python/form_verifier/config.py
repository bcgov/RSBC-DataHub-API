import os
from python.common.config import Config as BaseConfig


class Config(BaseConfig):
    WATCH_QUEUE                         = os.getenv('WATCH_QUEUE', 'DF.valid')
    WRITE_QUEUE                         = os.getenv('WRITE_QUEUE', 'validated')
    VIPS_API_USERNAME                   = os.getenv('VIPS_API_USERNAME')
    VIPS_API_PASSWORD                   = os.getenv('VIPS_API_PASSWORD')
    VIPS_API_ROOT_URL                   = os.getenv('VIPS_API_ROOT_URL')
    DAYS_TO_DELAY_FOR_VIPS_DATA_ENTRY   = os.getenv('DAYS_TO_DELAY_FOR_VIPS_DATA_ENTRY', 3)

