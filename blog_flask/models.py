"""Application database models"""


import datetime

from flask_login import UserMixin

from blog_flask import db


class User(db.Model, UserMixin):
    """User class"""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    avatar = db.Column(db.String(100), nullable=False, default='default.png')
    password = db.Column(db.String(100), nullable=False)

    posts = db.relationship(
        'Post',
        backref='author',
        lazy=True,
        uselit=True
    )

    def __repr__(self):
        return '{}'.format(self.username)


class Post(db.Model):
    """Post model"""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow())
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(
        db.Integer, db.ForeignKey(
            'user.id',
            ondelete='CASCADE',
            onupdate='CASCADE'
        ), nullable=False
    )

    author = db.relationship(
        User,
        backref='posts',
        uselist=False
    )

    def __repr__(self):
        return '{}, {}, {}'.format(self.title, self.created_at.strftime('%Y-%m-%d %H:%M'), self.author)
