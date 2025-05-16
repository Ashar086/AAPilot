from flask import render_template
from . import bp

@bp.route('/')
def landing_page():
    return render_template('core/landing-page.html')
