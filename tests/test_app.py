import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_index_page(client):
    """Test that the index page loads correctly"""
    response = client.get('/')
    assert response.status_code == 200
    assert b'House Price Predictor' in response.data

def test_about_page(client):
    """Test that the about page loads correctly"""
    response = client.get('/about')
    assert response.status_code == 200
    assert b'About the Project' in response.data

def test_contact_page(client):
    """Test that the contact page loads correctly"""
    response = client.get('/contact')
    assert response.status_code == 200
    assert b'Contact Information' in response.data

def test_prediction_endpoint(client):
    """Test the prediction endpoint with valid data"""
    test_data = {
        'bedrooms': '3',
        'bathrooms': '2',
        'floors': '2',
        'yr_built': '2000'
    }
    response = client.post('/predict', data=test_data)
    assert response.status_code == 302  # Redirect after successful prediction

def test_prediction_invalid_data(client):
    """Test the prediction endpoint with invalid data"""
    test_data = {
        'bedrooms': 'invalid',
        'bathrooms': '2',
        'floors': '2',
        'yr_built': '2000'
    }
    response = client.post('/predict', data=test_data)
    assert response.status_code == 302  # Redirect after failed prediction 