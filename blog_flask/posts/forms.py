"""Posts forms"""


from flask_login import current_user
from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import StringField, TextAreaField, SubmitField, FileField
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
    picture = FileField(
        label='Добавить изображение',
        validators=[FileAllowed(['png', 'jpg'])]
    )
    submit = SubmitField('Опубликовать')


class CommentForm(FlaskForm):
    """Create comment form"""

    content = TextAreaField(
        label='Комментарий',
        validators=[
            DataRequired()
        ],
    )
    submit = SubmitField('Комментировать')
