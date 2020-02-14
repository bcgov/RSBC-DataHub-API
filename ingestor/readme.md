# About the Ingestor

The ingestor is a Python Flask application that accepts POST requests in the form of a JSON payload and writes payload to a RabbitMQ queue for subsequent processing.  Endpoint:   
 
``` http://<host_name>/api/v1/event/<queue_name> ```

 # Environment Variables

 The ingestor can be configured using enviroment variables.  
 - `SECRET_KEY` - is an alpha numerical string that Flask uses to keep client-side sessions secure. Each instance **MUST** set a unique key.
 - `FLASK_ENV` - can be set to "Development" for debugging purposes. By default, this environment variable is not set which turns off the debugging info.
 - `RABBITMQ_URL` - is the URL that the ingestor uses to connect to RabbitMQ.  By default, the URL is set to 'localhost'.
 - `RABBITMQ_EXCHANGE` - is the name of the RabbitMQ exchange.  At present, the ingestor uses a blank / null exchange.  
 - `RABBITMQ_QUEUES` - is a list of authorized queue names separated by commas.  By default, there are two authorized queues: 'ETK' and 'EDM'.  On startup, the ingestor creates the queue in this list (if they don't already exist). The queue names added to this list affect the endpoint.  For example, if `RABBITMQ_QUEUES` is given this value, 'ETK,EDU' Then the following endpoints are valid: 
 
    - ```https://<host_name>/api/v1/event/ETK```
    - ```https://<host_name>/api/v1/event/EDU```

 - `MAX_CONNECTION_RETRIES` - sets the number of times that the Ingestor will attempt to connect to RabbitMQ before giving up.
 - `INGEST_USER` & `INGEST_PASS` - are the credentials the ingestor should use when connecting to RabbitMQ.  It is recommended that these credentials be different from the credentials used to administer RabbitMQ

