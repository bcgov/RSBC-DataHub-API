import logging
import logging.config
from datetime import datetime, timedelta
from python.common.config import Config
import re

logging.config.dictConfig(Config.LOGGING)


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
    DRIVERS_LICENCE_MUST_BE_SEIZED_BEFORE_APPLICATION_ACCEPTED = True
    CAN_APPLY_FOR_REVIEW_MORE_THAN_ONCE = False

    # We can't schedule a review immediately, we have to give time for
    # an applicant to receive disclosure and submit their evidence
    MIN_DAYS_FROM_SCHEDULING_TO_REVIEW = 4
    MIN_DAYS_FROM_SERVED_TO_REVIEW = 8
    MAX_DAYS_FROM_SERVED_TO_REVIEW = 14
    DAYS_TO_APPLY = 7
    DAYS_TO_PAY = DAYS_TO_APPLY + 1

    @staticmethod
    def is_okay_to_apply(date_served: datetime, today: datetime) -> bool:
        """
        IRPs and ADPs can only be appealed within 7 days after a driver receives their
        prohibition.
        """
        if (today.date() - date_served.date()).days <= ProhibitionBase.DAYS_TO_APPLY:
            return True
        return False

    @staticmethod
    def is_okay_to_pay(date_served: datetime, today: datetime) -> bool:
        """
        IRPs and ADPs have only 8 days to pay for their prohibition review
        after a driver receives their prohibition.
        """
        if (today.date() - date_served.date()).days <= ProhibitionBase.DAYS_TO_PAY:
            return True
        return False

    @staticmethod
    def get_deadline_date_string(date_served: datetime) -> str:
        """
        IRPs and ADPs have 7 days to apply. Returns deadline date string
        in the format:  September 7, 2020
        """
        deadline_days = ProhibitionBase.DAYS_TO_APPLY + 1
        return (date_served.date() + timedelta(days=deadline_days)).strftime("%B %-d, %Y")

    @staticmethod
    def get_min_max_review_dates(service_date: datetime, today: datetime) -> tuple:
        """
        IRP and ADP prohibition reviews must be scheduled within
        a 7 to 14 window from the date of service.
        """
        earliest_possible_date = today + timedelta(
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
    MIN_DAYS_FROM_SCHEDULING_TO_REVIEW = 8
    DAYS_FROM_MIN_REVIEW_DATE_TO_MAX = 6
    DRIVERS_LICENCE_MUST_BE_SEIZED_BEFORE_APPLICATION_ACCEPTED = False
    CAN_APPLY_FOR_REVIEW_MORE_THAN_ONCE = True

    @staticmethod
    def is_okay_to_apply(date_served: datetime, today: datetime) -> bool:
        """
        UL Reviews are not restricted.  Applicants can apply anytime.
        """
        return True

    @staticmethod
    def is_okay_to_pay(date_served: datetime, today: datetime) -> bool:
        """
        UL Reviews are not restricted.  Applicants can pay anytime.
        """
        return True

    @staticmethod
    def get_min_max_review_dates(service_date: datetime, today: datetime) -> tuple:
        """
        Over ride the base method. Set the maximum review date
        for ULs. Drivers have 14 days from today to schedule a
        review
        """
        min_date = today + timedelta(days=UnlicencedDriver.MIN_DAYS_FROM_SCHEDULING_TO_REVIEW)
        max_date = min_date + timedelta(days=UnlicencedDriver.DAYS_FROM_MIN_REVIEW_DATE_TO_MAX)
        return min_date, max_date

    @staticmethod
    def amount_due(presentation_type: str):
        return UnlicencedDriver.WRITTEN_REVIEW_PRICE

    @staticmethod
    def type_verbose() -> str:
        return "Unlicensed driver prohibition"

    @staticmethod
    def get_deadline_date_string(date_served: datetime) -> str:
        """
        ULs have no deadline to apply. This method should not be called by ULs.
        """
        return "UL's have no deadline date"


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
            if re.match(r"^(IRP90.*|IRP30.*)", vips_data['originalCause']) is not None:
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
