import pytest
import json
from python.common.message import Message
from pprint import pprint


class TestEncryptedMessage:

    BYTE_ENCODING = 'utf-8'
    KEY = 'to1AC3l-KLazylZRYHVTOVq_v7ixfdLeHTXWN5mBVIs='

    @pytest.fixture
    def sample_data(self):
        return {
            'event_id': 1234,
            'event_type': 'vt_query',
            'vt_query': {'ticket_number': '123ABC'}}

    @pytest.fixture
    def get_encrypted_message(self, sample_data):
        return Message.encrypt_sensitive_attribute(sample_data, self.KEY, self.BYTE_ENCODING)

    @staticmethod
    def test_encrypt_sensitive_attribute_method(get_encrypted_message):
        assert 'vt_query' not in get_encrypted_message
        assert 'encrypted' in get_encrypted_message
        assert isinstance(get_encrypted_message['encrypted'], str)

    def test_decrypt_sensitive_attribute_method(self, get_encrypted_message, sample_data):
        decrypted_message = Message.decrypt_sensitive_attribute(get_encrypted_message, self.KEY, self.BYTE_ENCODING)
        assert 'vt_query' in decrypted_message
        assert 'encrypted' not in decrypted_message
        assert 'ticket_number' in decrypted_message['vt_query']
        assert decrypted_message == sample_data

    def test_encode_encrypted_text_message(self, sample_data):
        sample_data['encrypt-at-rest'] = True
        message_bytes = Message.encode_message(sample_data, self.KEY, self.BYTE_ENCODING)
        message_string = message_bytes.decode("utf-8")
        message_dict = json.loads(message_string)
        assert isinstance(message_bytes, bytes)
        assert isinstance(message_dict, dict)
        assert 'encrypted' in message_dict
        assert 'vt_query' not in message_dict

    def test_plain_message_encode(self, sample_data):
        encoded_message = Message.encode_message(sample_data, '')
        assert isinstance(encoded_message, bytes)

    def test_plain_message_decode(self, sample_data):
        message_bytes = bytes(json.dumps(sample_data), "utf-8")
        encoded_message = Message.decode(message_bytes)
        assert isinstance(encoded_message, dict)

    def test_add_error_to_message_method(self):
        message_dict = {'event_type': 'some invalid event'}
        expected_error_message = 'error message'
        error_dict = {'isSuccess': False, 'errors': expected_error_message}
        modified_message = Message.add_error_to_message(message_dict, error_dict['errors'])
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
        modified_message = Message.add_error_to_message(message_dict, error_dict['errors'])
        assert isinstance(modified_message, dict)
        assert 'errors' in modified_message
        assert 'timestamp' in modified_message['errors'][0]
        assert 'description' in modified_message['errors'][0]

    @staticmethod
    def test_encode_plain_text_message(sample_data):
        message_bytes = Message.encode_message(sample_data, '')
        assert isinstance(message_bytes, bytes)

