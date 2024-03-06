# Maven/Springboot build container 

FROM maven:3.8.3-openjdk-17 AS maven_build

COPY pom.xml /tmp/

COPY clamav-client-spec.yaml /tmp/

COPY src /tmp/src/

WORKDIR /tmp/
	
RUN mvn clean package -Dmaven.test.skip=true

FROM openjdk:17-jdk-slim

RUN useradd -m appuser

USER appuser

EXPOSE 8080

WORKDIR /app/

COPY --from=maven_build /tmp/target/clamav_client-0.0.1-SNAPSHOT.jar /app/clamav_client-0.0.1-SNAPSHOT.jar

CMD ["java", "-jar", "/app/clamav_client-0.0.1-SNAPSHOT.jar"]
