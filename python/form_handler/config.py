import os
from python.common.config import Config as BaseConfig


class Config(BaseConfig):
    WATCH_QUEUE                         = os.getenv('WATCH_QUEUE', 'DF.valid')
    HOLD_QUEUE                          = os.getenv('HOLD_QUEUE', 'DF.hold')
    FAIL_QUEUE                          = os.getenv('FAIL_QUEUE', 'DF.fail')

    DAYS_TO_DELAY_FOR_VIPS_DATA_ENTRY   = os.getenv('DAYS_TO_DELAY_FOR_VIPS_DATA_ENTRY', '3')
    HOURS_TO_HOLD_BEFORE_TRYING_VIPS    = os.getenv('HOURS_TO_HOLD_BEFORE_TRYING_VIPS', '12')
    HOURS_TO_HOLD_BEFORE_DISCLOSURE     = os.getenv('HOURS_TO_HOLD_BEFORE_DISCLOSURE', '24')

    VIPS_API_ROOT_URL                   = os.getenv('VIPS_API_ROOT_URL')
    VIPS_API_USERNAME                   = os.getenv('VIPS_API_USERNAME')
    VIPS_API_PASSWORD                   = os.getenv('VIPS_API_PASSWORD')

    LINK_TO_PAYBC                       = os.getenv('LINK_TO_PAYBC', 'http://localhost')
    LINK_TO_SCHEDULE_FORM               = os.getenv('LINK_TO_SCHEDULE_FORM', 'http://localhost')
    LINK_TO_EVIDENCE_FORM               = os.getenv('LINK_TO_EVIDENCE_FORM', 'http://localhost')
    LINK_TO_APPLICATION_FORM            = os.getenv('LINK_TO_APPLICATION_FORM', 'http://localhost')

    LINK_TO_ICBC                        = os.getenv('LINK_TO_ICBC', 'http://localhost')

    LINK_TO_SERVICE_BC                  = os.getenv('LINK_TO_SERVICE_BC', 'http://localhost')

    LINK_TO_GET_DRIVING_RECORD          = os.getenv('LINK_TO_GET_DRIVING_RECORD', 'http://localhost')
