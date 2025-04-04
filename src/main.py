from flask import Flask, jsonify
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from config.config import config_dict
from routes.register_routes import register_routes
from utils.error_handlers import register_error_handlers
from utils.logger import get_logger
import os

logger = get_logger(__name__)

def create_app(config_name='development'):
    app = Flask(__name__)
    app.config.from_object(config_dict[config_name])
    

    # Inicializamos el limiter
    limiter = Limiter(
        get_remote_address,  # Utiliza la IP del cliente para limitar las peticiones
        app=app,  # Asociamos el limiter con nuestra app
        default_limits=[app.config['LIMTER_DEFAULT_LIMIT']],  # Límite por defecto global
        storage_uri=app.config['LIMTER_STORAGE_URL']  # URL de conexión al almacenamiento
    )
    
    @app.route('/')
    def index():
        return jsonify({
            'message': 'Welcome to the Flask application!',
            'status': 'success',
            'documentation': '/docs'  # Ejemplo de ruta de documentación
        }), 200
    register_routes(app)

   # Registramos manejadores de errores
    register_error_handlers(app)
    
    return app

if __name__ == '__main__':
    env = os.getenv('FLASK_ENV', 'development')
    app = create_app(env)
    app.run(host='0.0.0.0', port=5000)
