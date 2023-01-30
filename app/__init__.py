from flask import Flask
from .database import Database

db = Database()


def create_app() -> Flask:
    """Fábrica do aplicativo"""
    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY='dev',
        CONFIG_JSON_FILE='example.config.json',
    )

    db.init_app(app)

    # registering blueprints
    from .home import home_blueprint
    app.register_blueprint(home_blueprint)

    return app

