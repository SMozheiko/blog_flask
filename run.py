from blog_flask import create_app, db
from blog_flask.models import User, Post

app = create_app()
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
