import os
import mlflow

# Set the tracking URI to the local file-based backend
mlflow.set_tracking_uri("../mlruns")

# Set the experiment name
mlflow.set_experiment("lending_experiment")

# Start the MLflow server (if needed, this can be run separately)
# Command: mlflow ui --backend-store-uri file://<path-to-mlruns> --default-artifact-root file://<path-to-mlruns>
print("MLflow tracking URI set to:", mlflow.get_tracking_uri())