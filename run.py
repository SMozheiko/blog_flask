import datetime

from blog_flask.admin import app
from blog_flask.models import User, Post
from blog_flask.context_processsors import SearchForm


@app.context_processor
def search():
    form = SearchForm()
    return dict(search=form)


@app.context_processor
def year():
    today_year = datetime.datetime.now().year
    return dict(year=today_year)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
