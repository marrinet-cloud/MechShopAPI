from flask import Flask
from .extensions import db, ma, limiter, cache


def create_app(config_name: str = "DevelopmentConfig"):
    app = Flask(__name__)
    app.config.from_object(f"config.{config_name}")

    db.init_app(app)
    ma.init_app(app)
    limiter.init_app(app)
    cache.init_app(app)

    from .blueprints.customers import customers_bp
    app.register_blueprint(customers_bp, url_prefix="/customers")

    from .blueprints.mechanics import mechanics_bp
    app.register_blueprint(mechanics_bp, url_prefix="/mechanics")

    from .blueprints.service_tickets import service_tickets_bp
    app.register_blueprint(service_tickets_bp, url_prefix="/service-tickets")

    from .blueprints.inventory import inventory_bp
    app.register_blueprint(inventory_bp, url_prefix="/inventory")

    @app.get("/")
    def health():
        return {"status": "ok"}

    print(app.url_map)

    return app