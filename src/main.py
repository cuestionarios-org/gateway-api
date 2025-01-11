from flask import Flask, jsonify
from flask_limiter import Limiter
from flask_limiter.errors import RateLimitExceeded
from flask_limiter.util import get_remote_address
from config.config import config_dict
from routes.register_routes import register_routes
from utils.logger import get_logger
import os
import requests
import redis

logger = get_logger(__name__)

def create_app(config_name='development'):
    app = Flask(__name__)
    app.config.from_object(config_dict[config_name])
    
    print("XXXXXXXXXXXXXX", app.config['LIMTER_STORAGE_URL'])  # Accede desde app.config

    # Inicializamos el limiter
    limiter = Limiter(
        get_remote_address,  # Utiliza la IP del cliente para limitar las peticiones
        app=app,  # Asociamos el limiter con nuestra app
        default_limits=[app.config['LIMTER_DEFAULT_LIMIT']],  # Límite por defecto global
        storage_uri=app.config['LIMTER_STORAGE_URL']  # URL de conexión al almacenamiento
    )
    
#  Manejador para el error de demasiadas solicitudes
    @app.errorhandler(RateLimitExceeded)
    def handle_rate_limit_exceeded(e):
        return jsonify({
            "status": "error",
            "message": "Has excedido el límite de peticiones permitido. Por favor, inténtalo más tarde."
        }), 429
    register_routes(app)

    @app.errorhandler(404)
    def not_found_error(error):
        logger.warning(f"404 Error: {error}")
        return jsonify({
            "status": "error",
            "message": "El recurso solicitado no existe. Verifica la URL e intenta nuevamente."
        }), 404

    @app.errorhandler(500)
    def internal_error(error):
        logger.error(f"Server Error: {error}")
        return jsonify({"message": "Internal Server Error"}), 500
    
    @app.errorhandler(requests.exceptions.ConnectionError)
    def handle_connection_error(error):
        logger.error(f"Connection Error: {error}")
        return jsonify({
            "status": "error",
            "message": "El servicio no está disponible en este momento. Por favor, intente más tarde."
        }), 503
    
    @app.errorhandler(Exception)
    def global_error_handler(error):
        logger.error(f"Unexpected error: {error}")
        return jsonify({
            "status": "error",
            "message": "Ocurrió un error inesperado. Intenta más tarde."
        }), 500
    
    return app

if __name__ == '__main__':
    env = os.getenv('FLASK_ENV', 'development')
    app = create_app(env)
    app.run(host='0.0.0.0', port=5000)
