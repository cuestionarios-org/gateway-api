import pytest
from main import create_app
from unittest.mock import patch
import jwt
from src.config.config import TestingConfig


# 📌 FIXTURE: Cliente de Pruebas
@pytest.fixture
def client():
    app = create_app('testing')
    with app.test_client() as client:
        yield client


# 📌 Generar Token de Pruebas
def generate_token(expired=False):
    payload = {"email": "fom6@test.com", "password": "1234"}
    if expired:
        payload['exp'] = 0  # Token expirado
    return jwt.encode(payload, TestingConfig.JWT_SECRET_KEY, algorithm="HS256")


# ✅ Test de Token Faltante
def test_token_missing(client):
    response = client.get('/auth/protected')
    assert response.status_code == 401
    assert response.get_json()["message"] == "Token is missing!"


# ✅ Test de Token Inválido
def test_token_invalid(client):
    response = client.get('/auth/protected', headers={"Authorization": "Bearer invalid_token"})
    assert response.status_code == 401
    assert response.get_json()["message"] == "Token is invalid!"


# ✅ Test de Token Expirado
def test_token_expired(client):
    expired_token = generate_token(expired=True)
    response = client.get('/auth/protected', headers={"Authorization": f"Bearer {expired_token}"})
    assert response.status_code == 401
    assert response.get_json()["message"] == "Token is invalid!"


# ✅ Test de Token Válido
@patch('services.auth_service.AuthService.login')
def test_valid_token(mock_login, client):
    # Mockear el login
    mock_login.return_value = ({"access_token": "valid_test_token"}, 200)

    response = client.post('/auth/login', json={"email": "test@example.com", "password": "test"})
    assert response.status_code == 200
    token = response.get_json().get('access_token')

    # Mockear la validación del token
    with patch('services.auth_service.AuthService.protected_route') as mock_protected:
        mock_protected.return_value = ({"user_id": 1, "username": "test_user"}, 200)
        
        protected_response = client.get('/auth/protected', headers={"Authorization": f"Bearer {token}"})
        assert protected_response.status_code == 200
        assert protected_response.get_json()["username"] == "test_user"
