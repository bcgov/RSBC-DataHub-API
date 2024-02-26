#############################################################################################
###              Stage where Docker is building spring boot app using maven               ###
#############################################################################################
FROM maven:3.8.3-openjdk-17 as build

ARG MVN_PROFILE=default
ARG SERVICE_NAME=mail-it
ARG SKIP_TESTS=false

ENV SERVICE_NAME=${SERVICE_NAME}

COPY mail-it/pom.xml /tmp/

COPY mail-it/mail-it-api.yaml /tmp/

COPY mail-it/src /tmp/src/

WORKDIR /tmp/

RUN mvn -B clean install \
        -P ${MVN_PROFILE} \
        -Dmaven.test.skip=${SKIP_TESTS} \
        -f pom.xml

#############################################################################################

#############################################################################################
### Stage where Docker is running a java process to run a service built in previous stage ###
#############################################################################################
FROM openjdk:17-jdk-slim

RUN useradd -m appuser

USER appuser

# ARG MVN_PROFILES
ARG SERVICE_NAME=mail-it

COPY --from=build /tmp/target/${SERVICE_NAME}-*.jar /app/service.jar

CMD ["java", "-jar", "/app/service.jar"]

#############################################################################################
