import json
from python.validator.config import Config as ValidationConfig
from python.validator.validator import Validate


# To override the config class for testing
class Config(ValidationConfig):
    SCHEMA_FILENAME = 'schemas.json'
    

class TestValidator:

    def test_config_instantiation(self):
        config_class = ValidationConfig()
        assert type(config_class) is ValidationConfig

    def test_config_has_attribute_log_level(self):
        assert ValidationConfig.LOG_LEVEL == 'INFO'

    def test_instantiation(self):
        validate_class = Validate(Config())
        assert type(validate_class) is Validate

    def test_sample_data_event_issuance_passes_validation(self):
        sample_data = self.get_sample_data('python/tests/sample_data/event_issuance.json')
        assert type(sample_data) is dict
        validate_class = Validate(Config())
        assert validate_class.validate(sample_data) is True

    def test_sample_data_vt_payment_passes_validation(self):
        sample_data = self.get_sample_data('python/tests/sample_data/vt_payment.json')
        assert type(sample_data) is dict
        validate_class = Validate(Config())
        assert validate_class.validate(sample_data) is True

    def test_sample_data_vt_query_passes_validation(self):
        sample_data = self.get_sample_data('python/tests/sample_data/vt_query.json')
        assert type(sample_data) is dict
        validate_class = Validate(Config())
        assert validate_class.validate(sample_data) is True

    def test_sample_data_vt_dispute_passes_validation(self):
        sample_data = self.get_sample_data('python/tests/sample_data/vt_dispute.json')
        assert type(sample_data) is dict
        validate_class = Validate(Config())
        assert validate_class.validate(sample_data) is True

    def test_sample_data_vt_dispute_status_update_passes_validation(self):
        sample_data = self.get_sample_data('python/tests/sample_data/vt_dispute_status_update.json')
        assert type(sample_data) is dict
        validate_class = Validate(Config())
        assert validate_class.validate(sample_data) is True

    def test_sample_data_vt_dispute_finding_passes_validation(self):
        sample_data = self.get_sample_data('python/tests/sample_data/vt_dispute_finding.json')
        assert type(sample_data) is dict
        validate_class = Validate(Config())
        assert validate_class.validate(sample_data) is True

    def test_unknown_event_type_fails_validation(self):
        sample_data = self.get_sample_data('python/tests/sample_data/vt_payment.json')
        assert type(sample_data) is dict
        sample_data['event_type'] = 'unknown_event'
        validate_class = Validate(Config())
        assert validate_class.validate(sample_data) is False
    
    @staticmethod
    def get_sample_data(file_name) -> dict:
        with open(file_name, 'r') as f:
            data = f.read()
        
        return json.loads(data)
        


