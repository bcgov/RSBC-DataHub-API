import logging
import logging.config
from python.common.config import Config
from python.common.helper import load_json_into_dict
from cerberus import Validator as Cerberus

logging.config.dictConfig(Config.LOGGING)


class Validate:

    def __init__(self, config):
        self.config = config
        self.schemas = load_json_into_dict(config.SCHEMA_PATH + config.SCHEMA_FILENAME)

    def validate(self, message: dict) -> dict:
        """
            The validate methods looks up a schema with the same event_type
            in the schemas json file, and uses the validation rules described
            in the file to determine if the message is valid.  This method
            returns a dictionary with the status of the validation and, if not
            successful, an error message.
        :param message:
        :return: dictionary
        """
        cerberus_errors = []

        # check that message is a dictionary
        if not isinstance(message, dict):
            error_message = 'the message does not decode into a dictionary object'
            logging.warning(error_message)
            return {'isSuccess': False, "queue": "error", 'description': error_message}

        # check that that the message has an event_type attribute
        if 'event_type' not in message:
            error_message = 'the message does not have an event_type attribute'
            logging.warning(error_message)
            return {'isSuccess': False, "queue": "error", 'description': error_message}

        # check that that the message has an associated validation schema
        if message['event_type'] not in self.schemas:
            error_message = 'the message does not have an associated validation schema'
            logging.warning(error_message)
            return {'isSuccess': False, "queue": "error", 'description': error_message}

        # return the validation error message from the associated schema
        schema = self.schemas[message['event_type']]
        cerberus = Cerberus(schema['cerberus_rules'])
        cerberus.allow_unknown = schema['allow_unknown']
        if cerberus.validate(message):
            logging.info(' - message passed validation')
            return {'isSuccess': True, "queue": schema['valid-queue'], 'description': ''}
        else:
            logging.info(' - message failed validation validation')
            return {'isSuccess': False, "queue": schema['invalid-queue'], 'description': cerberus.errors}


