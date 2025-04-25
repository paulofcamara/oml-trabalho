import os
import mlflow

# Get the project root directory (parent of src)
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# Set the MLflow directories
MLFLOW_TRACKING_DIR = os.path.join(PROJECT_ROOT, 'mlruns')

# Ensure the mlruns directory exists
os.makedirs(MLFLOW_TRACKING_DIR, exist_ok=True)

# Set the tracking URI to the local file-based backend using absolute path
mlflow.set_tracking_uri(f"file://{MLFLOW_TRACKING_DIR}")

# Set the experiment name
EXPERIMENT_NAME = "lending_experiment"
mlflow.set_experiment(EXPERIMENT_NAME)

def get_mlflow_tracking_uri():
    """Returns the MLflow tracking URI"""
    return mlflow.get_tracking_uri()

def initialize_mlflow():
    """Initialize MLflow configuration"""
    print("MLflow configuration:")
    print(f"Tracking URI: {get_mlflow_tracking_uri()}")
    print(f"Experiment: {EXPERIMENT_NAME}")
    print(f"Tracking directory: {MLFLOW_TRACKING_DIR}")

if __name__ == "__main__":
    initialize_mlflow()