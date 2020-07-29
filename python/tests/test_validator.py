import json
from python.validator.config import Config as ValidationConfig
from python.validator.validate import Validate


# To override the config class for testing
class Config(ValidationConfig):
    SCHEMA_FILENAME = 'schema.json'
    

class TestValidator:

    def test_config_instantiation(self):
        config_class = ValidationConfig()
        assert type(config_class) is ValidationConfig

    def test_instantiation(self):
        validate_class = Validate(Config())
        assert type(validate_class) is Validate

    def test_sample_data_event_issuance_passes_validation(self):
        sample_data = self.get_sample_data('python/tests/sample_data/event_issuance.json')
        assert type(sample_data) is dict
        validate_class = Validate(Config())
        assert validate_class.validate(sample_data)['isSuccess'] is True

    def test_sample_data_event_issuance_fails_validation_with_empty_section_desc(self):
        sample_data = self.get_sample_data('python/tests/sample_data/event_issuance.json')
        assert type(sample_data) is dict
        sample_data['evt_issuance']['counts'][0]['section_desc'] = ''
        validate_class = Validate(Config())
        assert validate_class.validate(sample_data)['isSuccess'] is False

    def test_sample_data_event_issuance_fails_validation_with_missing_section_desc(self):
        sample_data = self.get_sample_data('python/tests/sample_data/event_issuance.json')
        assert type(sample_data) is dict
        del sample_data['evt_issuance']['counts'][0]['section_desc']
        validate_class = Validate(Config())
        assert validate_class.validate(sample_data)['isSuccess'] is False

    def test_sample_data_event_issuance_fails_validation_with_null_section_desc(self):
        sample_data = self.get_sample_data('python/tests/sample_data/event_issuance.json')
        assert type(sample_data) is dict
        sample_data['evt_issuance']['counts'][0]['section_desc'] = None
        validate_class = Validate(Config())
        assert validate_class.validate(sample_data)['isSuccess'] is False

    def test_sample_data_vt_payment_passes_validation(self):
        sample_data = self.get_sample_data('python/tests/sample_data/vt_payment.json')
        assert type(sample_data) is dict
        validate_class = Validate(Config())
        assert validate_class.validate(sample_data)['isSuccess'] is True

    def test_sample_data_vt_query_passes_validation(self):
        sample_data = self.get_sample_data('python/tests/sample_data/vt_query.json')
        assert type(sample_data) is dict
        validate_class = Validate(Config())
        assert validate_class.validate(sample_data)['isSuccess'] is True

    def test_sample_data_vt_dispute_passes_validation(self):
        sample_data = self.get_sample_data('python/tests/sample_data/vt_dispute.json')
        assert type(sample_data) is dict
        validate_class = Validate(Config())
        assert validate_class.validate(sample_data)['isSuccess'] is True

    def test_sample_data_vt_dispute_status_update_passes_validation(self):
        sample_data = self.get_sample_data('python/tests/sample_data/vt_dispute_status_update.json')
        assert type(sample_data) is dict
        validate_class = Validate(Config())
        assert validate_class.validate(sample_data)['isSuccess'] is True

    def test_sample_data_vt_dispute_finding_passes_validation(self):
        sample_data = self.get_sample_data('python/tests/sample_data/vt_dispute_finding.json')
        assert type(sample_data) is dict
        validate_class = Validate(Config())
        assert validate_class.validate(sample_data)['isSuccess'] is True

    def test_unknown_event_type_fails_validation(self):
        sample_data = self.get_sample_data('python/tests/sample_data/vt_payment.json')
        sample_data['event_type'] = 'unknown_event'
        validate_class = Validate(Config())
        assert validate_class.validate(sample_data)['isSuccess'] is False

    def test_message_without_an_event_type_fails_validation(self):
        sample_data = self.get_sample_data('python/tests/sample_data/vt_payment.json')
        del sample_data['event_type']
        validate_class = Validate(Config())
        assert validate_class.validate(sample_data)['isSuccess'] is False

    def test_message_that_breaks_validation_rule_returns_problematic_attribute_name(self):
        sample_data = self.get_sample_data('python/tests/sample_data/vt_payment.json')
        sample_data['event_id'] = "1234"  # string instead of integer
        validate_class = Validate(Config())
        assert validate_class.validate(sample_data)['isSuccess'] is False
        assert 'event_id' in validate_class.validate(sample_data)['description']

    @staticmethod
    def test_a_null_test_message_fails_validation():
        sample_data = None
        validate_class = Validate(Config())
        assert validate_class.validate(sample_data)['isSuccess'] is False

    @staticmethod
    def test_a_test_message_with_bad_json_fails_validation():
        sample_data = 'some string that is not json or does not decode into a dictionary'
        validate_class = Validate(Config())
        assert validate_class.validate(sample_data)['isSuccess'] is False

    @staticmethod
    def get_sample_data(file_name) -> dict:
        with open(file_name, 'r') as f:
            data = f.read()
        return json.loads(data)
        


