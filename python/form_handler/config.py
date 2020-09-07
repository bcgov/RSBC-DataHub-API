import os
from python.common.config import Config as BaseConfig


class Config(BaseConfig):
    WATCH_QUEUE                         = os.getenv('WATCH_QUEUE', 'DF.valid')
    HOLD_QUEUE                          = os.getenv('HOLD_QUEUE', 'DF.hold')

    DAYS_TO_DELAY_FOR_VIPS_DATA_ENTRY   = os.getenv('DAYS_TO_DELAY_FOR_VIPS_DATA_ENTRY', 3)
    HOURS_TO_HOLD_BEFORE_TRYING_VIPS    = os.getenv('HOURS_TO_HOLD_BEFORE_TRYING_VIPS', 4)

    VIPS_API_ROOT_URL                   = os.getenv('VIPS_API_ROOT_URL')
    VIPS_API_USERNAME                   = os.getenv('VIPS_API_USERNAME')
    VIPS_API_PASSWORD                   = os.getenv('VIPS_API_PASSWORD')

    # Common Services API for sending email
    COMM_SERV_AUTH_URL                  = os.getenv('COMM_SERV_AUTH_URL')
    COMM_SERV_API_ROOT_URL              = os.getenv('COMM_SERV_API_ROOT_URL')
    COMM_SERV_REALM                     = os.getenv('COMM_SERV_REALM')
    COMM_SERV_CLIENT_ID                 = os.getenv('COMM_SERV_CLIENT_ID')
    COMM_SERV_CLIENT_SECRET             = os.getenv('COMM_SERV_CLIENT_SECRET')

    ADMIN_EMAIL_ADDRESS                 = os.getenv('ADMIN_EMAIL_ADDRESS')
    REPLY_EMAIL_ADDRESS                 = os.getenv('REPLY_EMAIL_ADDRESS', 'do-not-reply@gov.bc.ca')

    # comma separated list of email addresses to receive a bcc of all outgoing emails
    BCC_EMAIL_ADDRESSES                 = os.getenv('ADMIN_EMAIL_ADDRESS')


