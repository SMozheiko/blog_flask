"""Usersapp controllers"""

from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required

from blog_flask import db, bcrypt
from blog_flask.models import User, Post
from blog_flask.users.forms import RegistrationForm, LoginForm, UserProfileUpdateForm, ChangePasswordRequestForm, \
    ChangePasswordForm
from blog_flask.users.utils import save_picture, send_reset_email


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
        return redirect(url_for('posts.allpost'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).one_or_none()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)
            return redirect(url_for('posts.allpost'))
        else:
            flash('Не верный логин и/или пароль', 'Внимание')
    return render_template('login.html', title='Авторизация', form=form)


@users.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UserProfileUpdateForm()
    if form.validate_on_submit():
        if form.avatar.data:
            avatar_file = save_picture(form.avatar.data)
            current_user.avatar = avatar_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Обновлено!', 'success')
        return redirect(url_for('users.account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        page = request.args.get('page', 1, type=int)
        user = User.query.filter_by(
            username=form.username.data
        ).first_or_404()
        posts = Post.query.filter_by(
            author=user
        ).order_by(
            Post.created_at.desc()
        ).paginate(page=page, per_page=5)
        image_file = url_for('static', filename='profile_pictures/' + current_user.avatar)
        return render_template(
            'account.html',
            title='Account',
            image_file=image_file,
            form=form,
            posts=posts,
            user=user
        )


@users.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.home'))


@users.route('/user_posts')
def user_posts():
    username = request.args.get('username', type=str)
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first()
    posts = Post.query.filter_by(author=user).order_by(
        Post.created_at.desc()
    ).paginate(page=page, per_page=5)
    return render_template('user_posts.html', posts=posts, user=user)


@users.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    """Password remainder"""
    if current_user.is_authenticated:
        return redirect(url_for('posts.allpost'))
    form = ChangePasswordRequestForm()
    if form.validate_on_submit():
        token = form.user.get_reset_token()
        send_reset_email(token, form.user.email)
        flash("На указанные адрес было направлено письмо со ссылкой на изменение пароля", 'info')
        return redirect(url_for('users.login'))
    return render_template('forgot_password.html', title='Восстановление пароля', form=form)


@users.route('/change_password', methods=['GET', 'POST'])
def change_password():
    """Change users password"""
    form = ChangePasswordForm()
    if request.method == 'GET':
        token = request.args.get('token', None, type=str)
        user = User.verify_reset_token(token)
        if not user:
            flash('Не правильный/истекший токен', 'error')
            return redirect(url_for('users.forgot_password'))
        return render_template('change_password.html', title='Смена пароля', form=form, user=user)
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user_id = request.args.get('user_id', type=int)
        user = User.query.get(user_id)
        user.password = hashed_password
        db.session.add(user)
        db.session.commit()
        flash('Успешно!',  'success')
        return redirect(url_for('users.login'))
