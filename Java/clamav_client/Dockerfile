# Maven/Springboot build container 

FROM maven:3.8.3-openjdk-17 AS maven_build

COPY pom.xml /tmp/

COPY clamav-client-spec.yaml /tmp/

COPY src /tmp/src/

WORKDIR /tmp/
	
RUN mvn clean package -Dmaven.test.skip=true

FROM eclipse-temurin:17-jre-alpine

EXPOSE 8080

WORKDIR /app/

RUN chgrp -R 0 /app && chmod -R g=u /app

COPY --from=maven_build /tmp/target/clamav_client-0.0.1-SNAPSHOT.jar /app/clamav_client-0.0.1-SNAPSHOT.jar

CMD ["java", "-jar", "/app/clamav_client-0.0.1-SNAPSHOT.jar"]