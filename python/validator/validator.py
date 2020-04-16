import logging
import json
from cerberus import Validator as Cerberus


class Validate:

    def __init__(self, config):
        self.schemas = self._get_schemas(config.SCHEMA_PATH + config.SCHEMA_FILENAME)
        logging.basicConfig(level=config.LOG_LEVEL)

    @staticmethod
    def _get_schemas(file_name) -> dict:
        with open(file_name, 'r') as f:
            data = f.read()
        return json.loads(data)

    def validate(self, message: dict) -> dict:
        """
            The validate methods looks up a schema with the same event_type
            in the schemas.json file, and uses the validation rules described
            in the file to determine if the message is valid.  This method
            returns a dictionary with the status of the validation and, if not
            successful, an error message.
        :param message:
        :return: dictionary
        """
        if not message or 'event_type' not in message:
            error_message = "the 'event_type' attribute is required"
            logging.info(error_message)
            return {'isSuccess': False, 'errors': error_message}

        # lookup the schema in self.schemas['data'] that matches the event_type in the message
        matching_schema = None
        for schema in self.schemas:
            if schema['event_type'] == message['event_type']:
                logging.info('matching schema found')
                matching_schema = schema

        if matching_schema:
            cerberus = Cerberus(matching_schema['cerberus'])
            cerberus.allow_unknown = matching_schema['allow_unknown']
            if cerberus.validate(message):
                logging.info(' - passes validation using: ' + matching_schema['event_type'])
                return {'isSuccess': True, 'errors': ''}
            else:
                logging.info(' - message failed validation')
                return {'isSuccess': False, 'errors': cerberus.errors}

        # No matching schema found in configuration
        logging.info(' - NOT valid ' + message['event_type'] + ' is not in the schemas.json file')
        return {
            'isSuccess': False,
            'errors': "event_type, " + message['event_type'] + ' is not in the schemas.json file'
        }
