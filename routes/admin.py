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

@admin_bp.route('/admin/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar_producto(id):
    db = database.obtener_conexion()
    if request.method == 'POST':
        # Aquí irá tu lógica para actualizar (UPDATE productos SET...)
        flash('Producto actualizado', 'success')
        return redirect(url_for('admin.admin_panel'))
    
    producto = db.execute('SELECT * FROM productos WHERE id = ?', (id,)).fetchone()
    db.close()
    return render_template('editar.html', producto=producto)

@admin_bp.route('/admin/eliminar/<int:id>', methods=['POST'])
@login_required
def eliminar_producto(id):
    db = database.obtener_conexion()
    db.execute('DELETE FROM productos WHERE id = ?', (id,))
    db.commit()
    db.close()
    flash('Producto eliminado', 'success')
    return redirect(url_for('admin.admin_panel'))