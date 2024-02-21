# Maven/Springboot build container 

FROM maven:3.8.4-openjdk-17 AS maven_build
# Create the working directory and copy over the POM
COPY pom.xml /tmp/
# Copy the sources
COPY src /tmp/src/
# Set the working DIR in maven_build
WORKDIR /tmp/
# Build the war file. 
RUN mvn clean package -Dmaven.test.skip=true
# Pull base image
FROM eclipse-temurin:17
# Expose port 8080
EXPOSE 8080
# Copy hello world to docker image from builder image
COPY --from=maven_build /tmp/target/clamav_client-0.0.1-SNAPSHOT.jar /app/clamav_client-0.0.1-SNAPSHOT.jar
# Default command to start the war
# CMD java -jar /app/clamav_client-0.0.1-SNAPSHOT.jar
CMD ["java", "-jar", "/app/clamav_client-0.0.1-SNAPSHOT.jar"]