"""Posts forms"""


from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, ValidationError, Length

from blog_flask.models import User, Post


class PostCreateForm(FlaskForm):
    """Creation form"""

    title = StringField(
        label='Заголовок',
        validators=[
            DataRequired(),
            Length(min=1, max=100)
        ]
    )
    content = TextAreaField(
        label='Содержание',
        validators=[DataRequired()]
    )
    submit = SubmitField('Опубликовать')
