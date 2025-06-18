# Maven/Springboot build container 

FROM maven:3.9.9-eclipse-temurin-21 AS maven_build

ENV RABBITMQ_URL=$RABBITMQ_URL
ENV RABBITMQ_USER=$RABBITMQ_USER
ENV RABBITMQ_PASS=$RABBITMQ_PASS

COPY pom.xml /tmp/

COPY src /tmp/src/

WORKDIR /tmp/
	
RUN mvn clean package -Dmaven.test.skip=true

FROM eclipse-temurin:21

# RUN useradd -m appuser
# USER appuser

EXPOSE 8080

WORKDIR /app/

COPY --from=maven_build /tmp/target/pdf-gen-service-0.0.1-SNAPSHOT.jar /app/pdf-gen-service-0.0.1-SNAPSHOT.jar

CMD ["java", "-jar", "/app/pdf-gen-service-0.0.1-SNAPSHOT.jar"]