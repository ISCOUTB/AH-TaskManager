from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_mysqldb import MySQL
import MySQLdb

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Para los mensajes flash

# Configuración de la base de datos MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'lunamiranda01'
app.config['MYSQL_DB'] = 'taskmanagerdb'
mysql = MySQL(app)

# Ruta principal
@app.route('/')
def home():
    return render_template('home.html')

# Ruta para el Sign Up
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        email = request.form.get('email')
        password = request.form.get('password')  
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM usuarios WHERE email = %s", (email,))
        account = cursor.fetchone()
        
        if account:
            flash('Email address already in use', 'danger')
            return redirect(url_for('signup'))
        
        cursor.execute("INSERT INTO usuarios(nombre, email, password) VALUES(%s, %s, %s)", (nombre, email, password))
        mysql.connection.commit()
        flash('Account created successfully', 'success')
        return redirect(url_for('login'))
    
    return render_template('signup.html')

# Ruta para el Log In
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)  # Usar DictCursor para obtener diccionarios
        cursor.execute("SELECT * FROM usuarios WHERE email = %s AND password = %s", (email, password))
        user = cursor.fetchone()
        if user:
            session['id'] = user['id']
            session['nombre'] = user['nombre']  # Almacena el nombre en la sesión

            flash('Logged in successfully', 'success')
            return redirect(url_for('task_list'))  # Redirige al home si el login es exitoso
        else:
            flash('Login failed. Check your credentials', 'danger')
    return render_template('login.html')

# Ruta para la lista de tareas
@app.route('/task_list')
def task_list():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    user_id = session.get('id')
    cursor.execute("SELECT * FROM tasks WHERE user_id = %s", (user_id,))
    tasks = cursor.fetchall()
    
    if 'nombre' in session:  # Verifica si el usuario está logueado
        nombre_usuario = session['nombre']  # Obtiene el nombre del usuario desde la sesión
    else:
        nombre_usuario = None  # Si no está logueado, no pasa nombre
    
    return render_template('task_list.html', tasks=tasks, nombre_usuario=nombre_usuario)

# Ruta para agregar tareas
@app.route('/add_task', methods=['GET', 'POST'])
def add_task():
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        status = request.form.get('status')
        user_id = session.get('id')
        
        if not name or not description or not status:
            flash('Please fill out all fields', 'danger')
            return redirect(url_for('add_task'))
        
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("INSERT INTO tasks(name, description, status, user_id) VALUES(%s, %s, %s, %s)", (name, description, status, user_id))
        mysql.connection.commit()
        flash('Task added successfully', 'success')
        return redirect(url_for('task_list'))
    
    return render_template('add_task.html')

# Ruta para editar tareas
@app.route('/edit_task/<int:task_id>', methods=['GET', 'POST'])
def edit_task(task_id):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM tasks WHERE id = %s", (task_id,))
    task = cursor.fetchone()
    
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        status = 'completed' if request.form.get('status') else 'pending'
        
        if not name or not description or not status:
            flash('Please fill out all fields', 'danger')
            return redirect(url_for('edit_task', task_id=task_id))
        
        cursor.execute("UPDATE tasks SET name = %s, description = %s, status = %s WHERE id = %s", (name, description, status, task_id))
        mysql.connection.commit()
        flash('Task updated successfully', 'success')
        return redirect(url_for('task_list'))
    
    return render_template('edit_task.html', task=task)

# Ruta para eliminar tareas
@app.route('/delete_task/<int:task_id>', methods=['POST'])
def delete_task(task_id):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("DELETE FROM tasks WHERE id = %s", (task_id,))
    mysql.connection.commit()
    flash('Task deleted successfully', 'success')
    return redirect(url_for('task_list'))

# Ruta para cerrar sesión
@app.route('/logout', methods=['POST'])
def logout():
    session.clear()
    flash('You have been logged out.', 'success')
    return redirect(url_for('login'))

# Ejecuta la aplicación
if __name__ == '__main__':
    app.run(debug=True)

