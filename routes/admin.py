from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
import database
import os
from werkzeug.utils import secure_filename
from .auth import login_required 

admin_bp = Blueprint('admin', __name__)

# ==========================================
# 1. PANEL DE CONTROL PRINCIPAL (ADMIN)
# ==========================================
@admin_bp.route('/admin')
@login_required

def admin_panel():
    db = database.obtener_conexion()
    
    # 1. Consulta de productos con su stock total calculado
    query_productos = '''
        SELECT p.*, COALESCE(SUM(st.cantidad), 0) as stock_total
        FROM productos p
        LEFT JOIN stock_talles st ON p.id = st.producto_id
        GROUP BY p.id
        ORDER BY p.fecha_creacion DESC
    '''
    productos = db.execute(query_productos).fetchall()
    
    # 2. NUEVA CONSULTA: Historial de ventas con detalles del producto
    query_ventas = '''
        SELECT v.*, p.nombre as producto_nombre, p.codigo as producto_codigo
        FROM ventas v
        INNER JOIN productos p ON v.producto_id = p.id
        ORDER BY v.fecha_venta DESC
    '''
    ventas = db.execute(query_ventas).fetchall()
    
    db.close()
    
    # Enviamos tanto los productos como las ventas al HTML
    return render_template('admin.html', productos=productos, ventas=ventas)


# ==========================================
# 2. AGREGAR NUEVO PRODUCTO (CON TALLES)
# ==========================================
@admin_bp.route('/admin/nuevo', methods=['POST'])
@login_required
def nuevo_producto():
    codigo = request.form.get('codigo')
    nombre = request.form.get('nombre')
    descripcion = request.form.get('descripcion')
    precio = request.form.get('precio')
    
    precio_oferta = request.form.get('precio_oferta')
    precio_oferta = float(precio_oferta) if precio_oferta else None
    
    cantidad_oferta = request.form.get('cantidad_oferta')
    cantidad_oferta = int(cantidad_oferta) if cantidad_oferta else None

    # Procesamiento de la imagen
    nombre_imagen = 'default.png'
    if 'imagen_archivo' in request.files:
        file = request.files['imagen_archivo']
        if file and file.filename != '':
            filename = secure_filename(file.filename)
            ruta_guardado = os.path.join(current_app.root_path, 'static', 'img', 'productos', filename)
            file.save(ruta_guardado)
            nombre_imagen = filename

    db = database.obtener_conexion()
    try:
        # Insertamos en la tabla maestra de productos
        cursor = db.execute('''
            INSERT INTO productos (codigo, nombre, descripcion, precio, precio_oferta, cantidad_oferta, imagen)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (codigo, nombre, descripcion, precio, precio_oferta, cantidad_oferta, nombre_imagen))
        
        nuevo_id = cursor.lastrowid

        # Insertamos el inventario real correspondiente a cada talle en la tabla secundaria
        talles_disponibles = ['S', 'M', 'L', 'XL', 'XXL']
        for talle in talles_disponibles:
            cantidad = int(request.form.get(f'stock_{talle}', 0))
            db.execute('''
                INSERT INTO stock_talles (producto_id, talle, cantidad)
                VALUES (?, ?, ?)
            ''', (nuevo_id, talle, cantidad))

        db.commit()
        flash('Producto agregado con éxito', 'success')
    except Exception as e:
        db.rollback()
        flash(f'Error al crear el producto en el sistema: {e}', 'danger')
    finally:
        db.close()

    return redirect(url_for('admin.admin_panel'))


# ==========================================
# 3. EDITAR PRODUCTO ACTUAL (CON TALLES)
# ==========================================
@admin_bp.route('/admin/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar_producto(id):
    db = database.obtener_conexion()
    
    if request.method == 'POST':
        # Capturamos datos generales del formulario
        codigo = request.form.get('codigo')
        nombre = request.form.get('nombre')
        precio = float(request.form.get('precio', 0))
        descripcion = request.form.get('descripcion', '')
        
        # Manejo de campos de oferta numéricos opcionales
        p_oferta = request.form.get('precio_oferta')
        precio_oferta = float(p_oferta) if p_oferta else None
        c_oferta = request.form.get('cantidad_oferta')
        cantidad_oferta = int(c_oferta) if c_oferta else None
        
        # Recolectamos el mapeo matricial de los inputs de talle
        stock_talles_dict = {
            'S': request.form.get('stock_S', 0),
            'M': request.form.get('stock_M', 0),
            'L': request.form.get('stock_L', 0),
            'XL': request.form.get('stock_XL', 0),
            'XXL': request.form.get('stock_XXL', 0)
        }
        
        # Procesamiento opcional de cambio de imagen
        imagen_archivo = request.files.get('imagen_archivo')
        nombre_imagen = None
        if imagen_archivo and imagen_archivo.filename != '':
            nombre_imagen = secure_filename(imagen_archivo.filename)
            ruta_guardado = os.path.join(current_app.root_path, 'static/img/productos', nombre_imagen)
            imagen_archivo.save(ruta_guardado)
            
        # Ejecutamos la actualización unificada
        database.actualizar_producto(id, codigo, nombre, precio, precio_oferta, cantidad_oferta, descripcion, stock_talles_dict, nombre_imagen)
        
        flash('¡Producto y niveles de stock actualizados correctamente!', 'success')
        return redirect(url_for('admin.admin_panel'))
        
    # --- MÉTODO GET: Preparamos la visualización ---
    producto = db.execute('SELECT * FROM productos WHERE id = ?', (id,)).fetchone()
    
    # Traemos los stocks físicos reales de este producto específicos por talle
    registros_stock = db.execute('SELECT talle, cantidad FROM stock_talles WHERE producto_id = ?', (id,)).fetchall()
    db.close()
    
    # Lo transformamos en un diccionario amigable para Jinja: {'S': 12, 'M': 5...}
    stock_talles = {reg['talle']: reg['cantidad'] for reg in registros_stock}
    
    return render_template('editar.html', producto=producto, stock_talles=stock_talles)


# ==========================================
# 4. ELIMINAR PRODUCTO
# ==========================================
@admin_bp.route('/admin/eliminar/<int:id>', methods=['POST'])
@login_required
def eliminar_producto(id):
    db = database.obtener_conexion()
    # Gracias a la restricción ON DELETE CASCADE de la DB relacional, 
    # limpiar la fila en 'productos' remueve automáticamente sus registros en 'stock_talles'
    db.execute('DELETE FROM productos WHERE id = ?', (id,))
    db.commit()
    db.close()
    flash('Producto eliminado con éxito', 'success')
    return redirect(url_for('admin.admin_panel'))


# ==========================================
# 5. REGISTRAR VENTA (DESCUENTO AUTOMÁTICO)
# ==========================================
@admin_bp.route('/admin/registrar-venta', methods=['POST'])
@login_required
def registrar_venta():
    producto_id = request.form.get('producto_id')
    talle_vendido = request.form.get('talle') 
    cantidad_a_vender = int(request.form.get('cantidad', 1))

    db = database.obtener_conexion()
    producto = db.execute('SELECT precio, nombre FROM productos WHERE id = ?', (producto_id,)).fetchone()
    
    if not producto:
        db.close()
        flash('El producto solicitado no existe.', 'danger')
        return redirect(url_for('admin.admin_panel'))

    stock_actual = db.execute('''
        SELECT cantidad FROM stock_talles 
        WHERE producto_id = ? AND talle = ?
    ''', (producto_id, talle_vendido)).fetchone()

    if not stock_actual or stock_actual['cantidad'] < cantidad_a_vender:
        db.close()
        flash(f"❌ Quiebre de stock en talle {talle_vendido} para: {producto['nombre']}.", 'danger')
        return redirect(url_for('admin.admin_panel'))

    precio_u = producto['precio']
    total = precio_u * cantidad_a_vender

    try:
        # Transacción segura: disminuye inventario específico y añade historial diario
        db.execute('''
            UPDATE stock_talles 
            SET cantidad = cantidad - ? 
            WHERE producto_id = ? AND talle = ?
        ''', (cantidad_a_vender, producto_id, talle_vendido))

        db.execute('''
            INSERT INTO ventas (producto_id, talle, cantidad, precio_unitario, total_venta)
            VALUES (?, ?, ?, ?, ?)
        ''', (producto_id, talle_vendido, cantidad_a_vender, precio_u, total))

        db.commit()
        flash(f"✅ Venta procesada: {cantidad_a_vender}x {producto['nombre']} (Talle {talle_vendido})", 'success')
    except Exception as e:
        db.rollback()
        flash(f"Error interno en la base de datos al asentar la venta: {e}", 'danger')
    finally:
        db.close()

    return redirect(url_for('admin.admin_panel'))