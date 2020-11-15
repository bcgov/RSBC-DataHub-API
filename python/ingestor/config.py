import os
from python.common.config import Config as BaseConfig

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(BaseConfig):
    FLASK_SECRET_KEY                    = os.getenv('FLASK_SECRET_KEY')
    PARAMETERS_FILE                     = os.getenv('PARAMETERS_FILE', 'parameters.json')

    # Routes are protected with         basic http authentication
    FLASK_BASIC_AUTH_USER               = os.getenv('FLASK_BASIC_AUTH_USER')
    FLASK_BASIC_AUTH_PASS               = os.getenv('FLASK_BASIC_AUTH_PASS')

    VIPS_API_ROOT_URL                   = os.getenv('VIPS_API_ROOT_URL')
    VIPS_API_USERNAME                   = os.getenv('VIPS_API_USERNAME')
    VIPS_API_PASSWORD                   = os.getenv('VIPS_API_PASSWORD')

    MAX_FORM_SUBMISSION_BYTES           = int(os.getenv('MAX_FORM_SUBMISSION_BYTES', '100000'))

    HOURS_BEFORE_REVIEW_EVIDENCE_DUE    = os.getenv('HOURS_BEFORE_REVIEW_EVIDENCE_DUE', '48')

    # When an applicant is scheduling a review. Business rules state they must be offered a
    # minimum of 3 different review days.  If fewer review days offered, expand the schedule from
    # 7 to 10 days.
    MIN_REVIEW_DAYS_OFFERED             = int(os.getenv('MIN_REVIEW_DAYS_OFFERED', '3'))
    ADDITIONAL_DAYS_TO_QUERY            = int(os.getenv('ADDITIONAL_DAYS_TO_QUERY', '3'))


