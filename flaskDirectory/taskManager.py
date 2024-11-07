from flask import Blueprint, render_template, request, redirect, url_for, g
from flaskDirectory.auth import login_required
from .models import Todo, User
from flaskDirectory import db
bp = Blueprint('taskManager', __name__, url_prefix = '/taskManager')
taskmanager = 'taskManager.index'

@bp.route('/list')
@login_required
def index():
    todos = Todo.query.all()
    return render_template('todo/index.html', todos = todos)

@bp.route('/create', methods = ('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']

        todo = Todo(g.user.id, title, description)
        db.session.add(todo)
        db.session.commit()
        return redirect(url_for(taskmanager))
    return render_template('todo/create.html')

def get_todo(id):
    todo = Todo.query.get_or_404(id)
    return todo

@bp.route('/update/<int:id>', methods = ('GET', 'POST'))
@login_required
def update(id):
    todo = get_todo(id)

    if request.method == 'POST':
        todo.title = request.form['title']
        todo.description = request.form['description']
        todo.status = True if request.form.get('status') == 'on' else False

        db.session.commit()
        return redirect(url_for(taskmanager))
    return render_template('todo/update.html', todo = todo)

@bp.route('/delete/<int:id>', methods = ('GET', 'POST'))
@login_required
def delete(id):
    todo = get_todo(id)
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for(taskmanager))