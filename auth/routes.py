from flask import render_template, request, redirect, url_for
from . import bp

@bp.route('/register')
def register():
    return render_template('shared/register.html')
