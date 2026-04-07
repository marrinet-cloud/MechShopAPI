import os


class DevelopmentConfig:
    DEBUG = True
    SECRET_KEY = os.environ.get("SECRET_KEY") or "super-secret-key-change-this"
    SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://root:sqlMari$22@localhost/mechanic_shop_db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    CACHE_TYPE = "SimpleCache"
    CACHE_DEFAULT_TIMEOUT = 60

    RATELIMIT_STORAGE_URI = "memory://"


class TestingConfig:
    TESTING = True
    DEBUG = True
    SECRET_KEY = os.environ.get("SECRET_KEY") or "super-secret-key-change-this"
    SQLALCHEMY_DATABASE_URI = "sqlite:///testing.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    CACHE_TYPE = "SimpleCache"
    CACHE_DEFAULT_TIMEOUT = 60

    RATELIMIT_STORAGE_URI = "memory://"


class ProductionConfig:
    DEBUG = False
    SECRET_KEY = os.environ.get("SECRET_KEY") or "super secret secrets"
    SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    CACHE_TYPE = "SimpleCache"
    CACHE_DEFAULT_TIMEOUT = 60

    RATELIMIT_STORAGE_URI = "memory://"