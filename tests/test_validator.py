import os
import unittest
import json
from validator.validator import Validate as Validate


class TestValidator:


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


    def getSampleData(self, fileName) -> dict:
        with open(fileName, 'r') as f:
            data = f.read()
        
        return json.loads(data)
        

class Config():
    SCHEMA_FILENAME         = 'validator/schemas.json'


