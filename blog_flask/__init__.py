"""Main app module"""


from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


db = SQLAlchemy()
login_manager = LoginManager()


def create_app() -> Flask:
    """Creating main app"""
    app = Flask(__name__)
    db.init_app(app)
    return app
