from flask import Blueprint

api_bp = Blueprint('auth', __name__, url_prefix='/api')

from . import views
