# Road Safety Initiative

This project develops a system to ingest, validate and write road safety data into a business intelligence database for further analysis.  

At the present time, road safety data is made up of the following types of events:
- the issuance of a ticket
- the payment of a ticket
- the dispute of a ticket
- the status of a dispute
- the finding of a disputed ticket
- the query of a ticket record


The system to handle these events is made up of four containers / pods:
- An ingestor that accepts events as JSON data
- A Message Broker (RabbitMQ) that stores the events while they're being processed.
- A validator that checks each event to make sure it includes the required fields.
- A writer that inserts the data into a business intelligence database

# Local development 

To begin local development of this project:
- create a `.env` file by copying `.env.sample` to `.env` in the root of the project directory
- edit the default values in the `.env` file to reflect your secret values.
- run `docker-compose build && docker-compose up`

Additional documentation is available for each container / pod:
- [Ingestor](./python/docs/ingestor.md)
- [Validator](./python/docs/validator.md)
- [Writer](./python/docs/writer.md)




