from typing import Dict

import pandas as pd
import uvicorn
from fastapi import FastAPI
from fastapi import HTTPException
from pydantic import BaseModel

from mlflow_initializer import initialize_mlflow
from mlflow_initializer import load_config
from mlflow_initializer import load_production_model

# Initialize FastAPI app
app = FastAPI(title="Bank Lending Prediction Service")

# Initialize MLflow and load model on startup
config = load_config()
initialize_mlflow()
model = load_production_model()


class PredictionRequest(BaseModel):
    features: Dict[str, float]


class PredictionResponse(BaseModel):
    prediction: int
    probability: float
    threshold: float = 0.5


@app.post("/predict", response_model=PredictionResponse)
async def predict(request: PredictionRequest):
    try:
        # Convert input features to DataFrame
        df = pd.DataFrame([request.features])

        # Make prediction
        prediction_proba = model.predict_proba(df)
        # Probability of positive class (1)
        probability = prediction_proba[0][1]
        prediction = int(probability >= 0.5)

        return PredictionResponse(
            prediction=prediction,
            probability=float(probability),
            threshold=0.5,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/health")
async def health_check():
    return {"status": "healthy", "model": "bank_lending_model"}


if __name__ == "__main__":
    server_config = config["server"]
    print(
        "Starting prediction service on "
        f"{server_config['host']}:{server_config['port']}"
    )
    uvicorn.run(app, host=server_config["host"], port=server_config["port"])
