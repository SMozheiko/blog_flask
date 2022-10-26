"""Users utils module"""

import os

from secrets import token_hex

from flask import url_for, current_app
from flask_mail import Message
from PIL import Image

from blog_flask import mail


def save_picture(form_picture) -> str:
    """Saves uploaded user avatar"""
    random_hex = token_hex(8)
    _, file_extension = os.path.splitext(form_picture.filename)
    picture_filename = random_hex + file_extension
    picture_path = os.path.join(current_app.root_path, 'static/profile_pictures', picture_filename)
    output_size = (150, 150)
    img = Image.open(form_picture)
    img.thumbnail(output_size)
    img.save(picture_path)

    return picture_filename


def send_reset_email(token: str, email: str):
    """Send email for reset password"""
    msg_body = 'Перейдите по ссылке {} чтобы сбросить пароль.' \
               'Если Вы не делали запрос на смену пароля - просто' \
               'проигнорируйте это письмо'.format(url_for('users.change_password', token=token, _external=True))
    msg = Message(subject='password reset', recipients=[email], body=msg_body)
    mail.send(msg)
