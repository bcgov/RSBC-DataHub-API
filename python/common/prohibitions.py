import logging
from datetime import datetime, timedelta
from python.common.config import Config
from python.common.helper import localize_timezone
import pytz
import re

logging.basicConfig(level=Config.LOG_LEVEL, format=Config.LOG_FORMAT)


def prohibition_factory(prohibition_type: str):
    if prohibition_type == "UL":
        return UnlicencedDriver()
    if prohibition_type == "IRP":
        return ImmediateRoadside()
    if prohibition_type == "ADP":
        return AdministrativeDriving()
    logging.critical('prohibition_type not known')
    return None


class ProhibitionBase:
    WRITTEN_REVIEW_PRICE = 100
    ORAL_REVIEW_PRICE = 200
    MUST_APPLY_FOR_REVIEW_WITHIN_7_DAYS = True
    DRIVERS_LICENCE_MUST_BE_SEIZED_BEFORE_APPLICATION_ACCEPTED = True

    # We can't schedule a review immediately, we have to give time for
    # an applicant to receive disclosure and submit their evidence
    MIN_DAYS_FROM_SCHEDULING_TO_REVIEW = 4
    MIN_DAYS_FROM_SERVED_TO_REVIEW = 7
    MAX_DAYS_FROM_SERVED_TO_REVIEW = 16

    @staticmethod
    def get_min_max_review_dates(service_date: datetime, today=datetime.now()) -> tuple:
        """
        IRP and ADP prohibition reviews must be scheduled within
        a 7 to 14 window from the date of service.
        """
        tz = pytz.timezone('America/Vancouver')
        earliest_possible_date = today.astimezone(tz) + timedelta(
            days=ProhibitionBase.MIN_DAYS_FROM_SCHEDULING_TO_REVIEW)
        legislated_minimum = service_date + timedelta(days=ProhibitionBase.MIN_DAYS_FROM_SERVED_TO_REVIEW)
        # The earliest possible review date is the greater of the
        # legislated minimum date and the earliest possible date
        if earliest_possible_date > legislated_minimum:
            legislated_minimum = earliest_possible_date
        legislated_maximum = service_date + timedelta(days=ProhibitionBase.MAX_DAYS_FROM_SERVED_TO_REVIEW)
        if earliest_possible_date > legislated_maximum:
            legislated_maximum = earliest_possible_date
        return legislated_minimum, legislated_maximum

    @staticmethod
    def amount_due(presentation_type: str):
        if presentation_type == "WRIT":
            return ProhibitionBase.WRITTEN_REVIEW_PRICE
        if presentation_type == "ORAL":
            return ProhibitionBase.ORAL_REVIEW_PRICE

    @staticmethod
    def type_verbose() -> str:
        pass

    @staticmethod
    def is_eligible_for_oral_review(vips_data: dict):
        # Unlicenced Driving Prohibitions are never eligible for oral reviews
        return False


class UnlicencedDriver(ProhibitionBase):
    WRITTEN_REVIEW_PRICE = 50
    MUST_APPLY_FOR_REVIEW_WITHIN_7_DAYS = False
    DRIVERS_LICENCE_MUST_BE_SEIZED_BEFORE_APPLICATION_ACCEPTED = False

    @staticmethod
    def get_min_max_review_dates(service_date: datetime, today=datetime.now()) -> tuple:
        """
        Over ride the base method. Set the maximum review date
        for Unlicenced Drivers have 14 days from today to schedule a
        review
        """
        min_date = localize_timezone(today) + timedelta(days=UnlicencedDriver.MIN_DAYS_FROM_SCHEDULING_TO_REVIEW)
        max_date = localize_timezone(today) + timedelta(days=UnlicencedDriver.MAX_DAYS_FROM_SERVED_TO_REVIEW)
        return min_date, max_date

    @staticmethod
    def amount_due(presentation_type: str):
        return UnlicencedDriver.WRITTEN_REVIEW_PRICE

    @staticmethod
    def type_verbose() -> str:
        return "Unlicensed driver prohibition"


class ImmediateRoadside(ProhibitionBase):

    @staticmethod
    def type_verbose() -> str:
        return "Immediate roadside prohibition"

    @staticmethod
    def is_eligible_for_oral_review(vips_data: dict):
        """
        Only 30 and 90-day IRP Prohibitions are eligible for oral reviews
        """
        if 'originalCause' in vips_data:
            if re.match(r"^(IRP90.|IRP30.)", vips_data['originalCause']) is not None:
                return True
        return False


class AdministrativeDriving(ProhibitionBase):

    @staticmethod
    def type_verbose() -> str:
        return "Administrative driving prohibition"

    @staticmethod
    def is_eligible_for_oral_review(vips_data: dict):
        # Administrative Driving Prohibitions are always eligible for oral reviews
        return True
