import pytest
import requests
from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_health_check():
    """Test the health check endpoint"""
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert data["status"] == "healthy"

def test_root_endpoint():
    """Test the root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data

def test_scrape_endpoint_invalid_url():
    """Test scraping with invalid URL"""
    response = client.post("/api/scrape", json={
        "url": "invalid-url",
        "login_enabled": False
    })
    assert response.status_code == 400

def test_scrape_endpoint_missing_url():
    """Test scraping without URL"""
    response = client.post("/api/scrape", json={
        "login_enabled": False
    })
    assert response.status_code == 422  # Validation error

def test_scrape_endpoint_login_missing_fields():
    """Test scraping with login enabled but missing credentials"""
    response = client.post("/api/scrape", json={
        "url": "https://example.com",
        "login_enabled": True,
        "login_url": "https://example.com/login"
        # Missing username and password
    })
    assert response.status_code == 422  # Validation error

if __name__ == "__main__":
    pytest.main([__file__]) 