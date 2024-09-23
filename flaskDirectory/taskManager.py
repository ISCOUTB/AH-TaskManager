from flask import Blueprint

bp = Blueprint('taskManager', __name__, url_prefix = '/taskManager')

@bp.route('/list')
def index():
    return "TO-DO LIST"

@bp.route('/create')
def create():
    return "CREATE TASK"