"""Error handlers"""


from flask import Blueprint, render_template

errors = Blueprint('errors', __name__)


@errors.app_errorhandler(404)
def error_404(error):
    """Error 404 handler"""
    return render_template('errors/404.html', title='Not found'), 404


@errors.app_errorhandler(403)
def error_403(error):
    """Error 403 handler"""
    return render_template('errors/403.html', title='Unauthorized'), 403


@errors.app_errorhandler(500)
def error_500(error):
    """Error 500 handler"""
    return render_template('errors/500.html', title='Internal server error'), 500
