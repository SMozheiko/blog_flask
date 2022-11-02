"""Posts controllers"""
import datetime
import json

from flask import render_template, url_for, flash, redirect, request, abort, Blueprint
from flask_login import current_user, login_required
from sqlalchemy import or_, and_

from blog_flask.users.utils import save_picture
from blog_flask.models import Post, Comment, Images, Like
from blog_flask.posts.forms import PostCreateForm, CommentForm


posts = Blueprint('posts', __name__, url_prefix='/posts')


@posts.route('/allpost', methods=['GET', 'POST'])
@login_required
def allpost():
    """Controller for list of all posts"""
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', None, type=str)
    favorites = request.args.get('favorites', 0, type=int)
    if favorites:
        posts_list = Post.query.join(
            Like, Like.post_id == Post.id
        ).filter(
            Like.user == current_user
        ).order_by(
            Post.created_at.desc()
        ).paginate(
            page=page, per_page=5
        )
    elif search:
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
        if form.picture.data:
            img = save_picture(form.picture.data, post=True)
            image_obj = Images(
                post=post_item,
                content=img,
                created_at=datetime.datetime.now()
            )
            image_obj.save()
        else:
            post_item.save()
        flash('Опубликовано', 'success')
        return redirect(url_for('posts.allpost'))
    return render_template('create_post.html', title='Новый пост', form=form)


@posts.route('/post')
def post():
    """Post detail page"""
    post_id = request.args.get('post_id', 0, type=int)
    post_item = Post.query.get_or_404(post_id)
    form = CommentForm()
    post_item.comments.sort(key=lambda x: x.created_at, reverse=True)
    likes = len(list(post_item.likes))
    liked = bool(Like.query.filter(
        and_(
            Like.post == post_item,
            Like.user == current_user
        )
    ).count())
    return render_template('post.html', post=post_item, form=form, likes=likes, liked=liked)


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
        if form.picture.data:
            img = save_picture(form.picture.data, post=True)
            image_obj = Images(
                post=post_item,
                content=img,
                created_at=datetime.datetime.now()
            )
            image_obj.save()
        else:
            post_item.save()
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
    post_item.delete()
    flash('Пост удален', 'success')
    return redirect(url_for('posts.allpost'))


@posts.route('/comment', methods=['POST'])
@login_required
def comment():
    """Add comment"""
    post_id = request.args.get('post_id', 0, type=int)
    post_item = Post.query.filter(Post.id == post_id).one_or_none()
    if post_item is None:
        abort(404)
    form = CommentForm()
    if form.validate_on_submit():
        comment_obj = Comment(
            content=form.content.data,
            created_at=datetime.datetime.now(),
            author=current_user,
            post=post_item
        )
        comment_obj.save()
        flash('Успешно!', 'success')
        return redirect(url_for('posts.post', post_id=post_item.id))


@posts.route('/edit_comment', methods=['GET', 'POST'])
@login_required
def edit_comment():
    """Edit comment"""
    comment_id = request.args.get('comment_id', 0, type=int)
    comment_item = Comment.query.filter(Comment.id == comment_id).one_or_none()
    if comment_item is None:
        abort(404)
    if comment_item.author != current_user:
        abort(403)
    edit_form = CommentForm()
    if edit_form.validate_on_submit():
        comment_item.content = edit_form.content.data
        comment_item.created_at = datetime.datetime.now()
        comment_item.save()
        flash('Обновлено!', 'success')
        return redirect(url_for('posts.post', post_id=comment_item.post.id))
    edit_form.content.data = comment_item.content
    form = CommentForm()
    comment_item.post.comments.sort(key=lambda x: x.created_at, reverse=True)
    return render_template('post.html', post=comment_item.post, form=form, edit_form=edit_form, comment_id=comment_id)


@posts.route('/delete_comment', methods=['POST'])
@login_required
def delete_comment():
    """Delete comment"""
    comment_id = request.args.get('comment_id', 0, type=int)
    comment_item = Comment.query.filter(Comment.id == comment_id).one_or_none()
    post_id = comment_item.post_id
    if comment_item is None:
        abort(404)
    if comment_item.author != current_user:
        abort(403)
    comment_item.delete()
    return redirect(url_for('posts.post', post_id=post_id))


@posts.route('/like', methods=['POST'])
@login_required
def like():
    """set/remove users like"""
    post_id = request.args.get('post_id', 0, type=int)
    post_item: Post = Post.query.filter(Post.id == post_id).one_or_none()
    count = len(list(post_item.likes))
    post_like = Like.query.filter(
        and_(
            Like.post == post_item,
            Like.user == current_user
        )
    ).one_or_none()
    if post_like:
        post_like.delete()
        return json.dumps({
            'status': 'ok',
            'likes': count - 1
        })

    post_like = Like(
        user=current_user,
        post=post_item
    )
    post_like.save()
    return json.dumps({
        'status': 'ok',
        'likes': count + 1
    })
