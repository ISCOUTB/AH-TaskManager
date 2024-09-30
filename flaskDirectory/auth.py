from flask import Blueprint, render_template

from . import models

bp = Blueprint('auth', __name__, url_prefix = '/auth')

@bp.route('/signup')
def signup():
    return render_template('auth/signup.html')

@bp.route('/login')
def login():
    return render_template('auth/login.html')