class DevelopmentConfig:
    DEBUG = True
    SECRET_KEY = "super-secret-key-change-this"
    SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://root:sqlMari$22@localhost/mechanic_shop_db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    CACHE_TYPE = "SimpleCache"
    CACHE_DEFAULT_TIMEOUT = 60

    RATELIMIT_STORAGE_URI = "memory://"


class TestingConfig:
    TESTING = True
    DEBUG = True
    SECRET_KEY = "super-secret-key-change-this"
    SQLALCHEMY_DATABASE_URI = "sqlite:///testing.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    CACHE_TYPE = "SimpleCache"
    CACHE_DEFAULT_TIMEOUT = 60

    RATELIMIT_STORAGE_URI = "memory://"


class ProductionConfig:
    DEBUG = False
    SECRET_KEY = "super-secret-key-change-this"
    SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://root:sqlMari$22@localhost/mechanic_shop_db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    CACHE_TYPE = "SimpleCache"
    CACHE_DEFAULT_TIMEOUT = 60

    RATELIMIT_STORAGE_URI = "memory://"