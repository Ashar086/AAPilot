from flask import Blueprint

bp = Blueprint('results', __name__, template_folder='templates')

from . import routes
