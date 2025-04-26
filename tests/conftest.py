import pytest
from unittest.mock import patch, MagicMock

@pytest.fixture(autouse=True)
def mock_environment():
    """Mock both MLflow and config for all tests"""
    mock_config = {
        "model": {
            "name": "bank_lending_model",
            "stage": "Production",
            "version": None
        },
        "mlflow": {
            "tracking_uri": "http://localhost:5000"  # Use localhost for tests
        },
        "server": {
            "host": "0.0.0.0",
            "port": 8000
        }
    }
    
    mock_model = MagicMock()
    mock_model.predict_proba.return_value = [[0.3, 0.7]]
    
    with patch('src.mlflow_initializer.load_config', return_value=mock_config), \
         patch('src.prediction_service.load_config', return_value=mock_config), \
         patch('mlflow.set_tracking_uri') as mock_uri, \
         patch('mlflow.get_experiment_by_name') as mock_get_exp, \
         patch('mlflow.set_experiment') as mock_set_exp, \
         patch('mlflow.pyfunc.load_model', return_value=mock_model):
        
        mock_exp = MagicMock()
        mock_exp.experiment_id = '1'
        mock_get_exp.return_value = mock_exp
        
        yield