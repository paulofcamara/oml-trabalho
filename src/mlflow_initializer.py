import json
import mlflow


def load_config():
    with open('config/app.json', 'r') as f:
        return json.load(f)


def initialize_mlflow():
    # Load configuration
    config = load_config()

    # Configure MLflow to use our remote tracking server
    mlflow.set_tracking_uri(config['mlflow']['tracking_uri'])

    # Set the experiment name
    EXPERIMENT_NAME = "bank_lending_prediction"

    # Create or get the experiment
    experiment = mlflow.get_experiment_by_name(EXPERIMENT_NAME)
    if experiment is None:
        experiment_id = mlflow.create_experiment(EXPERIMENT_NAME)
    else:
        experiment_id = experiment.experiment_id

    # Set as active experiment
    mlflow.set_experiment(EXPERIMENT_NAME)

    return experiment_id


def load_production_model():
    """
    Load the production model from MLflow model registry
    """
    config = load_config()
    model_name = config['model']['name']

    # Load the model from the Model Registry
    model = mlflow.pyfunc.load_model(f"models:/{model_name}@Production")

    return model