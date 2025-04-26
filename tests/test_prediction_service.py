import logging
from unittest.mock import patch, Mock
from fastapi.testclient import TestClient
from fastapi import HTTPException
import pytest
from src.prediction_service import app

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

client = TestClient(app)

def test_health_check():
    """Test the health check endpoint"""
    logger.debug("Running health check test")
    response = client.get("/health")
    logger.debug(f"Health check response: {response.json()}")
    assert response.status_code == 200
    assert response.json() == {
        "status": "healthy",
        "model": "bank_lending_model"
    }

def test_predict_endpoint():
    """Test the prediction endpoint with sample data"""
    logger.debug("Running prediction test")
    test_features = {
        "features": {
            "person_age": 30.0,
            "person_income": 60000.0,
            "person_emp_length": 5.0,
            "loan_amnt": 10000.0,
            "loan_int_rate": 10.5,
            "loan_percent_income": 0.15,
            "cb_person_cred_hist_length": 10.0
        }
    }
    
    try:
        response = client.post("/predict", json=test_features)
        logger.debug(f"Prediction response: {response.json()}")
    except Exception as e:
        logger.error(f"Error during prediction: {str(e)}")
        raise
        
    assert response.status_code == 200
    
    # Check response structure
    result = response.json()
    assert "prediction" in result
    assert "probability" in result
    assert "threshold" in result
    
    # Check data types
    assert isinstance(result["prediction"], int)
    assert isinstance(result["probability"], float)
    assert isinstance(result["threshold"], float)
    assert result["threshold"] == 0.5
    # Since we mocked probability as 0.7, prediction should be 1
    assert result["prediction"] == 1
    assert abs(result["probability"] - 0.7) < 0.001  # Check probability with tolerance

def test_predict_invalid_input():
    """Test the prediction endpoint with invalid input data"""
    logger.debug("Running invalid input prediction test")
    
    # Test with missing required feature
    invalid_features = {
        "features": {
            "person_age": 30.0,
            # Missing person_income
            "person_emp_length": 5.0,
            "loan_amnt": 10000.0,
            "loan_int_rate": 10.5,
            "loan_percent_income": 0.15,
            "cb_person_cred_hist_length": 10.0
        }
    }
    
    response = client.post("/predict", json=invalid_features)
    assert response.status_code == 422  # FastAPI validation error status code
    error_detail = response.json()["detail"]
    assert "Missing required features" in str(error_detail)
    assert "person_income" in str(error_detail)
    
    # Test with invalid data types
    invalid_types = {
        "features": {
            "person_age": "invalid",  # String instead of float
            "person_income": 60000.0,
            "person_emp_length": 5.0,
            "loan_amnt": 10000.0,
            "loan_int_rate": 10.5,
            "loan_percent_income": 0.15,
            "cb_person_cred_hist_length": 10.0
        }
    }
    
    response = client.post("/predict", json=invalid_types)
    assert response.status_code == 422
    error_detail = response.json()["detail"]
    assert "Input should be a valid number" in str(error_detail)
    assert "unable to parse string as a number" in str(error_detail)
    
    # Test with invalid ranges
    invalid_ranges = {
        "features": {
            "person_age": 150.0,  # Age too high
            "person_income": 60000.0,
            "person_emp_length": 5.0,
            "loan_amnt": 10000.0,
            "loan_int_rate": 10.5,
            "loan_percent_income": 0.15,
            "cb_person_cred_hist_length": 10.0
        }
    }
    
    response = client.post("/predict", json=invalid_ranges)
    assert response.status_code == 422
    error_detail = response.json()["detail"]
    assert "Age must be between" in str(error_detail)

def test_predict_boundary_values():
    """Test the prediction endpoint with boundary values"""
    logger.debug("Running boundary values prediction test")
    
    # Test with extreme age value
    boundary_features = {
        "features": {
            "person_age": 100.0,  # Extreme age
            "person_income": 1000000.0,  # High income
            "person_emp_length": 50.0,  # Long employment
            "loan_amnt": 1000000.0,  # Large loan
            "loan_int_rate": 30.0,  # High interest
            "loan_percent_income": 0.99,  # High debt-to-income
            "cb_person_cred_hist_length": 50.0  # Long credit history
        }
    }
    
    response = client.post("/predict", json=boundary_features)
    assert response.status_code == 200
    result = response.json()
    assert isinstance(result["prediction"], int)
    assert isinstance(result["probability"], float)
    assert 0 <= result["probability"] <= 1  # Probability should be between 0 and 1

    # Test with minimum values
    min_features = {
        "features": {
            "person_age": 18.0,  # Minimum legal age
            "person_income": 0.0,  # No income
            "person_emp_length": 0.0,  # No employment history
            "loan_amnt": 100.0,  # Small loan
            "loan_int_rate": 1.0,  # Low interest
            "loan_percent_income": 0.0,  # No debt-to-income
            "cb_person_cred_hist_length": 0.0  # No credit history
        }
    }
    
    response = client.post("/predict", json=min_features)
    assert response.status_code == 200
    result = response.json()
    assert isinstance(result["prediction"], int)
    assert isinstance(result["probability"], float)
    assert 0 <= result["probability"] <= 1

@patch('src.prediction_service.load_production_model')
def test_model_loading(mock_load_model):
    """Test model loading mechanism"""
    logger.debug("Running model loading test")
    
    # Create a mock model with predict_proba method
    mock_predictor = Mock()
    mock_predictor.predict_proba.return_value = [[0.3, 0.7]]  # Mock prediction probabilities
    mock_load_model.return_value = mock_predictor
    
    # Reset model to None to force loading
    import src.prediction_service
    src.prediction_service.model = None
    
    test_features = {
        "features": {
            "person_age": 30.0,
            "person_income": 60000.0,
            "person_emp_length": 5.0,
            "loan_amnt": 10000.0,
            "loan_int_rate": 10.5,
            "loan_percent_income": 0.15,
            "cb_person_cred_hist_length": 10.0
        }
    }
    
    # First request should trigger model loading
    response = client.post("/predict", json=test_features)
    assert response.status_code == 200
    mock_load_model.assert_called_once()
    assert src.prediction_service.model is not None

@patch('src.prediction_service.ensure_model_loaded', side_effect=Exception("MLflow connection error"))
def test_mlflow_connection_error(mock_ensure_model):
    """Test behavior when MLflow connection fails"""
    logger.debug("Running MLflow connection error test")
    
    # Reset model to None to force reinitialization
    import src.prediction_service
    src.prediction_service.model = None
    
    test_features = {
        "features": {
            "person_age": 30.0,
            "person_income": 60000.0,
            "person_emp_length": 5.0,
            "loan_amnt": 10000.0,
            "loan_int_rate": 10.5,
            "loan_percent_income": 0.15,
            "cb_person_cred_hist_length": 10.0
        }
    }
    
    response = client.post("/predict", json=test_features)
    assert response.status_code == 500
    assert "MLflow connection error" in str(response.json()["detail"])