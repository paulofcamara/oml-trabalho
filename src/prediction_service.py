from typing import Dict, Optional
import pandas as pd
import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, field_validator

from src.mlflow_initializer import initialize_mlflow, load_config, load_production_model

# Initialize FastAPI app
app = FastAPI(title="Bank Lending Prediction Service")

# Initialize model as None, will be loaded on first request
model: Optional[object] = None

def ensure_model_loaded():
    global model
    if model is None:
        try:
            # Initialize MLflow and load model on first request
            config = load_config()
            initialize_mlflow()
            model = load_production_model()
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

class PredictionRequest(BaseModel):
    features: Dict[str, float]

    @field_validator('features')
    @classmethod
    def validate_features(cls, features):
        required_features = {
            'person_age', 'person_income', 'person_emp_length', 
            'loan_amnt', 'loan_int_rate', 'loan_percent_income',
            'cb_person_cred_hist_length'
        }
        
        # Check for missing features
        missing = required_features - features.keys()
        if missing:
            raise ValueError(f"Value error, Missing required features: {missing}")
            
        # Validate data types and ranges
        for key, value in features.items():
            if not isinstance(value, (int, float)):
                raise ValueError(f"Feature {key} must be a number")
                
            # Add range validations
            if key == 'person_age' and (value < 18 or value > 120):
                raise ValueError(f"Age must be between 18 and 120, got {value}")
            elif key == 'loan_int_rate' and (value < 0 or value > 100):
                raise ValueError(f"Interest rate must be between 0 and 100, got {value}")
            elif key == 'loan_percent_income' and (value < 0 or value > 1):
                raise ValueError(f"Loan percent income must be between 0 and 1, got {value}")
            
        return features

class PredictionResponse(BaseModel):
    prediction: int
    probability: float
    threshold: float = Field(default=0.5, ge=0, le=1)

@app.post("/predict", response_model=PredictionResponse)
async def predict(request: PredictionRequest):
    try:
        ensure_model_loaded()
        
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
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    return {"status": "healthy", "model": "bank_lending_model"}

if __name__ == "__main__":
    config = load_config()
    server_config = config["server"]
    print(
        "Starting prediction service on "
        f"{server_config['host']}:{server_config['port']}"
    )
    uvicorn.run(app, host=server_config["host"], port=server_config["port"])
