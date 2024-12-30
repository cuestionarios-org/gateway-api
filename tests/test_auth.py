import pytest
from main import create_app

@pytest.fixture
def client():
    app = create_app('testing')
    with app.test_client() as client:
        yield client

def test_login_success(client, mocker):
    mocker.patch('services.auth_service.AuthService.login', return_value=({"access_token": "fake_token"}, 200))
    response = client.post('/auth/login', json={"email": "fom6@test.com", "password": "1234"})
    assert response.status_code == 200
    assert "access_token" in response.get_json()

def test_login_failure(client, mocker):
    mocker.patch('services.auth_service.AuthService.login', return_value=({"message": "Invalid credentials"}, 401))
    response = client.post('/auth/login', json={"email": "wrong", "password": "wrong"})
    assert response.status_code == 401
    assert response.get_json()["message"] == "Invalid credentials"

def test_register_success(client, mocker):
    mocker.patch('services.auth_service.AuthService.register', return_value=({"message": "User registered"}, 201))
    response = client.post('/auth/register', json={"username": "newuser", "password": "password"})
    assert response.status_code == 201
    assert response.get_json()["message"] == "User registered"

def test_register_incomplete_data(client):
    response = client.post('/auth/register', json={"username": "newuser"})
    assert response.status_code == 500 # todo 400

# Modificar cuando tengamos una ruta protegida real
def test_protected_route_without_token(client):
    response = client.get('/auth/protected')
    assert response.status_code == 401  # Código de estado correcto
    json_data = response.get_json()
    assert json_data is not None
    assert json_data["message"] == "Token is missing!"

