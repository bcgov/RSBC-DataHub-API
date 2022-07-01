# About the Ingestor

The ingestor is a Python Flask API with the following endpoints:

### E-Ticket

Accepts POST requests in the form of a JSON payload and writes the payload to a RabbitMQ `ingested` queue for 
subsequent processing.  Endpoint:   
 
``` http://<host_name>/v1/publish/event/ETK ```

### Digital Forms

Accepts POST requests in the form of an XML payload from Orbeon (a proprietary product hosted by GDX) 
and writes the payload to a RabbitMQ `ingested` queue for subsequent processing. Endpoint:   
 
``` http://<host_name>/v1/publish/event/form ```

### Schedule

Accepts POST requests with two form-url-encoded parameters (prohibition_number and last_name)
and returns a JSON object that contains the available dates and times 
that an applicant is eligible to book a review. The endpoint is protected with basic authentication. 
The credentials are passed in as environment variables.
 
``` http://<host_name>/schedule ```


### Evidence

Accepts POST requests with two form-url-encoded parameters (prohibition_number and last_name)
and returns a JSON object that indicates if an applicant is eligible to upload evidence for their review.
The endpoint is protected with basic authentication. The credentials are passed in as environment variables.
 
``` http://<host_name>/evidence ```


### List Email Templates (DEV only)

Accepts GET requests and returns an HTML page with links to email templates automatically sent by the components. 
This endpoint is only available in the DEV and PR environments.   
 
``` http://<host_name>/check_templates ```


### View Specific Email Template (DEV only)

Accepts GET requests and returns an HTML page that shows the text and layout of the template requested. 
This endpoint is only available in the DEV and PR environments.   
 
``` http://<host_name>/check?template=<template_name> ```


 # Environment Variables

 The ingestor can be configured using environment variables.  
 - `SECRET_KEY` - is an alpha numerical string that Flask uses to keep client-side sessions secure. Each instance **MUST** set a unique key.
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
