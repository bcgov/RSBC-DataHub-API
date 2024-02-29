# mail-it

A simple mail application (with attachment support)

Built for Java 17, Spring boot 3.2

## Maven

### Build All Componenets

```bash
mvn clean install
```

# Configuration
| Key                                 | Required | Value                              | Description                                                                                                                                                 |
| ----------------------------------- | :------: | ---------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------- |
| EMAIL_HOST                         |    x     | {mailhog}                | The email server recieving the emails  |
| EMAIL_PORT                         |    x     | {25}                | The email server port  |
| USER                         |    x     | {somename}                | Client sending emails user id.  |
| PASSWORD                         |    x     | {password}                | Client sending emails user password.  |



## Run locally in docker

```bash
docker-compose up
```

### Containers

#### mailhog (Fake) email service endpoint for development. 

A [mailhog](https://github.com/mailhog/MailHog) instance accessible at [http://localhost:8025/](http://localhost:8025/)

