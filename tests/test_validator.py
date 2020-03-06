import os
import unittest
import json
import logging
from validator.config import Config as ValidationConfig
from validator.validator import Validate as Validate


# To override the config class for testing
class Config(ValidationConfig):
    SCHEMA_FILENAME         = 'validator/schemas.json'
    

class TestValidator:

    def test_config_instantiation(self):
        config_class = ValidationConfig()
        assert type(config_class) is ValidationConfig


    def test_config_has_attribute_log_level(self):
        assert ValidationConfig.VALIDATOR_LOG_LEVEL == 'INFO'


    def test_instantiation(self):
        validate_class = Validate(Config())
        assert type(validate_class) is Validate


    def test_sample_data_event_issuance_passes_validation(self):

        sampleData = self.getSampleData('sample_data/event_issuance.json')
        assert type(sampleData) is dict

        validate_class = Validate(Config())
        assert validate_class.validate(sampleData) == True


    def test_sample_data_vt_payment_passes_validation(self):

        sampleData = self.getSampleData('sample_data/vt_payment.json')
        assert type(sampleData) is dict

        validate_class = Validate(Config())
        assert validate_class.validate(sampleData) == True


    def test_sample_data_vt_query_passes_validation(self):

        sampleData = self.getSampleData('sample_data/vt_query.json')
        assert type(sampleData) is dict

        validate_class = Validate(Config())
        assert validate_class.validate(sampleData) == True


    def test_sample_data_vt_dispute_passes_validation(self):

        sampleData = self.getSampleData('sample_data/vt_dispute.json')
        assert type(sampleData) is dict

        validate_class = Validate(Config())
        assert validate_class.validate(sampleData) == True


    def test_sample_data_vt_dispute_status_update_passes_validation(self):

        sampleData = self.getSampleData('sample_data/vt_dispute_status_update.json')
        assert type(sampleData) is dict

        validate_class = Validate(Config())
        assert validate_class.validate(sampleData) == True


    def test_sample_data_vt_dispute_finding_passes_validation(self):

        sampleData = self.getSampleData('sample_data/vt_dispute_finding.json')
        assert type(sampleData) is dict

        validate_class = Validate(Config())
        assert validate_class.validate(sampleData) == True


    def getSampleData(self, fileName) -> dict:
        with open(fileName, 'r') as f:
            data = f.read()
        
        return json.loads(data)
        


