"""Application database models"""


import datetime

import jwt
from flask import current_app
from flask_login import UserMixin

from blog_flask import db, login_manager


@login_manager.user_loader
def load_user(user_id):
    """User loader"""
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    """User class"""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    avatar = db.Column(db.String(100), nullable=False, default='default.png')
    password = db.Column(db.String(100), nullable=False)

    posts = db.relationship(
        'Post',
        back_populates='author',
        lazy=True,
        uselist=True
    )

    def get_reset_token(self, exp=1800) -> str:
        """Generate JWT token"""
        exp_time = datetime.datetime.now() + datetime.timedelta(seconds=exp)
        return jwt.encode(
            {'user_id': self.id, 'exp': exp_time.timestamp()},
            current_app.config['SECRET_KEY']
        )

    @classmethod
    def verify_reset_token(cls, token: str):
        """Check JWT token"""
        data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
        try:
            user_id = data.get('user_id')
        except Exception:
            return
        else:
            exp = data.get('exp')
            if exp and datetime.datetime.now().timestamp() <= exp:
                return cls.query.filter(User.id == user_id).one_or_none()
            return

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
        back_populates='posts',
        uselist=False
    )

    def __repr__(self):
        return '{}, {}, {}'.format(self.title, self.created_at.strftime('%Y-%m-%d %H:%M'), self.author)
