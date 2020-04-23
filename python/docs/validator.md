# About the Validator

The validator is a Python application that:
 - listens for messages posted to a RabbitMQ queue,
 - determines if the message is valid or not-valid,
 - if the message is valid, the message is moved to a `valid` queue,
 - if the message is not-valid, the message is moved to a `not-valid` queue.
 
 The application is designed to be configured using environment variables and JSON configuration files.

 # Environment Variables

  - `RABBITMQ_URL` - is the URL that the validator uses to connect to RabbitMQ.  By default, the URL is set to 'localhost'.
  - `WATCH_QUEUE` - name of the queue that the validator listens to. When messages arrive in this queue, the validator determines if it's valid or not.
  - `VALID_QUEUE` - the name of the queue that the validator publishes messages that are valid. 
  - `FAIL_QUEUE` - the name of the queue that the validator publishes messages that are not valid.
  - `RABBITMQ_MESSAGE_ENCODE` - the encoding used for RabbitMQ messages. By default this is set to 'utf-8'.
  - `SCHEMA_FILENAME` - the name of the JSON file that is used by the validator to determine if messages are valid or not valid (see more details below).
  - `VALIDATOR_USER` & `VALIDATOR_PASS` - are the credentials the validator should use when connecting to RabbitMQ.  It is recommended that these credentials be different from the credentials used to administer RabbitMQ


  # Validation Schema

The validator uses a JSON schema to determine if a message is valid.  By default, the name of the JSON schema is `schema.json`, but it can be overridden using an environment variable, `SCHEMA_FILENAME`.

To validate a message / event, the validator first uses the rules defined under the `basic_message_structure` attribute
 of the schema.json file.  If the basic message structure passes validation, the validator then runs a second validation 
 using rules specific to the event type.  

For example, if the validator receives a message with an `event_type` of `evt_issuance` the message is first validated 
against rules defined under the `basic_mesage_structure` attribute, then against rules defined under the `evt_issuance` 
attribute of the schema.json file.
    
If the message passes **both** sets of rules the validator will publish the message to the `valid` queue, otherwise 
the message is written to the failed queue.

Below is an example of the basic_message_structure rules:

```
{
      "basic_message_structure": {
        "allow_unknown": true,
        "cerberus_rules": {
          "event_id": {
            "type": "integer",
            "required": true
          },
          "event_version": {
            "type": "string",
            "required": true
          },
          "event_date_time": {
            "type": "string",
            "required": true
          },
          "event_type": {
            "type": "string",
            "required": true,
            "allowed": [
              "evt_issuance",
              "vt_query",
              "vt_payment",
              "vt_dispute",
              "vt_dispute_status_update",
              "vt_dispute_finding"
            ]
          }
    }
  }
}
```
The basic_message_structure has two required attributes:
 - `allow_unknown` - **Boolean** when set to 'True', the validator will allow fields / attributes that are not 
 documented in the schema.  When set to 'False' all fields must be listed in the schema
 - `cerberus_rules` - a set of fields / attributes and the associated rules. 
 [Cerberus](https://docs.python-cerberus.org/en/stable/) is a well-documented, third-party validation library.

The rules for each event_type follow an identical pattern.  Below is an example of the rules for the `vt_query` event
type.  

```
{
  "vt_query": {
    "allow_unknown": true,
    "cerberus_rules": {
      "vt_query": {
        "type": "dict",
        "required": true
      }
    }
  }
}
```

When a message fails validation, a validation error message is added to the message under the attribute, `errors`. 
Below is an example:

```
{
 "errors": [
    {
        "description": {
            "event_id": [
                "must be of integer type"
                ]}, 
            "timestamp": "22-Apr-2020 (15:46:52.017086)"
        }
    ]
}
```