import logging
import logging.config


def has_not_applied_before_evidence(**args) -> tuple:
    error = 'You must apply before you can submit evidence.'
    logging.info(error)
    args['error_string'] = error
    return True, args


def has_not_paid_before_evidence(**args) -> tuple:
    error = 'You must pay before you can submit evidence.'
    logging.info(error)
    args['error_string'] = error
    return True, args


def has_not_applied_before_scheduling(**args) -> tuple:
    error = 'You must submit an application before you can schedule.'
    logging.info(error)
    args['error_string'] = error
    return True, args
