import os
from python.common.config import Config as BaseConfig


class Config(BaseConfig):
    SOURCE_QUEUE        = os.getenv('SOURCE_QUEUE', 'DF.hold')
    DESTINATION_QUEUE   = os.getenv('DESTINATION_QUEUE', 'DF.validated')



