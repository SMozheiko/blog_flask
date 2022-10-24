"""Usersapp controllers"""

from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required

from blog_flask import db, bcrypt
from blog_flask.models import User, Post
from blog_flask.users.forms import RegistrationForm, LoginForm, UserProfileUpdateForm, ChangePasswordRequestForm, \
    ChangePasswordForm
from blog_flask.users.utils import save_picture


users = Blueprint('users', __name__)


@users.route('/register', methods=['GET', 'POST'])
def register():
    """Users registration controller"""
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(
            username=form.username.data,
            email=form.email.data,
            password=hashed_password
        )
        db.session.add(user)
        db.session.commit()
        flash("Регистрация прошла успешно", "success")
        return redirect(url_for('users.login'))
    return render_template('register.html', title='Register', form=form)


@users.route('/login', methods=['GET', 'POST'])
def login():
    """User login controller"""
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).one_or_none()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            return  redirect(url_for('main.home'))
        else:
            flash('Не верный логин и/или пароль', 'Внимание')
    return render_template('login.html', title='Авторизация', form=form)
