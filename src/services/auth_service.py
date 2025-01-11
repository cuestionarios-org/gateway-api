import requests
import jwt
import os
from config.config import Config

class AuthService:
    AUTH_URL = os.getenv('AUTH_SERVICE_URL')
    AUTH_USER_URL = os.getenv('AUTH_USER_URL')

    @staticmethod
    def login(payload):
        response = requests.post(f"{AuthService.AUTH_URL}/login", json=payload)
        return response.json(), response.status_code

    @staticmethod
    def register(payload):
        response = requests.post(f"{AuthService.AUTH_URL}/register", json=payload)
        return response.json(), response.status_code
    
    @staticmethod
    def list_users(token):
        try:
            # Decode and validate the token
            token = token.split("Bearer ")[1]
            data = jwt.decode(token, Config.JWT_SECRET_KEY, algorithms=["HS256"])
            role = data.get("role")

            if role not in ["admin", "moderator"]:
                return {"message": "No tienes permisos para acceder a este recurso."}, 403

            # Make the request to the auth service
            headers = {"Authorization": f"Bearer {token}"}
            response = requests.get(f"{AuthService.AUTH_USER_URL}/list", headers=headers)
            return response.json(), response.status_code
        except jwt.ExpiredSignatureError:
            return {"message": "El token ha expirado."}, 401
        except jwt.InvalidTokenError as e:
            return {"message": "Token inválido.", "error": str(e)}, 401
        except Exception as e:
            return {"message": "Error al procesar la solicitud.", "error": str(e)}, 500
        
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