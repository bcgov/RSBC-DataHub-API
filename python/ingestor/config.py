import os
from python.common.config import Config as BaseConfig

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(BaseConfig):
    FLASK_SECRET_KEY            = os.getenv('FLASK_SECRET_KEY')
    PARAMETERS_FILE             = os.getenv('PARAMETERS_FILE', 'parameters.json')

    VIPS_API_ROOT_URL           = os.getenv('VIPS_API_ROOT_URL')
    VIPS_API_USERNAME           = os.getenv('VIPS_API_USERNAME')
    VIPS_API_PASSWORD           = os.getenv('VIPS_API_PASSWORD')

