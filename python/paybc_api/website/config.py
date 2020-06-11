import os


class Config:
    PAYBC_FLASK_SECRET = os.getenv('PAYBC_FLASK_SECRET')
    PAYBC_CLIENT_ID = os.getenv('PAYBC_CLIENT_ID')
    PAYBC_CLIENT_SECRET = os.getenv('PAYBC_CLIENT_SECRET')
    OAUTH2_USER = os.getenv('OAUTH2_USER', 'admin')

