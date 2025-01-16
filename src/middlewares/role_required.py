from functools import wraps
from flask import request, jsonify
import jwt
from config.config import Config
import inspect

def role_required(required_roles):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            token = request.headers.get('Authorization')
            if not token:
                return jsonify({"message": "Token is missing!"}), 401
            
            try:
                token = token.split("Bearer ")[1]
                token_data = jwt.decode(token, Config.JWT_SECRET_KEY, algorithms=["HS256"])
                if token_data.get("role") not in required_roles:
                    return jsonify({"message": "No tienes permisos para este recurso."}), 403
            except jwt.ExpiredSignatureError:
                return jsonify({"message": "El token ha expirado."}), 401
            except jwt.InvalidTokenError:
                return jsonify({"message": "Token inválido."}), 401
            
            # Verificar si la función decorada acepta `token_data`
            sig = inspect.signature(f)
            if "token_data" in sig.parameters:
                return f(*args, token_data=token_data, **kwargs)
            else:
                return f(*args, **kwargs)
        return wrapper
    return decorator
