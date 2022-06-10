import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    LOG_LEVEL                           = os.environ.get('LOG_LEVEL', 'WARNING').upper()
    FLASK_SECRET_KEY                    = os.getenv('FLASK_SECRET_KEY')
    ICBC_API_USERNAME                   = os.getenv('ICBC_API_USERNAME')
    ICBC_API_PASSWORD                   = os.getenv('ICBC_API_PASSWORD')


