import pytest
from cryptography.fernet import Fernet
import json
import python.common.message as message
from pprint import pprint


class TestEncryptedMessage:

    KEY = str(Fernet.generate_key(), 'utf-8')

    @pytest.fixture
    def sample_data(self):
        return {
            'event_id': 1234,
            'event_type': 'vt_query',
            'vt_query': {'ticket_number': '123ABC'}}

    @pytest.fixture
    def get_encrypted_message(self, sample_data):
        return message.encrypt_sensitive_attribute(sample_data, self.KEY)

    @staticmethod
    def test_encrypt_sensitive_attribute_method(get_encrypted_message):
        assert 'vt_query' not in get_encrypted_message
        assert 'encrypted' in get_encrypted_message
        assert isinstance(get_encrypted_message['encrypted'], str)

    def test_decrypt_sensitive_attribute_method(self, get_encrypted_message, sample_data):
        decrypted_message = message.decrypt_sensitive_attribute(get_encrypted_message, self.KEY)
        assert 'vt_query' in decrypted_message
        assert 'encrypted' not in decrypted_message
        assert 'ticket_number' in decrypted_message['vt_query']
        assert decrypted_message == sample_data

    def test_encode_encrypted_text_message_v1(self, sample_data):
        sample_data['encrypt_at_rest'] = True
        message_bytes = message.encode_message(sample_data, self.KEY)
        message_string = message_bytes.decode("utf-8")
        message_dict = json.loads(message_string)
        assert isinstance(message_bytes, bytes)
        assert isinstance(message_dict, dict)
        assert 'encrypted' in message_dict
        assert 'vt_query' not in message_dict

    def test_plain_message_encode(self, sample_data):
        encoded_message = message.encode_message(sample_data, '')
        assert isinstance(encoded_message, bytes)

    def test_plain_message_decode(self, sample_data):
        message_bytes = bytes(json.dumps(sample_data), "utf-8")
        encoded_message = message.decode(message_bytes)
        assert isinstance(encoded_message, dict)

    def test_add_error_to_message_method(self):
        message_dict = {'event_type': 'some invalid event'}
        expected_error_message = 'error message'
        error_dict = {'isSuccess': False, 'errors': expected_error_message}
        modified_message = message.add_error_to_message(message_dict, error_dict['errors'])
        assert isinstance(modified_message, dict)
        assert 'errors' in modified_message
        assert 'timestamp' in modified_message['errors'][0]
        assert 'description' in modified_message['errors'][0]
        assert modified_message['errors'][0]['description'] == expected_error_message

    @staticmethod
    def test_add_error_to_message_method_handles_cerberus_errors():
        error_message = {'fieldA': ['required', 'must be string']}
        message_dict = 'some string that is not valid JSON'
        error_dict = {'isSuccess': False, 'errors': error_message}
        modified_message = message.add_error_to_message(message_dict, error_dict['errors'])
        assert isinstance(modified_message, dict)
        assert 'errors' in modified_message
        assert 'timestamp' in modified_message['errors'][0]
        assert 'description' in modified_message['errors'][0]

    @staticmethod
    def test_encode_plain_text_message(sample_data):
        message_bytes = message.encode_message(sample_data, '')
        assert isinstance(message_bytes, bytes)
        pprint(message_bytes)

    @staticmethod
    def test_decode_plain_text_message(sample_data):
        message_bytes = message.encode_message(sample_data, '')
        message_dict = message.decode_message(message_bytes, '')
        pprint(message_bytes)
        assert sample_data == message_dict

    @staticmethod
    def test_encode_encrypted_text_message(sample_data):
        encryption_string = str(Fernet.generate_key(), "utf-8")
        print(encryption_string)
        sample_data['encrypt_at_rest'] = True
        message_bytes = message.encode_message(sample_data, encryption_string)
        assert isinstance(message_bytes, bytes)
        pprint(message_bytes)

