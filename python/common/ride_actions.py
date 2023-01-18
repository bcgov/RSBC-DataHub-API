import logging
import logging.config
import requests


def app_accepted_event(**args):
    logging.info("this is from ride function new app_accepted_event")
    logging.info(args)
    #TODO: Call RIDE API endpoint
    #TODO: For errors write to RabbitMQ
    return True, args

def disclosure_sent(**args):
    logging.info("this is from ride function disclosure_sent")
    logging.info(args)
    # TODO: Call RIDE API endpoint
    # TODO: For errors write to RabbitMQ
    return True, args

def evidence_submitted(**args):
    logging.info("this is from ride function evidence_submitted")
    logging.info(args)
    # TODO: Call RIDE API endpoint
    # TODO: For errors write to RabbitMQ
    return True, args

def payment_received(**args):
    logging.info("this is from ride function payment_received")
    logging.info(args)
    # TODO: Call RIDE API endpoint
    # TODO: For errors write to RabbitMQ
    return True, args

def review_scheduled(**args):
    logging.info("this is from ride function review_scheduled")
    logging.info(args)
    # TODO: Call RIDE API endpoint
    # TODO: For errors write to RabbitMQ
    return True, args