"""Database update sxript"""
from blog_flask import db, create_app


app = create_app()
with app.app_context():
    db.create_all()
