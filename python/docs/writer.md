# About the Writer

The writer is a Python application that:
 - consumes messages posted to a RabbitMQ queue,
 - creates insert statements for one or more database tables
 - writes the data to the database and deletes the message from the queue
 - if the record already exists in the database or otherwise cannot be inserted, 
 the message is moved to a failed-write queue and an error message attribute is appended to the event  
 
 The application is designed to be configured using environment variables and JSON configuration files.

 # Environment Variables

 - `RABBITMQ_URL` - is the URL that the ingestor uses to connect to RabbitMQ.  By default, the URL is set to 'localhost'.
 - `RABBITMQ_EXCHANGE` - is the name of the RabbitMQ exchange.  At present, the ingestor uses a blank / null exchange.   
 - `RETRY_DELAY` - is the time (in seconds) that RabbitMQ will wait before trying the connection again
 - `LOG_LEVEL` - sets the verbosity of the logging system. Options are: WARN, INFO or DEBUG. By default the log level is set to INFO.
 - `RABBITMQ_MESSAGE_ENCODE` - determines the encoding mechanism used for messages.  By default it is set to `uft-8`.
 - `WRITE_QUEUE` - is the name of the RabbitMQ that the ingestor will use to save messages.  By default the name of this queue is **ingested** but can 
 be overridden as needed.
 - `MAX_CONNECTION_RETRIES` - sets the number of times that the Ingestor will attempt to connect to RabbitMQ before giving up.
  
 - `WATCH_QUEUE` - name of the queue that the writer listens to. When messages arrive in this queue, it's written to the database.
 - `FAIL_QUEUE` - name of the queue that the writer moves messages that cannot be written to the database. 
 - `MQ_WRITER_USER` & `MQ_WRITER_PASS` - are the credentials the writer should use when connecting to RabbitMQ.  It is recommended that these credentials be different from the credentials used to administer RabbitMQ
  
 - `DB_HOST` - the host name of the database
 - `DB_NAME` - the name of the database
 - `DB_USERNAME` & `DB_PASSWORD` - credentials used to connect the writer to the database.
 - `MAPPER_CONFIG_FILENAME` - the name of the JSON file that is used by the configure the writer (see below).


  # Mapping Schema

The writer uses a JSON schema to map the JSON attributes to the database fields.  By default, the name of the mapping configuration file is `mapper.json`, but it can be overridden using the `MAPPER_CONFIG_FILENAME` environent variable.

The mapper.json file defines a field mapping for each datatype.

```
{
        "data_types": [
                    {
                        ... <datatype 1> 
                    },
                    {
                        ... <datatype 2>
                    }
        ]
}
```

Each mapping definitions has two required attributes:
 - `name` - the short name of the datatype.  This name must match the `event_type` attribute in the JSON message. 
 - `tables` - a list of objects that describes which tables should be populated (more below)


```
{
    "name": "evt_issuance",
    "tables": [
        { 
          ... <table definition 1>
        },
        { 
          ... <table definition 2>
        }
    ]
}
```

Each table definition describes a database table that the writer will populate from the JSON message and describes how JSON attributes map to the database field names.

For example, the following table object tells the writer to populate a table called `vph_events` with data from three fields:
 - EVENT_ID,
 - EVENT_DTM,
 - TICKET_NO

```
{
    "name": "vph_events",
    "relationship": "one-to-one",
    "fields": [
        {
            "json_name": "event_id",
            "destination_name": "EVENT_ID"
        },
        {
            "json_name": "event_date_time",
            "destination_name": "EVENT_DTM"
        },
        {
            "json_name": "evt_issuance.ticket_number",
            "destination_name": "TICKET_NO"
        }
    ]
},
```

The `relationship` attribute tells the writer whether each JSON message should populate a single record ("one-to-one") or multiple records ("one-to-many") in the table.

Below is an example of a `one-to-many` table definition.  

```
{
    "name": "vph_violation_kpi_details",
    "relationship": "one-to-many",
    "many_details": {
        "iterate_on": "evt_issuance.counts",
        "key_field": {
            "json_name": "evt_issuance.ticket_number",
            "destination_name": "TICKET_NO"
        }
    },
    "fields": [
        {
            "json_name": "count_number",
            "destination_name": "count_nbr"
        },
        {
            "json_name": "act_code",
            "destination_name": "act_cd"
        },
        {
            "json_name": "section_text",
            "destination_name": "section_txt"
        }
    ]
}
```

One-to-many table definitions have an additional attribute called, `many_details` with two sub-attributes:
 - `iterate_on` - the list attribute in the JSON message which the writer will itterate over.
 - `key_field` - the name of the primary field used by the database to join the one-to-many table to the parent table.
