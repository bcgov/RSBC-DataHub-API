import logging
import pika
import time
import json
from cerberus import Validator as Cerberus


class Validate():

    
    def __init__(self, config):
        self.schemas = self._getSchemas(config.SCHEMA_FILENAME)
        logging.basicConfig(level=config.VALIDATOR_LOG_LEVEL)


    def _getSchemas(self, fileName) -> dict:
        with open(fileName, 'r') as f:
            data = f.read()
        
        return json.loads(data)


    def validate(self, message) -> bool:
        # loop through each schema, return True on 
        # first schema that passes validation

        for schema in self.schemas['data']:
            v = Cerberus(schema['cerberus'])
            v.allow_unknown = schema['allow_unknown']
            if(v.validate(message)):
                logging.info(' - passes validation using: ' + schema['short_name'])
                return True

        logging.info(' - NOT valid ')
        return False


