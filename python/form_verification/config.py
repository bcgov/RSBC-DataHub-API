import os
from python.common.config import Config as BaseConfig


class Config(BaseConfig):
    WATCH_QUEUE                         = os.getenv('WATCH_QUEUE', 'DF.valid')
    WRITE_QUEUE                         = os.getenv('WRITE_QUEUE', 'validated')
    VIPS_API_USER                       = os.getenv('VIPS_API_USER')
    VIPS_API_PASS                       = os.getenv('VIPS_API_PASS')
    VIPS_API_ROOT_URI                   = os.getenv('VIPS_API_ROOT_URI')
    DAYS_TO_DELAY_FOR_VIPS_DATA_ENTRY   = os.getenv('DAYS_TO_DELAY_FOR_VIPS_DATA_ENTRY', 3)

