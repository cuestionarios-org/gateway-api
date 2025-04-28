from flask import Flask, jsonify, redirect  
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from config.config import config_dict
from routes.register_routes import register_routes
from utils.error_handlers import register_error_handlers
from utils.logger import get_logger
import os
from flask_cors import CORS

logger = get_logger(__name__)

def create_app(config_name='development'):
    app = Flask(__name__)
    CORS(app)
    app.config.from_object(config_dict[config_name])
    
    # Habilita CORS para todos los orígenes y rutas

    # Inicializamos el limiter
    limiter = Limiter(
        get_remote_address,  # Utiliza la IP del cliente para limitar las peticiones
        app=app,  # Asociamos el limiter con nuestra app
        default_limits=[app.config['LIMTER_DEFAULT_LIMIT']],  # Límite por defecto global
        storage_uri=app.config['LIMTER_STORAGE_URL']  # URL de conexión al almacenamiento
    )
    
    @app.route('/')
    def root_redirect():
        return redirect('/api')  # Redirige a la ruta /api
    
    @app.route('/api')
    def index():
        return jsonify({
            'message': 'Bienvenido al Api de Cuestionarios',
            'status': 'success',
            'documentation': '/docs',  # Ejemplo de ruta de documentación
            'auth': '/auth/register',
            'login': '/auth/login',
            'quizzes': '/quizzes',
            'questions': '/questions',
            'answers': '/answers',

        }), 200
    register_routes(app)

   # Registramos manejadores de errores
    register_error_handlers(app)
    
    return app

if __name__ == '__main__':
    env = os.getenv('FLASK_ENV', 'development')
    app = create_app(env)
    app.run(host='0.0.0.0', port=5000)
