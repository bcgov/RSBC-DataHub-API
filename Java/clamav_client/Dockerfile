# Maven/Springboot build container 

FROM maven:3.8.3-openjdk-17 AS maven_build

ENV CLAMAV_CLIENT_PORT=$CLAMAV_CLIENT_PORT
ENV CLAMAV_CLIENT_HOST=$CLAMAV_CLIENT_HOST
ENV CLAMAV_CLIENT_TIMEOUT=$CLAMAV_CLIENT_TIMEOUT
ENV CLAMAV_CLIENT_BASIC_AUTH_USER=$CLAMAV_CLIENT_BASIC_AUTH_USER
ENV CLAMAV_CLIENT_BASIC_AUTH=$CLAMAV_CLIENT_BASIC_AUTH

COPY pom.xml /tmp/

COPY clamav-client-spec.yaml /tmp/

COPY src /tmp/src/

WORKDIR /tmp/
	
RUN mvn clean package -Dmaven.test.skip=true

FROM eclipse-temurin:17-jre-alpine

# RUN useradd -m appuser
# USER appuser

EXPOSE 8080

WORKDIR /app/

COPY --from=maven_build /tmp/target/clamav_client-0.0.1-SNAPSHOT.jar /app/clamav_client-0.0.1-SNAPSHOT.jar

CMD ["java", "-jar", "/app/clamav_client-0.0.1-SNAPSHOT.jar"]