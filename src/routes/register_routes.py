from flask import Flask
from routes.auth_routes import auth_bp
from routes.questions_routes import qa_bp

def register_routes(app: Flask):
    """
    Registra todos los blueprints en la aplicación Flask.

    Args:
        app (Flask): La instancia de la aplicación Flask.
    """
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(qa_bp, url_prefix='/questions')

