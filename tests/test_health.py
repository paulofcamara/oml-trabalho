from fastapi.testclient import TestClient
import pytest
import traceback
import sys

def test_health_check():
    """Test the health check endpoint"""
    try:
        from src.prediction_service import app
        client = TestClient(app)
        response = client.get("/health")
        print(f"Response: {response.json()}")  # Debug print
        assert response.status_code == 200
        assert response.json() == {
            "status": "healthy",
            "model": "bank_lending_model"
        }
    except Exception as e:
        print("Exception occurred:")
        print(str(e))
        traceback.print_exc(file=sys.stdout)
        raise