"""
Configuración de la aplicación Flask
Define variables de entorno y configuraciones por ambiente
"""

import os
from datetime import timedelta


class Config:
    """Configuración base"""
    
    # Flask
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'automatas-lexer-2026-dev'
    DEBUG = False
    TESTING = False
    
    # Upload
    MAX_CONTENT_LENGTH = 1 * 1024 * 1024  # 1MB max
    
    # Session
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'


class DevelopmentConfig(Config):
    """Configuración para desarrollo"""
    DEBUG = True
    SESSION_COOKIE_SECURE = False


class ProductionConfig(Config):
    """Configuración para producción"""
    DEBUG = False
    TESTING = False
    SESSION_COOKIE_SECURE = True


class TestingConfig(Config):
    """Configuración para testing"""
    TESTING = True
    DEBUG = True


# Seleccionar configuración según ambiente
config_by_name = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig,
}


def get_config(env=None):
    """
    Obtiene la configuración apropiada
    
    Args:
        env: Nombre del ambiente ('development', 'production', 'testing')
    
    Returns:
        Clase de configuración
    """
    if env is None:
        env = os.environ.get('FLASK_ENV', 'development')
    
    return config_by_name.get(env, DevelopmentConfig)
