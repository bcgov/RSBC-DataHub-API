from cryptography.fernet import Fernet
import datetime
import json


def encode_message(message: dict, secret: str, encoding="utf-8") -> bytes:
    """
    Encrypt the sensitive attributes of the message but leave the event attributes and
    errors attributes unencrypted so admins can look at the message in RabbitMQ and
    determine why the message failed validation or why it couldn't be written to the
    database.
    """
    if 'encrypt_at_rest' in message and message['encrypt_at_rest'] is True:
        message = encrypt_sensitive_attribute(message, secret, encoding)
    return encode(message)


def decode_message(body: bytes, secret: str, encoding="utf-8") -> dict:
    message = decode(body)
    if 'encrypt_at_rest' in message and message['encrypt_at_rest'] is True:
        return decrypt_sensitive_attribute(message, secret, encoding)
    return message


def encrypt_sensitive_attribute(message: dict, secret: str, encoding="utf-8", attribute_name="encrypted") -> dict:
    """
    Encrypt the attribute of the message that may contain personal information
    and return the entire message with encrypted and unencrypted attributes.
    The event attributes and errors attributes are left unencrypted to help
    administrators troubleshoot validation errors.
    """
    fernet = Fernet(bytes(secret, encoding))
    sensitive_attribute = message['event_type']
    sensitive_bytes = encode(message[sensitive_attribute])
    encrypted_string = fernet.encrypt(sensitive_bytes).decode(encoding)
    message[attribute_name] = encrypted_string
    message.pop(sensitive_attribute)
    return message


def decrypt_sensitive_attribute(message: dict, secret: str, encoding="utf-8", attribute_name="encrypted") -> dict:
    """
    Decrypt the `encrypted` message attribute within the message and return the
    original message with the unencrypted message attributes included.
    """
    fernet = Fernet(bytes(secret, encoding))
    sensitive_attribute = message['event_type']
    token = message[attribute_name].encode(encoding)
    sensitive_bytes = fernet.decrypt(token)
    message[sensitive_attribute] = decode(sensitive_bytes)
    message.pop(attribute_name)
    return message


def encode(payload: dict, encoding="utf-8") -> bytes:
    """
    Encrypt the payload
    """
    return bytes(json.dumps(payload), encoding)


def decode(body: bytes, encoding="utf-8") -> dict:
    """
    Decrypt the entire body
    """
    message_string = body.decode(encoding)
    return json.loads(message_string)


def add_error_to_message(message: dict, error: dict) -> dict:
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
