import os
from python.common.config import Config as BaseConfig

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(BaseConfig):
    FLASK_SECRET_KEY            = os.getenv('FLASK_SECRET_KEY')
    PARAMETERS_FILE             = os.getenv('PARAMETERS_FILE', 'parameters.json')

