from flask import Blueprint

bp = Blueprint('assessment', __name__, template_folder='templates')

from . import routes
