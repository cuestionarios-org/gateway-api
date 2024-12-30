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
    
    @staticmethod
    def protected_route(token):
        from src.config.config import Config
        import jwt

        try:
            token = token.split("Bearer ")[1]
            data = jwt.decode(token, Config.JWT_SECRET_KEY, algorithms=["HS256"])
            return {"message": "Token válido", "user_id": data['user_id']}, 200
        except Exception as e:
            return {"message": "Token is invalid!", "error": str(e)}, 401