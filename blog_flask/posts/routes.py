"""Posts controllers"""
import datetime

from flask import render_template, url_for, flash, redirect, request, abort, Blueprint
from flask_login import current_user, login_required
from sqlalchemy import or_

from blog_flask import db
from blog_flask.models import Post
from blog_flask.posts.forms import PostCreateForm


posts = Blueprint('posts', __name__, url_prefix='/posts')


@posts.route('/allpost', methods=['GET', 'POST'])
@login_required
def allpost():
    """Controller for list of all posts"""
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', None, type=str)
    if search:
        posts_list = Post.query.filter(
            or_(
                Post.title.contains(search),
                Post.content.contains(search)
            )
        ).order_by(
            Post.created_at.desc()
        ).paginate(
            page=page, per_page=5
        )
    else:
        posts_list = Post.query.order_by(Post.created_at.desc()).paginate(
            page=page, per_page=5
        )
    return render_template('allpost.html', posts=posts_list)


@posts.route('/publish', methods=['GET', 'POST'])
@login_required
def publish():
    """Controller to create new post"""
    form = PostCreateForm()
    if form.validate_on_submit():
        post_item = Post(
            title=form.title.data,
            content=form.content.data,
            created_at=datetime.datetime.utcnow(),
            author=current_user
        )
        db.session.add(post_item)
        db.session.commit()
        flash('Опубликовано', 'success')
        return redirect(url_for('posts.allpost'))
    return render_template('create_post.html', title='Новый пост', form=form)


@posts.route('/post')
def post():
    """Post detail page"""
    post_id = request.args.get('post_id', 0, type=int)
    post_item = Post.query.get_or_404(post_id)
    return render_template('post.html', post=post_item)


@posts.route('/update', methods=['GET', 'POST'])
@login_required
def update_post():
    """Update post"""
    post_id = request.args.get('post_id', 0, type=int)
    post_item = Post.query.get_or_404(post_id)
    if post_item.author != current_user:
        abort(403)
    form = PostCreateForm()
    if form.validate_on_submit():
        post_item.content = form.content.data
        post_item.title = form.title.data
        db.session.commit()
        flash('Обновлено', 'success')
        return redirect(url_for('posts.post', post_id=post_id))
    elif request.method == 'GET':
        form.title.data = post_item.title
        form.content.data = post_item.content
    return render_template('create_post.html', title='Обновление поста', form=form, legend='Обновление поста')


@posts.route('/delete', methods=['POST'])
@login_required
def delete_post():
    """Delete post"""
    post_id = request.args.get('post_id', 0, type=int)
    post_item = Post.query.filter(Post.id == post_id).one_or_none()
    if post_item is None or post_item.author != current_user:
        abort(403)
    db.session.delete(post_item)
    db.session.commit()
    flash('Пост удален', 'success')
    return redirect(url_for('posts.allpost'))
