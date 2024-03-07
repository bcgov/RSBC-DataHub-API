# Maven/Springboot build container 

FROM maven:3.8.3-openjdk-17 AS build

ENV EMAIL_HOST=${EMAIL_HOST}
ENV EMAIL_PORT=${EMAIL_PORT}
ENV USER=${USER}
ENV PASSWORD=${PASSWORD}

COPY mail-it/pom.xml /tmp/

COPY mail-it/mail-it-api.yaml /tmp/

COPY mail-it/src /tmp/src/

WORKDIR /tmp/

RUN mvn clean package -Dmaven.test.skip=true

# running the service

FROM openjdk:17-jdk-slim

RUN useradd -m appuser

USER appuser

COPY --from=build /tmp/target/mail-it-*.jar /app/service.jar

CMD ["java", "-jar", "/app/service.jar"]
