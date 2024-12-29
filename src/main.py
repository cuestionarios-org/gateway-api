from flask import Flask, jsonify
from config.config import config_dict
from routes.auth_routes import auth_bp
from utils.logger import get_logger
import os

logger = get_logger(__name__)

def create_app(config_name='development'):
    app = Flask(__name__)
    app.config.from_object(config_dict[config_name])
    
    app.register_blueprint(auth_bp, url_prefix='/auth')

    @app.errorhandler(500)
    def internal_error(error):
        logger.error(f"Server Error: {error}")
        return jsonify({"message": "Internal Server Error"}), 500

    return app

if __name__ == '__main__':
    env = os.getenv('FLASK_ENV', 'development')
    app = create_app(env)
    app.run(host='0.0.0.0', port=5000)
