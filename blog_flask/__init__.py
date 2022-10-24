"""Main app module"""


from flask import Flask
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

from blog_flask.config import Config

db = SQLAlchemy()

login_manager = LoginManager()
bcrypt = Bcrypt()


def create_app() -> Flask:
    """Creating main app"""

    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)

    login_manager.init_app(app)
    from blog_flask.users.routes import login
    login_manager.unauthorized_callback = login
    bcrypt.init_app(app)

    from blog_flask.main.routes import main
    from blog_flask.users.routes import users
    from blog_flask.posts.routes import posts
    app.register_blueprint(main)
    app.register_blueprint(users)
    app.register_blueprint(posts)

    return app
