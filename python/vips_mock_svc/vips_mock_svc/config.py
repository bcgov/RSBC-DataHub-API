import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    FLASK_SECRET_KEY                    = os.getenv('FLASK_SECRET_KEY')

    BASIC_AUTH_USER                     = os.getenv('FLASK_BASIC_AUTH_USER', 'user1')
    BASIC_AUTH_PASS                     = os.getenv('FLASK_BASIC_AUTH_PASS', 'secret1')
