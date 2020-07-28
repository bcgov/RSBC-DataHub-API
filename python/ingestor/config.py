import os
from python.common.config import Config as BaseConfig

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(BaseConfig):
    SECRET_KEY                  = os.getenv('SECRET_KEY')
    PARAMETERS_FILE             = os.getenv('PARAMETERS_FILE', 'parameters.json')
    INGEST_USER                 = os.getenv('INGEST_USER')
    INGEST_PASS                 = os.getenv('INGEST_PASS')

