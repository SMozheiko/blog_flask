"""Admin module"""

from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from blog_flask.models import User, Post, Like, Comment, Images
from blog_flask import db, create_app

app = create_app()

admin = Admin(app)
for view in User, Post, Like, Comment, Images:
    admin.add_view(ModelView(view, db.session))
