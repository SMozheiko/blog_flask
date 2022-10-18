"""Main app module"""


from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

from config import Config

db = SQLAlchemy()
login_manager = LoginManager()


def create_app() -> Flask:
    """Creating main app"""
    app = Flask(__name__)
    db.init_app(app)

    from blog_flask.main.routes import main
    app.register_blueprint(main)

    app.config.from_object(Config)
    return app
