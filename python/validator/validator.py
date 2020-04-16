import logging
import json
from cerberus import Validator as Cerberus


class Validate:

    def __init__(self, config):
        self.schema = self._get_schema(config.SCHEMA_PATH + config.SCHEMA_FILENAME)
        logging.basicConfig(level=config.LOG_LEVEL)

    @staticmethod
    def _get_schema(file_name) -> dict:
        with open(file_name, 'r') as f:
            data = f.read()
        return json.loads(data)

    def validate(self, message: dict) -> dict:
        """
            The validate methods looks up a schema with the same event_type
            in the schema.json file, and uses the validation rules described
            in the file to determine if the message is valid.  This method
            returns a dictionary with the status of the validation and, if not
            successful, an error message.
        :param message:
        :return: dictionary
        """
        # check that message is a dictionary
        if not isinstance(message, dict):
            error_message = 'message does not decode into dictionary object'
            logging.info(error_message)
            return {'isSuccess': False, 'errors': error_message}

        # check basic structure of the message / event
        cerberus = Cerberus(self.schema['basic_message_structure']['cerberus_rules'])
        cerberus.allow_unknown = self.schema['basic_message_structure']['allow_unknown']
        if not cerberus.validate(message):
            logging.info(' - message failed basic validation')
            return {'isSuccess': False, 'errors': cerberus.errors}

        # if the message passes basic validation, test again
        # against specific event type
        cerberus = Cerberus(self.schema[message['event_type']]['cerberus_rules'])
        cerberus.allow_unknown = self.schema[message['event_type']]['allow_unknown']
        if cerberus.validate(message):
            logging.info(' - message passed validation for type: ' + message['event_type'])
            return {'isSuccess': True, 'errors': ''}
        else:
            logging.info(' - message failed validation for type: ' + message['event_type'])
            return {'isSuccess': False, 'errors': cerberus.errors}
