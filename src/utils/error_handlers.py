from flask import jsonify
from flask_limiter.errors import RateLimitExceeded
import requests
from utils.logger import get_logger

logger = get_logger(__name__)

def register_error_handlers(app):
    """
    Registra los manejadores de errores en la aplicación Flask.
    """
    
    @app.errorhandler(RateLimitExceeded)
    def handle_rate_limit_exceeded(e):
        return jsonify({
            "status": "error",
            "message": "Has excedido el límite de peticiones permitido. Por favor, inténtalo más tarde."
        }), 429

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
