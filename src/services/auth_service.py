import requests
import os

class AuthService:
    AUTH_URL = os.getenv('AUTH_SERVICE_URL')

    @staticmethod
    def login(payload):
        response = requests.post(f"{AuthService.AUTH_URL}/login", json=payload)
        return response.json(), response.status_code

    @staticmethod
    def register(payload):
        response = requests.post(f"{AuthService.AUTH_URL}/register", json=payload)
        return response.json(), response.status_code
