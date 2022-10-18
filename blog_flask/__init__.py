"""Main app module"""


from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

from blog_flask.config import Config

db = SQLAlchemy()
login_manager = LoginManager()


def create_app() -> Flask:
    """Creating main app"""
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)

    login_manager.init_app(app)

    from blog_flask.main.routes import main
    app.register_blueprint(main)

    return app
