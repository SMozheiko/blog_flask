"""Routees for mainapp"""

from flask import render_template, Blueprint
from blog_flask.models import User


main = Blueprint('main', __name__)


@main.route('/')
@main.route('/home')
def home():
    """Homepage controller"""
    return render_template('home.html')
