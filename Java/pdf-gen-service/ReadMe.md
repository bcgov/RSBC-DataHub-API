# RSBC APR pdf-gen-service

## Application Overview
This application renders PDF forms for the **RSBC APR** project. It is a Java Spring Boot microservice that generates PDF documents based on data received from Rabbit MQ or direct requests over HTTP from front end forms.

This service use the Adobe Experience Manager along with XDP templates to render PDF output. 

PDF form facsimiles are limited to permutations of forms 1 and 3. 

---

![Project Status: In Development](https://img.shields.io/badge/status-in--development-yellow)

---

## Getting Started

### Prerequisites
- Java 17+
- Maven 3.8+
- Git
- (Optional) Docker, if containerizing

---

## Cloning the Repository
```bash
git clone https://github.com/bcgov/RSBC-DataHub-API.git
cd RSBC-DataHub-API/Java/pdf-gen-service
```
---

## Building the Application
Run the following to build the project and produce an executable JAR:

```bash
mvn clean install
```

The compiled JAR will be located in the `target/` directory.

---

## Running the Application
You can run the application locally using:

```bash
java -jar target/pdf-gen-service-<version>.jar
```

Or use Spring Boot directly:

```bash
mvn spring-boot:run
```

---

## Environment Variables
The application expects certain environment variables to be set for configuration. These should be supplied in your runtime environment or via a `.env` file if using Docker.

| Variable Name           | Description                               |
|--------------------------|------------------------------------------|
| `RABBITMQ_URL`         | RabbitMQ endpoint        |
| `RABBITMQ_PASS`       | RabbitMQ password       |
| `RABBITMQ_USER`       | RabbitMQ user       |
| `ADOBEORDS_USER`      | Adobe ORDS user    |
| `ADOBEORDS_PASS`      | Adobe ORDS password   |
| `ADOBEORDS_BASE_URL`  | Adobe ORDS endpoint (should end ../adobeords/web/) |
| `AEM_REPORT_SRV_URL`  | Adobe Report Server endpoint |
| `AEM_REPORT_SRV_APPID`  | Adobe Report Server AppId name  |
| `MAILIT_USER`              | Mail it service user   |
| `MAILIT_PASS`              | Mail it service password    |
| `MAILIT_URL`              | Mail it service endpoint   |
| `DO_NOT_REPLY_ADDRESS`  | Do not replay address    |
| `APPEALS_REGISTRY_EMAIL` | RSBC Appeal Registry email address  |
| `EMAIL_BCC1`              | BCC 1 (optional)    |
| `EMAIL_BCC2`              | BCC 2 (optional)   |
| `SPRING_ACTIVE_PROFILE` | Spring profile ('default' if not supplied)     |
| `LOGGING_LEVEL` | Springboot logging level (e.g., `DEBUG`, `INFO`)     |
| `HTTP_LISTENER_USER`              | Http Listener user   |
| `HTTP_LISTENER_PASS`              | Http Listener password    |

**All variables except those marked optional are required for the application to start and
function correctly**.  

---

## Run the application locally using Docker
You can run the application locally using Docker once an environmental variables list 
has been added to a new .env file. 

- Copy the supplied .env.template file to a .env file. 

- Customize your environmental variables in the new .env file.  

- Launch the containerized application  

```bash
docker-compose up --build
```
**Note: If RabbitMQ is also containerized, you may have to create a common network and attach otherwise each container
is isolated from the other.  

---

## Deployment

### Pipelines
🚧 **To be Determined**  
Continuous Integration and Deployment (CI/CD) pipelines for this service are under development. Future updates will include instructions on automated deployment.

---

## Additional Information for Developers
- This service is structured as a typical Spring Boot application.
- Unit and integration tests can be found under the `src/test` directory.
- Logging is configured via `application.properties` or `application-splunk.properties`.

---

## License
This project is licensed under the [Apache License 2.0](../../../../LICENSE).
