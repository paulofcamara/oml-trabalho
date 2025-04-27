FROM openjdk:11-jre-slim

WORKDIR /app

# Copy the JAR file from the correct relative path
COPY ./prediction-service/target/*.jar app.jar

EXPOSE 8080

CMD ["java", "-jar", "app.jar"]
