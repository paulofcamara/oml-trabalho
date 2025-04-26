import pytest
from unittest.mock import patch, mock_open, MagicMock
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.mlflow_initializer import load_config, initialize_mlflow

def test_load_config():
    """Test loading configuration from file"""
    mock_config = '''{"mlflow": {"tracking_uri": "http://localhost:5000"},
                     "model": {"name": "bank_lending_model"},
                     "server": {"host": "0.0.0.0", "port": 8000}}'''
    
    with patch("builtins.open", mock_open(read_data=mock_config)):
        config = load_config()
        
        assert isinstance(config, dict)
        assert "mlflow" in config
        assert "tracking_uri" in config["mlflow"]
        assert config["model"]["name"] == "bank_lending_model"

@patch('mlflow.set_tracking_uri')
@patch('mlflow.get_experiment_by_name')
@patch('mlflow.set_experiment')
def test_initialize_mlflow(mock_set_experiment, mock_get_experiment, mock_set_tracking_uri):
    """Test MLflow initialization"""
    # Mock the experiment to simulate it already exists
    mock_experiment = MagicMock()
    mock_experiment.experiment_id = '1'
    mock_get_experiment.return_value = mock_experiment
    
    # Mock the config
    mock_config = {
        "mlflow": {"tracking_uri": "http://localhost:5000"},
        "model": {"name": "bank_lending_model"}
    }
    with patch("src.mlflow_initializer.load_config", return_value=mock_config):
        # Call the function
        experiment_id = initialize_mlflow()
        
        # Verify MLflow was properly initialized
        assert experiment_id == '1'
        mock_set_tracking_uri.assert_called_once_with("http://localhost:5000")
        mock_get_experiment.assert_called_once_with("bank_lending_prediction")
        mock_set_experiment.assert_called_once_with("bank_lending_prediction")

@patch('mlflow.set_tracking_uri')
def test_initialize_mlflow_missing_experiment(mock_set_tracking_uri):
    """Test MLflow initialization when experiment doesn't exist"""
    # Mock the experiment to simulate it doesn't exist
    with patch('mlflow.get_experiment_by_name', return_value=None):
        with patch('mlflow.create_experiment', return_value='2') as mock_create:
            # Mock the config
            mock_config = {
                "mlflow": {"tracking_uri": "http://localhost:5000"},
                "model": {"name": "bank_lending_model"}
            }
            with patch("src.mlflow_initializer.load_config", return_value=mock_config):
                # Call the function
                experiment_id = initialize_mlflow()
                
                # Verify MLflow created new experiment
                assert experiment_id == '2'
                mock_create.assert_called_once_with("bank_lending_prediction")

def test_load_config_file_not_found():
    """Test config loading when file is not found"""
    with patch("builtins.open", side_effect=FileNotFoundError):
        with pytest.raises(FileNotFoundError):
            load_config()

def test_load_config_invalid_json():
    """Test config loading with invalid JSON"""
    invalid_config = '''{invalid json'''
    
    with patch("builtins.open", mock_open(read_data=invalid_config)):
        with pytest.raises(Exception):
            load_config()

@patch('mlflow.set_tracking_uri')
def test_initialize_mlflow_connection_error(mock_set_tracking_uri):
    """Test MLflow initialization when connection fails"""
    # Mock connection error
    mock_set_tracking_uri.side_effect = Exception("Connection failed")
    
    # Mock the config
    mock_config = {
        "mlflow": {"tracking_uri": "http://localhost:5000"},
        "model": {"name": "bank_lending_model"}
    }
    with patch("src.mlflow_initializer.load_config", return_value=mock_config):
        with pytest.raises(Exception) as exc_info:
            initialize_mlflow()
        assert "Connection failed" in str(exc_info.value)

def test_load_config_required_fields():
    """Test config loading with missing required fields"""
    incomplete_config = '''{"mlflow": {}}'''  # Missing required fields
    
    with patch("builtins.open", mock_open(read_data=incomplete_config)):
        with pytest.raises(KeyError):
            config = load_config()
            _ = config["model"]["name"]  # This should raise KeyError