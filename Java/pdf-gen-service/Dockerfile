# Maven/Springboot build container 

FROM maven:3.9.9-eclipse-temurin-21 AS maven_build

COPY pom.xml /tmp/

COPY src /tmp/src/

WORKDIR /tmp/

RUN mvn clean package -Dmaven.test.skip=true

# running the service

FROM eclipse-temurin:23-jre-alpine

USER nonroot

COPY --from=maven_build /tmp/target/pdf-gen-service-*.jar /app/service.jar

EXPOSE 8080

CMD ["java", "-jar", "/app/service.jar"]