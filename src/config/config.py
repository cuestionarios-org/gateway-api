import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
    SERVICE_TIMEOUT = int(os.getenv('SERVICE_TIMEOUT', 5))
    RETRY_ATTEMPTS = int(os.getenv('RETRY_ATTEMPTS', 3))

    # Configuración para Rate Limiting
    LIMTER_DEFAULT_LIMIT = os.getenv('LIMITER_DEFAULT_LIMIT', '5 per minute')  # 5 peticiones por minuto
    LIMTER_STORAGE_URL = os.getenv('LIMITER_STORAGE_URL', 'redis://localhost:6379')  # Redis como almacenamiento


class DevelopmentConfig(Config):
    DEBUG = True
    LIMTER_STORAGE_URL = "memory://"  # Usar almacenamiento en memoria en desarrollo

class TestingConfig(Config):
    TESTING = True
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
    LIMTER_STORAGE_URL = "memory://" 

class ProductionConfig(Config):
    DEBUG = False

config_dict = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig
}
