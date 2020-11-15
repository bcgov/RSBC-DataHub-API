import os
from python.common.config import Config as BaseConfig


class Config(BaseConfig):
    WATCH_QUEUE                         = os.getenv('WATCH_QUEUE', 'DF.valid')
    HOLD_QUEUE                          = os.getenv('HOLD_QUEUE', 'DF.hold')
    FAIL_QUEUE                          = os.getenv('FAIL_QUEUE', 'DF.fail')

    DAYS_TO_DELAY_FOR_VIPS_DATA_ENTRY   = os.getenv('DAYS_TO_DELAY_FOR_VIPS_DATA_ENTRY', '3')
    HOURS_TO_HOLD_BEFORE_TRYING_VIPS    = os.getenv('HOURS_TO_HOLD_BEFORE_TRYING_VIPS', '4')
    HOURS_TO_HOLD_BEFORE_DISCLOSURE     = os.getenv('HOURS_TO_HOLD_BEFORE_DISCLOSURE', '24')

    VIPS_API_ROOT_URL                   = os.getenv('VIPS_API_ROOT_URL')
    VIPS_API_USERNAME                   = os.getenv('VIPS_API_USERNAME')
    VIPS_API_PASSWORD                   = os.getenv('VIPS_API_PASSWORD')

    LINK_TO_PAYBC                       = os.getenv('LINK_TO_PAYBC', 'https://paytest.gov.bc.ca')
    LINK_TO_SCHEDULE_FORM               = os.getenv('LINK_TO_SCHEDULE_FORM',
                                        'https://forms2.qa.gov.bc.ca/forms/content?id=34F8F542261449CBA35F220B74ADC393')
    LINK_TO_EVIDENCE_FORM               = os.getenv('LINK_TO_EVIDENCE_FORM',
                                        'https://forms2.qa.gov.bc.ca/forms/content?id=C88D6641F78A4D5FBC383CC50E641CE6')
    LINK_TO_APPLICATION_FORM            = os.getenv('LINK_TO_APPLICATION_FORM',
                                        'https://forms2.qa.gov.bc.ca/forms/content?id=FC005E942B274061A110A2CFC42C1EA2')

    LINK_TO_ICBC                        = os.getenv('LINK_TO_ICBC',
            'https://www.icbc.com/driver-licensing/visit-dl-office/Pages/Book-a-knowledge-test-and-other-services.aspx')

    LINK_TO_SERVICE_BC                  = os.getenv('LINK_TO_SERVICE_BC',
                                                    'https://appointments.servicebc.gov.bc.ca/appointment')


