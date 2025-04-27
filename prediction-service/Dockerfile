FROM openjdk:17-jdk-slim
WORKDIR /app
COPY ./prediction-service/target/*.jar app.jar
CMD ["java", "-jar", "app.jar"]
EXPOSE 8080
ENTRYPOINT ["java","-jar","/app/app.jar"]