import pytest
import json
from app import app

@pytest.fixture
def client():
    """Create a test client for the Flask app"""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_home_endpoint(client):
    """Test the home page endpoint"""
    response = client.get('/')
    assert response.status_code == 200
    assert b'CI/CD Pipeline Demo' in response.data
    assert b'Deployed successfully' in response.data

def test_health_endpoint(client):
    """Test the health check endpoint"""
    response = client.get('/health')
    assert response.status_code == 200
    
    data = json.loads(response.data)
    assert 'status' in data
    assert data['status'] == 'healthy'
    assert 'service' in data
    assert data['service'] == 'cicd-demo-app'
    assert 'timestamp' in data

def test_info_endpoint(client):
    """Test the info endpoint"""
    response = client.get('/info')
    assert response.status_code == 200
    
    data = json.loads(response.data)
    assert 'application' in data
    assert data['application'] == 'CI/CD Pipeline Demo'
    assert 'version' in data
    assert 'hostname' in data
    assert 'endpoints' in data
    assert len(data['endpoints']) == 3

def test_health_endpoint_returns_json(client):
    """Verify health endpoint returns JSON content type"""
    response = client.get('/health')
    assert response.content_type == 'application/json'

def test_info_endpoint_returns_json(client):
    """Verify info endpoint returns JSON content type"""
    response = client.get('/info')
    assert response.content_type == 'application/json'

def test_invalid_endpoint(client):
    """Test that invalid endpoints return 404"""
    response = client.get('/invalid')
    assert response.status_code == 404
