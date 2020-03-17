import os
from common.config import Config as BaseConfig

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(BaseConfig):
    SECRET_KEY                  = os.getenv('SECRET_KEY')
    WRITE_QUEUE                 = os.getenv('WRITE_QUEUE', 'ETK')
    INGEST_USER                 = os.getenv('INGEST_USER')
    INGEST_PASS                 = os.getenv('INGEST_PASS')

