import requests
import logging
import json
import uuid
import calendar
from datetime import datetime, timedelta
from iso8601 import parse_date
from unicodedata import normalize
from python.common.config import Config
import base64

logging.basicConfig(level=Config.LOG_LEVEL)


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

    @staticmethod
    def get_max_review_date(service_date: datetime) -> datetime:
        """
        Most prohibition reviews must be
        """
        return service_date + timedelta(days=17)

    @staticmethod
    def amount_due(presentation_type: str):
        if presentation_type == "WRIT":
            return ProhibitionBase.WRITTEN_REVIEW_PRICE
        if presentation_type == "ORAL":
            return ProhibitionBase.ORAL_REVIEW_PRICE


class UnlicencedDriver(ProhibitionBase):
    WRITTEN_REVIEW_PRICE = 50
    MUST_APPLY_FOR_REVIEW_WITHIN_7_DAYS = False
    DRIVERS_LICENCE_MUST_BE_SEIZED_BEFORE_APPLICATION_ACCEPTED = False
    DAYS_TO_SCHEDULE_REVIEW = 30

    @staticmethod
    def get_max_review_date(service_date: datetime):
        """
        Over ride the base method. Set the maximum review date
        for Unlicenced Drivers have 30 days to schedule review
        """
        # TODO - replace datetime.now() with submitted application date
        #  otherwise the date returned won't be consistent.
        #  REMOVE BEFORE FLIGHT
        return datetime.now() + timedelta(days=UnlicencedDriver.DAYS_TO_SCHEDULE_REVIEW)

    @staticmethod
    def amount_due(presentation_type: str):
        return UnlicencedDriver.WRITTEN_REVIEW_PRICE


class ImmediateRoadside(ProhibitionBase):
    pass


class AdministrativeDriving(ProhibitionBase):
    pass
