from flask import Blueprint

bp = Blueprint('recipient', __name__, template_folder='templates')

from . import routes
