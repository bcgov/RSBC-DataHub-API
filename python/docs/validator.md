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

The validator uses a JSON schema to determine if a message is valid.  By default, the name of the JSON schema is `schemas.json`, but it can be overridden using an environent variable, `SCHEMA_FILENAME`.

The schema.json file defines a collection of schema definitions. The validator will publish a message to the `valid` queue if the message passes **any one** of such schemas.

```
{
        "data": [
                    {
                        ... <schema 1> 
                    },
                    {
                        ... <schema 2>
                    }
        ]
}
```

It is recommended to create a schema for each different data type.

Each schema definitions has **four** required attributes:
 - `short_name` - the short name of the schema used for log file output. 
 - `description` - a description field for reference in the schema only
 - `allow_unknown` - **Boolean** when set to 'True', the validator will allow fields / attributes that are not documented in the schema.  When set to 'False' all fields must be listed in the schema
 - `cerberus` - a set of fields / attributes and the associated rules. [Cerberus](https://docs.python-cerberus.org/en/stable/) is a well documented third-party validation library.


```
{
      "short_name": "evt_issuance",
      "description": "schema for evt_issuance",
      "allow_unknown": true,
      "cerberus": {
        ... < cerberus rules as defined below >
      }
}
```

# Cerberus

Below is an example of a Cerberus rule set.  Each attribute is the name of an field expected in the message.  Sub-attributes define the type of data expected and other rules. Cerberus' documentation describes a full list of the available rules here:  [https://docs.python-cerberus.org/en/stable/validation-rules.html]

```
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
    "evt_issuance"
    ]
},
"evt_issuance": {
    "type": "dict",
    "required": true
}
```

