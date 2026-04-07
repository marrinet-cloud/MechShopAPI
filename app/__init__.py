from flask import Flask
from .extensions import db, ma, limiter, cache
from flask_swagger_ui import get_swaggerui_blueprint


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

    SWAGGER_URL = "/api/docs"
    API_URL = "/static/swagger.yaml"

    swaggerui_blueprint = get_swaggerui_blueprint(
        SWAGGER_URL,
        API_URL,
        config={"app_name": "Mechanic Shop API"}
    )
    app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

    @app.get("/")
    def health():
        return {"status": "ok"}

    return app