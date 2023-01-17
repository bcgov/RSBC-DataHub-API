import logging
import logging.config
import requests


def app_accepted_event(**args):
    logging.info("this is from ride function")
    logging.info(args)