from cryptography.fernet import Fernet
import datetime
import json


class Message:

    ENCRYPTED_ATTRIBUTE_NAME = 'encrypted'

    @staticmethod
    def encode_message(message: dict, secret: str, encoding="utf-8") -> bytes:
        """
        Encrypt the sensitive attributes of the message but leave the event attributes and
        errors attributes unencrypted so admins can look at the message in RabbitMQ and
        determine why the message failed validation or why it couldn't be written to the
        database.
        """
        if 'encrypt-at-rest' in message and message['encrypt-at-rest']:
            message = Message.encrypt_sensitive_attribute(message, secret, encoding)
        return Message.encode(message)

    @staticmethod
    def decode_message(body: bytes, secret, encoding="utf-8") -> dict:
        messsage = Message.decode(body)
        if 'encrypt-at-rest' in messsage and messsage['encrypt-at-rest']:
            return Message.decrypt_sensitive_attribute(messsage, secret, encoding)
        return messsage 

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
