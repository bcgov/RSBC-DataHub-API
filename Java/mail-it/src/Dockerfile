#############################################################################################
###              Stage where Docker is building spring boot app using maven               ###
#############################################################################################
FROM maven:3.8.3-openjdk-17 as build

ARG MVN_PROFILE=default
ARG SERVICE_NAME=mail-it
ARG SKIP_TESTS=false

ENV SERVICE_NAME=${SERVICE_NAME}

# install skywalking agent
# WORKDIR /skywalking

# RUN wget https://mirror.its.dal.ca/apache/skywalking/$SW_V/apache-skywalking-apm-$SW_V.tar.gz && \
#     tar -xzvf apache-skywalking-apm-$SW_V.tar.gz && \
#     rm apache-skywalking-apm-$SW_V.tar.gz

# add spring boot plugin
# RUN mv apache-skywalking-apm-bin/agent/optional-plugins/apm-spring-annotation-plugin-8.4.0.jar apache-skywalking-apm-bin/agent/plugins/apm-spring-annotation-plugin-8.4.0.jar

WORKDIR /

COPY . .

RUN mvn -B clean install \
        -P ${MVN_PROFILE} \
        -Dmaven.test.skip=${SKIP_TESTS} \
        -f mail-it/pom.xml

#############################################################################################

#############################################################################################
### Stage where Docker is running a java process to run a service built in previous stage ###
#############################################################################################
FROM openjdk:17-jdk-slim

# ARG MVN_PROFILES
ARG SERVICE_NAME=mail-it

# COPY --from=build ./skywalking/apache-skywalking-apm-bin/agent /app/agent

COPY --from=build ./${SERVICE_NAME}/target/${SERVICE_NAME}-*.jar /app/service.jar

# CMD ["java", "-javaagent:/app/agent/skywalking-agent.jar", "-jar", "/app/service.jar"]
CMD ["java", "-jar", "/app/service.jar"]

#############################################################################################
