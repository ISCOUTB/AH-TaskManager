from flask import render_template, request, redirect, url_for, mysql
from . import tasks_blueprint

@tasks_blueprint.route('/')
def task_list():
    return "Lista de tareas"

# Ruta para ver las tareas
@tasks_blueprint.route('/')
def task_list():
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM tasks')  # Consulta las tareas de la base de datos
    tasks = cursor.fetchall()  # Obtiene todas las tareas
    cursor.close()
    return render_template('task_list.html', tasks=tasks)

# Ruta para agregar una nueva tarea
@tasks_blueprint.route('/add', methods=['POST'])
def add_task():
    if request.method == 'POST':
        task_name = request.form['task_name']
        cursor = mysql.connection.cursor()
        cursor.execute('INSERT INTO tasks (name) VALUES (%s)', (task_name,))
        mysql.connection.commit()
        cursor.close()
        return redirect(url_for('tasks.task_list'))