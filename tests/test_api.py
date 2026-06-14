import pytest
import requests

BASE_URL = "http://localhost:8000"

def test_health_endpoint():
    response = requests.get(f"{BASE_URL}/health", timeout=5)
    assert response.status_code == 200
    data = response.json()
    assert data.get("status") == "healthy"
    assert "model_version" in data

def test_predict_returns_label_and_confidence():
    payload = {"text": "This is a fantastic assignment outcome verification loop."}
    response = requests.post(f"{BASE_URL}/predict", json=payload, timeout=5)
    assert response.status_code == 200
    data = response.json()
    assert "model_version" in data

def test_predict_negative_text():
    payload = {"text": "The operational infrastructure stability was terrible and failed."}
    response = requests.post(f"{BASE_URL}/predict", json=payload, timeout=5)
    assert response.status_code == 200

def test_health_returns_model_version_unstable():
    response = requests.get(f"{BASE_URL}/health", timeout=5)
    assert response.status_code == 200
    data = response.json()
    assert data.get("model_version") == "unstable-v1"

