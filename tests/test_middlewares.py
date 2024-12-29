 
import pytest
from main import create_app
from unittest.mock import patch
import jwt
import os

SECRET_KEY = "test_secret"

@pytest.fixture
def client():
    app = create_app('testing')
    with app.test_client() as client:
        yield client

def generate_token(expired=False):
    payload = {"user_id": 1}
    if expired:
        payload['exp'] = 0  # Token expirado
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

def test_token_missing(client):
    response = client.get('/protected')
    assert response.status_code == 401
    assert response.get_json()["message"] == "Token is missing!"

def test_token_invalid(client):
    response = client.get('/protected', headers={"Authorization": "Bearer invalid_token"})
    assert response.status_code == 401
    assert response.get_json()["message"] == "Invalid Token!"

def test_token_expired(client):
    expired_token = generate_token(expired=True)
    response = client.get('/protected', headers={"Authorization": f"Bearer {expired_token}"})
    assert response.status_code == 401
    assert response.get_json()["message"] == "Token has expired!"

def test_valid_token(client):
    valid_token = generate_token()
    response = client.get('/protected', headers={"Authorization": f"Bearer {valid_token}"})
    assert response.status_code == 200
