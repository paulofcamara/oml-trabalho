#!/bin/bash
set -e  # Exit on any error

echo "Starting build process..."

# Check if we're in the right directory
if [ ! -d "prediction-service" ]; then
    echo "Error: prediction-service directory not found!"
    exit 1
fi

echo "Building prediction-service..."
cd prediction-service
mvn clean package -B  # -B for non-interactive (batch) mode

echo "Building Docker image..."
cd ..
docker build -t prediction-service .

echo "Build completed successfully!"
