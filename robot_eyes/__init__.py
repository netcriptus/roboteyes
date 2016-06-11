from uuid import uuid4
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

__version__ = '0.1.0'

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)

    app.config.from_object('robot_eyes.settings.base')
    db.init_app(app)

    # Blueprints
    from robot_eyes.controllers import controllers

    # Register blueprints
    app.register_blueprint(controllers)

    app.secret_key = uuid4().hex

    return app
