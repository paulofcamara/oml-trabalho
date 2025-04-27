#!/bin/bash
set -e  # Exit on any error

echo "Starting build process..."

echo "Cleaning unnecessary files..."
# Clean Maven target directories
find . -type d -name "target" -exec rm -rf {} +
# Clean temporary files
find . -type f -name "*.log" -delete
find . -type f -name "*.tmp" -delete
find . -type f -name "*~" -delete
# Clean IDE specific files
find . -type d -name ".idea" -exec rm -rf {} +
find . -type f -name "*.iml" -delete
find . -type d -name ".vscode" -exec rm -rf {} +
find . -type f -name ".DS_Store" -delete

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
