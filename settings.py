import os


class Config(object):
    """Base configuration."""

    SECRET_KEY = os.environ.get("SECRET", "super-secret-key")
    APP_DIR = os.path.abspath(os.path.dirname(__file__))
    PROJECT_ROOT = os.path.abspath(os.path.join(APP_DIR, os.pardir))
    DEBUG_TB_INTERCEPT_REDIRECTS = False
    CACHE_TYPE = "redis"
    CORS_ORIGIN_WHITELIST = [
        "http://0.0.0.0:3000",
        "http://localhost:3000",
    ]


class ProductionConfig(Config):
    """Production configuration."""

    ENV = "production"
    DEBUG = False


class DevConfig(Config):
    """Development configuration."""

    ENV = "dev"
    DEBUG = True
    DB_NAME = "dev.database"
    DB_PATH = os.path.join(Config.PROJECT_ROOT, DB_NAME)
    CACHE_TYPE = "redis"


class TestConfig(Config):
    """Test configuration."""

    TESTING = True
    DEBUG = True
