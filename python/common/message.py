from cryptography.fernet import Fernet
import datetime
import json


class Message:

    ENCRYPTED_ATTRIBUTE_NAME = 'encrypted'

    # @staticmethod
    # def encode_entire_message(is_encrypt: bool, message: dict, secret: str, encoding="utf-8") -> bytes:
    #     """
    #     Encrypt and encode the entire message.  When a message is
    #     ingested it hasn't yet been validated so we encrypt the
    #     entire message before sending it to RabbitMQ in case the
    #     message format isn't as expected.
    #     """
    #     encoded_message = Message.encode(message, encoding)
    #     if is_encrypt:
    #         fernet = Fernet(bytes(secret, encoding))
    #         return fernet.encrypt(encoded_message)
    #     else:
    #         return encoded_message
    #
    # @staticmethod
    # def decode_entire_message(is_encrypt: bool, encoded_message: bytes, secret: str, encoding="utf-8") -> dict:
    #     """
    #     Decrypt and decode an ingested message and return a Python dictionary.
    #     An ingested message is entirely encrypted.
    #     """
    #     if is_encrypt:
    #         fernet = Fernet(bytes(secret, encoding))
    #         return Message.decode(fernet.decrypt(encoded_message))
    #     else:
    #         Message.decode(encoded_message)
            
    @staticmethod
    def encode_message(is_encrypt: bool, message: dict, secret: str, encoding="utf-8") -> bytes:
        """
        Encrypt the sensitive attributes of the message but leave the event attributes and
        errors attributes unencrypted so admins can look at the message in RabbitMQ and
        determine why the message failed validation or why it couldn't be written to the
        database.
        """
        if is_encrypt:
            message = Message.encrypt_sensitive_attribute(message, secret, encoding)
        return Message.encode(message)

    @staticmethod
    def decode_message(is_encrypt: bool, body: bytes, secret, encoding) -> dict:
        decoded_message = Message.decode(body)
        if is_encrypt:
            return Message.decrypt_sensitive_attribute(decoded_message, secret, encoding)
        return decoded_message 

    @staticmethod
    def encrypt_sensitive_attribute(message: dict, secret: str, encoding="utf-8") -> dict:
        """
        Encrypt the attribute of the message that may contain personal information
        and return the entire message with encrypted and unencrypted attributes.
        The event attributes and errors attributes are left unencrypted to help
        administrators troubleshoot validation errors.
        """
        fernet = Fernet(bytes(secret, encoding))
        sensitive_attribute = message['event_type']
        sensitive_bytes = Message.encode(message[sensitive_attribute])
        encrypted_string = fernet.encrypt(sensitive_bytes).decode(encoding)
        message[Message.ENCRYPTED_ATTRIBUTE_NAME] = encrypted_string
        message.pop(sensitive_attribute)
        return message

    @staticmethod
    def decrypt_sensitive_attribute(message: dict, secret: str, encoding="utf-8") -> dict:
        """
        Decrypt the `encrypted` message attribute within the message and return the
        original message with the unencrypted message attributes included.
        """
        fernet = Fernet(bytes(secret, encoding))
        sensitive_attribute = message['event_type']
        token = message[Message.ENCRYPTED_ATTRIBUTE_NAME].encode(encoding)
        sensitive_bytes = fernet.decrypt(token)
        message[sensitive_attribute] = Message.decode(sensitive_bytes)
        message.pop(Message.ENCRYPTED_ATTRIBUTE_NAME)
        return message

    @staticmethod
    def encode(payload: dict, encoding="utf-8") -> bytes:
        """
        Encrypt the payload
        """
        return bytes(json.dumps(payload), encoding)

    @staticmethod
    def decode(body: bytes, encoding="utf-8") -> dict:
        """
        Decrypt the entire body
        """
        message_string = body.decode(encoding)
        return json.loads(message_string)

    @staticmethod
    def add_error_to_message(message, error) -> dict:
        """
            Add 'errors' as a message attribute so as to keep a
            history of events in case it fails repeatedly.
        :param message:
        :param error:
        :return:
        """
        now_string = datetime.datetime.now().strftime("%d-%b-%Y (%H:%M:%S.%f)")
        if not isinstance(message, dict):
            message = dict()

        if 'errors' not in message:
            message['errors'] = []
        message['errors'].append({'description': error, 'timestamp': now_string})
        return message
