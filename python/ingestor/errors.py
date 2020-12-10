import logging


def has_not_applied(**args) -> tuple:
    """
    Check that review has not previously been scheduled
    """
    error = 'You must apply before you can submit evidence.'
    logging.info(error)
    args['error_string'] = error
    return False, args


def has_not_paid(**args) -> tuple:
    """
    Check that review has been scheduled
    """
    error = 'You must pay before you can submit evidence.'
    logging.info(error)
    args['error_string'] = error
    return False, args

