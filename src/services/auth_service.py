import requests
import jwt
import os
from config.config import Config
from utils.logger import get_logger
logger = get_logger(__name__)


class AuthService:
    """
    Clase para interactuar con el servicio de autenticación.
    Contiene métodos para iniciar sesión, registrar usuarios y acceder a rutas protegidas.
    """
    # Formaciono de la URL del servicio de autenticación
    AUTH_SERVICE_URL ='http://' + os.getenv('AUTH_HOST','localhost') + ':' + os.getenv('AUTH_PORT','5011')

    AUTH_URL = AUTH_SERVICE_URL + '/auth'
    AUTH_USER_URL = AUTH_SERVICE_URL + '/users'

    @staticmethod
    def login(payload):
        logger.warning(f"AUTH_URL: {AuthService.AUTH_URL}")
        response = requests.post(f"{AuthService.AUTH_URL}/login", json=payload)
        return response.json(), response.status_code

    @staticmethod
    def register(payload):
        response = requests.post(f"{AuthService.AUTH_URL}/register", json=payload)
        return response.json(), response.status_code
    
    @staticmethod
    def list_users(token):
        try:
            # Prepara los encabezados con el token recibido
            headers = {"Authorization": token}
            
            # Realiza la solicitud al servicio de autenticación
            response = requests.get(f"{AuthService.AUTH_USER_URL}/list", headers=headers)
            return response.json(), response.status_code
        except requests.exceptions.ConnectionError:
            return {"message": "Error de conexión con el servicio de autenticación."}, 503
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