import pytest
from main import create_app
from unittest.mock import patch

# 📌 FIXTURE: Cliente de Pruebas
@pytest.fixture
def client():
    app = create_app('testing')
    with app.test_client() as client:
        yield client


# ✅ Test de Login Exitoso
@patch('services.auth_service.AuthService.login')
def test_login_success(mock_login, client):
    mock_login.return_value = ({"access_token": "fake_token"}, 200)

    response = client.post('/auth/login', json={"email": "fom6@test.com", "password": "1234"})
    assert response.status_code == 200
    assert "access_token" in response.get_json()


# ✅ Test de Login Fallido
@patch('services.auth_service.AuthService.login')
def test_login_failure(mock_login, client):
    mock_login.return_value = ({"message": "Invalid credentials"}, 401)

    response = client.post('/auth/login', json={"email": "wrong", "password": "wrong"})
    assert response.status_code == 401
    assert response.get_json()["message"] == "Invalid credentials"


# ✅ Test de Registro Exitoso
@patch('services.auth_service.AuthService.register')
def test_register_success(mock_register, client):
    mock_register.return_value = ({"message": "User registered"}, 201)

    response = client.post('/auth/register', json={"username": "newuser", "password": "password"})
    assert response.status_code == 201
    assert response.get_json()["message"] == "User registered"


# ✅ Test de Registro con Datos Incompletos (Mockeado)
@patch('services.auth_service.AuthService.register')
def test_register_incomplete_data(mock_register, client):
    # Simula una respuesta de error con datos incompletos
    mock_register.return_value = ({"message": "Incomplete data"}, 400)
    
    response = client.post('/auth/register', json={"username": "newuser"})
    assert response.status_code == 400
    assert response.get_json()["message"] == "Incomplete data"


# ✅ Test de Ruta Protegida sin Token
def test_protected_route_without_token(client):
    response = client.get('/auth/protected')
    assert response.status_code == 401
    assert response.get_json()["message"] == "Token is missing!"
