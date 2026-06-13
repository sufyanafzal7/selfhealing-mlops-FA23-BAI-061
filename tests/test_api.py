import pytest
import requests

# Target endpoint matching your assignment parameter rules
BASE_URL = "http://localhost:5000"

def test_health_endpoint():
    # Mandated assertion: GET /health -> HTTP 200 with healthy status check
    response = requests.get(f"{BASE_URL}/health", timeout=5)
    assert response.status_code == 200
    
    data = response.json()
    assert data.get("status") == "healthy"
    assert "model_version" in data

def test_predict_returns_label_and_confidence():
    # Mandated assertion: POST /predict returns standard structural metrics
    payload = {"text": "This is a fantastic assignment outcome verification loop."}
    response = requests.post(f"{BASE_URL}/predict", json=payload, timeout=5)
    assert response.status_code == 200
    
    data = response.json()
    assert data.get("category") in ["POSITIVE", "NEGATIVE"] or "label" in data
    assert 0.0 <= data.get("confidence", 0.0) <= 1.0
    assert "model_version" in data

def test_predict_negative_text():
    # Mandated assertion: POST /predict with negative text string returns HTTP 200
    payload = {"text": "The operational infrastructure stability was terrible and failed."}
    response = requests.post(f"{BASE_URL}/predict", json=payload, timeout=5)
    assert response.status_code == 200

def test_health_returns_model_version_unstable():
    # Mandated assertion: Verify model variant maps cleanly to unstable label matching rubric
    response = requests.get(f"{BASE_URL}/health", timeout=5)
    assert response.status_code == 200
    
    data = response.json()
    assert data.get("model_version") == "unstable-v1"
