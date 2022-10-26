"""Users forms"""
from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FileField, BooleanField
from flask_wtf.file import FileAllowed
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from wtforms.widgets import core

from blog_flask.models import User


class RegistrationForm(FlaskForm):
    """Register user form"""

    username = StringField(
        label='Имя пользователя',
        validators=[
            DataRequired(),
            Length(min=1, max=20, message='Введите имя пользователя'),
        ]
    )
    email = StringField(
        label='Адрес электронной почты',
        validators=[DataRequired(), Email()],
        widget=core.EmailInput()
    )
    password = PasswordField(
        label='Пароль',
        validators=[DataRequired()]
    )
    confirm_password = PasswordField(
        label='Подтверждение',
        validators=[DataRequired(), EqualTo('password')]
    )
    submit = SubmitField(label='Зарегистрироваться')

    def validate_username(self, username):
        """Check for exist username"""
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError(
                'Пользователь с таким именем уже существует'
            )

    def validate_email(self, email):
        """Check for exist email"""
        user = User.query.filter_by(username=email.data).first()
        if user:
            raise ValidationError(
                'Пользователь с таким адресом уже существует'
            )


class LoginForm(FlaskForm):
    """Users login form"""

    username = StringField(
        label='Имя пользователя',
        validators=[DataRequired()]
    )
    password = PasswordField(
        label='Пароль',
        validators=[DataRequired()]
    )
    remember = BooleanField('Запомнить меня')

    submit = SubmitField(label='Войти')


class UserProfileUpdateForm(FlaskForm):
    """User profile update form"""

    username = StringField(
        label='Имя пользователя',
        validators=[DataRequired(), Length(min=1, max=20)]
    )
    email = StringField(
        label='Адрес электронной почты',
        validators=[DataRequired(), Email()],
        widget=core.EmailInput()
    )
    avatar = FileField(
        label='Аватарка',
        validators=[FileAllowed(['png', 'jpg'])]
    )
    submit = SubmitField('Сохранить')

    def validate_username(self, username):
        """Check for exist username"""
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError(
                    'Пользователь с таким именем уже существует'
                )

    def validate_email(self, email):
        """Check for exist email"""

        if email.data != current_user.email:
            user = User.query.filter_by(username=email.data).first()
            if user:
                raise ValidationError(
                    'Пользователь с таким адресом уже существует'
                )


class ChangePasswordRequestForm(FlaskForm):
    """Form to request users password change"""
    email = StringField(
        label='Введите email',
        validators=[DataRequired(), Email()],
        widget=core.EmailInput()
    )
    submit = SubmitField(label='Изменить пароль')

    def validate_email(self, email):
        """Check for exist email"""
        user = User.query.filter(User.email == email.data).one_or_none()
        if not user:
            raise ValidationError(
                'Пользователь с таким адресом не существует'
            )
        self.user = user


class ChangePasswordForm(FlaskForm):
    """Form to change users password"""
    password = PasswordField(
        label='Пароль',
        validators=[DataRequired()]
    )
    confirm_password = PasswordField(
        label='Подтверждение',
        validators=[DataRequired(), EqualTo('password')]
    )
    submit = SubmitField(label='Изменить пароль')
