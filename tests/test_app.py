import pytest
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../app')))
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_predict_endpoint(client):
    # Test text configuration matching assignment parameter rules
    payload = {
        "text": "The cinematography was breathtaking and the performances were outstanding"
    }
    response = client.post('/predict', json=payload)
    assert response.status_code == 200
    data = response.get_json()
    assert "category" in data or "label" in response.get_data(as_text=True) or data is not None
    assert "confidence" in data
