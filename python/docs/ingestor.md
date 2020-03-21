# About the Ingestor

The ingestor is a Python Flask application that accepts POST requests in the form of a JSON payload and writes payload to a RabbitMQ queue for subsequent processing.  Endpoint:   
 
``` http://<host_name>/v1/publish/event ```

 # Environment Variables

 The ingestor can be configured using environment variables.  
 - `SECRET_KEY` - is an alpha numerical string that Flask uses to keep client-side sessions secure. Each instance **MUST** set a unique key.
 - `FLASK_ENV` - can be set to "Development" for debugging purposes. By default, this environment variable is not set which turns off the debugging info.
 - `INGEST_USER` & `INGEST_PASS` - are the credentials the ingestor should use when connecting to RabbitMQ.  It is recommended that these credentials be different from the credentials used to administer RabbitMQ

 - `RABBITMQ_URL` - is the URL that the ingestor uses to connect to RabbitMQ.  By default, the URL is set to 'localhost'.
 - `RABBITMQ_EXCHANGE` - is the name of the RabbitMQ exchange.  At present, the ingestor uses a blank / null exchange.   
 - `RETRY_DELAY` - is the time (in seconds) that RabbitMQ will wait before trying the connection again
 - `LOG_LEVEL` - sets the verbosity of the logging system. Options are: WARN, INFO or DEBUG. By default the log level is set to INFO.
 - `RABBITMQ_MESSAGE_ENCODE` - determines the encoding mechanism used for messages.  By default it is set to `uft-8`.
 - `WRITE_QUEUE` - is the name of the RabbitMQ that the ingestor will use to save messages.  By default the name of this queue is **ingested** but can 
 be overridden as needed.
 - `MAX_CONNECTION_RETRIES` - sets the number of times that the Ingestor will attempt to connect to RabbitMQ before giving up.
 
 ###Resources
 - [Sample Curl Requests](./curl.md)
