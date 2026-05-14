from flask import Blueprint, render_template, request, redirect, url_for, session, flash
import database
from functools import wraps

auth_bp = Blueprint('auth', __name__)

# Decorador para proteger rutas (copiado de tu app.py)
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Por favor, inicia sesión para acceder.', 'warning')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if database.verificar_usuario(username, password):
            db = database.obtener_conexion()
            user = db.execute('SELECT * FROM usuarios WHERE username = ?', (username,)).fetchone()
            db.close()
            
            session['user_id'] = user['id']
            session['username'] = user['username']
            session['role'] = user['rol']
            
            flash(f'¡Bienvenido {username}!', 'success')
            return redirect(url_for('admin.admin_panel'))
        else:
            flash('Usuario o contraseña incorrectos.', 'danger')
            
    return render_template('login.html')

@auth_bp.route('/logout')
def logout():
    session.clear()
    flash('Sesión cerrada correctamente.', 'info')
    return redirect(url_for('public.index'))