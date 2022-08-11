from flask import Flask

from .home import home_blueprint


def create_app(config=None) -> Flask:
    """Fábrica do aplicativo"""
    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY='dev'
    )

    # registering blueprints
    app.register_blueprint(home_blueprint)

    return app

