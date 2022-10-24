"""Context processors"""

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class SearchForm(FlaskForm):
    """Search form"""
    search = StringField(
        label='Поиск',
        validators=[DataRequired()]
    )
    find = SubmitField(
        label='Найти'
    )
