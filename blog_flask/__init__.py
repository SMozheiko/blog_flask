"""Main app module"""


from flask import Flask
from flask_bcrypt import Bcrypt
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

from blog_flask.config import Config

db = SQLAlchemy()

login_manager = LoginManager()
bcrypt = Bcrypt()
mail = Mail()


def create_app() -> Flask:
    """Creating main app"""

    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    mail.init_app(app)

    login_manager.init_app(app)
    from blog_flask.users.routes import login
    login_manager.unauthorized_callback = login
    bcrypt.init_app(app)

    from blog_flask.main.routes import main
    from blog_flask.users.routes import users
    from blog_flask.posts.routes import posts
    from blog_flask.errors.handlers import errors
    app.register_blueprint(main)
    app.register_blueprint(users)
    app.register_blueprint(posts)
    app.register_blueprint(errors)

    return app
