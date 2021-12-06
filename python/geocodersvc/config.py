import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    LOG_FORMAT                  = "%(asctime)s::%(levelname)s::%(name)s::%(message)s"
    LOG_LEVEL                   = os.environ.get('LOG_LEVEL', 'WARNING').upper()

    # OpenShift Environment (dev, test, prod)
    ENVIRONMENT                 = os.getenv('ENVIRONMENT', 'dev')

    # Flask requires a secret key for encryption tasks
    GEOCODE_SECRET_KEY          = os.getenv('GEOCODE_SECRET_KEY')
    
    # The Geocoder API Routes are protected with basic http authentication
    GEOCODE_BASIC_AUTH_USER     = os.getenv('GEOCODE_BASIC_AUTH_USER')
    GEOCODE_BASIC_AUTH_PASS     = os.getenv('GEOCODE_BASIC_AUTH_PASS')

    DATA_BC_API_URL             = os.getenv('DATA_BC_API_URL', 'https://geocoder.api.gov.bc.ca')
    DATA_BC_API_KEY             = os.getenv('DATA_BC_API_KEY')

    # Minimum acceptable score threshold from DataBC; if below
    # threshold, query will be sent to Google for processing
    MIN_CONFIDENCE_SCORE        = int(os.getenv('MIN_CONFIDENCE_SCORE', '55'))

    GOOGLE_FAIL_OVER_ENABLED    = os.getenv('GOOGLE_FAIL_OVER_ENABLED', 'FALSE')
    GOOGLE_API_ROOT_URL         = os.getenv('GOOGLE_API_ROOT_URL', 'https://maps.googleapis.com/maps/api/geocode/json')
    GOOGLE_API_KEY              = os.getenv('GOOGLE_API_KEY', 'not-implemented-at-this-time')


