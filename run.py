from blog_flask import create_app, db
from blog_flask.models import User, Post
from blog_flask.context_processsors import SearchForm

app = create_app()
with app.app_context():
    db.create_all()


@app.context_processor
def search():
    form = SearchForm()
    return dict(search=form)


if __name__ == '__main__':
    app.run(debug=True)
