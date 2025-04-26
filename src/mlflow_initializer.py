import json

import mlflow


def load_config():
    with open("config/app.json", "r") as f:
        return json.load(f)


def initialize_mlflow():
    # Load configuration
    config = load_config()

    # Configure MLflow to use our remote tracking server
    mlflow.set_tracking_uri(config["mlflow"]["tracking_uri"])

    # Set the experiment name
    experiment_name = "bank_lending_prediction"

    # Create or get the experiment
    experiment = mlflow.get_experiment_by_name(experiment_name)
    if experiment is None:
        experiment_id = mlflow.create_experiment(experiment_name)
    else:
        experiment_id = experiment.experiment_id

    # Set as active experiment
    mlflow.set_experiment(experiment_name)

    return experiment_id


def load_production_model():
    """
    Load the production model from MLflow model registry.
    """
    config = load_config()
    model_name = config["model"]["name"]

    # Load the model from the Model Registry
    model = mlflow.pyfunc.load_model(f"models:/{model_name}@Production")

    return model
