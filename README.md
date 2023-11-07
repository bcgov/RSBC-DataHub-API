

# Road Safety DataHub API

A series of Python components that process eTicketing and digital forms for RoadSafety BC. 


![img](https://img.shields.io/badge/Lifecycle-Stable-97ca00)

At the present time, these components process the following types of events:

Electronic Tickets:
- the issuance of a ticket
- the payment of a ticket
- the dispute of a ticket
- the status of a dispute
- the finding of a disputed ticket
- the query of a ticket record
  
Driving Prohibition Reviews
- the application to review
- the payment for a review
- the scheduling of a review
- the release of police evidence 


The system to handle these events is made up of seven containers / pods:
- An ingestor that accepts events as either XML or JSON data
- A Message Broker (RabbitMQ) that stores the events while they're being processed.
- A validator that checks events to make sure required fields are included
- A geocoder that determines the geolocation of an address
- An API endpoint for PayBC to query for payable items
- A writer that inserts the data into the business intelligence database
- A form handler that processes digital form submissions

# Local development 

To begin local development of this project:
- create a `.env` file by copying `.env.sample` to `.env` in the root of the project directory
- edit the default values in the `.env` file to reflect your secret values.
- run `docker-compose build && docker-compose up`

Additional documentation is available for each container / pod:
- [Ingestor](./python/docs/ingestor.md)
- [Validator](./python/docs/validator.md)
- [Writer](./python/docs/writer.md)
- [Geocoder](./python/docs/geocoder.md)
- [PayBC API](./python/docs/paybc_api.md)  
- [Form Handler](./python/docs/form_handler.md)


## How to Contribute

If you would like to contribute, please see our [Contributing](./CONTRIBUTING.md) guidelines.

Please note that this project is released with a [Contributor Code of Conduct](./CODE_OF_CONDUCT.md). By participating in this project you agree to abide by its terms.
