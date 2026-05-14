from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
import database
import os
from werkzeug.utils import secure_filename
from .auth import login_required # Importamos el decorador

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/admin')
@login_required
def admin_panel():
    db = database.obtener_conexion()
    productos = db.execute('SELECT * FROM productos ORDER BY fecha_creacion DESC').fetchall()
    db.close()
    return render_template('admin.html', productos=productos)

@admin_bp.route('/admin/nuevo', methods=['POST'])
@login_required
def nuevo_producto():
    # ... (Aquí va tu lógica actual de request.form y guardar imagen)
    flash('Producto agregado con éxito', 'success')
    return redirect(url_for('admin.admin_panel'))

# Agregá aquí también las rutas de /editar/<id> y /eliminar/<id>