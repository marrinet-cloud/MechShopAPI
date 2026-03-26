class DevelopmentConfig:
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://root:sqlMari$22@localhost/mechanic_shop_db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class TestingConfig:
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://root:sqlMari$22@localhost/mechanic_shop_db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig:
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://root:sqlMari$22@localhost/mechanic_shop_db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False