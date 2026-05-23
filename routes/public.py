from flask import Blueprint, render_template, request, redirect, url_for, flash
import database

public_bp = Blueprint('public', __name__)

@public_bp.route('/')
def index():
    db = database.obtener_conexion()
    
    # 1. CONSULTA COMPLETA PARA EL CATÁLOGO:
    # Agrupamos por producto y sumamos las cantidades de todos sus talles reales
    query_productos = '''
        SELECT p.*, COALESCE(SUM(st.cantidad), 0) as stock
        FROM productos p
        LEFT JOIN stock_talles st ON p.id = st.producto_id
        GROUP BY p.id
        ORDER BY p.fecha_creacion DESC
    '''
    productos_db = db.execute(query_productos).fetchall()
    
    # 2. SELECCIÓN DE DESTACADOS PARA EL SWIPER:
    # Filtramos de forma inteligente para el carrusel superior (por ejemplo, los primeros 4)
    destacados_db = productos_db[:4]
    
    db.close()
    
    # Enviamos AMBAS variables que tu index.html necesita para renderizar
    return render_template('index.html', productos=productos_db, destacados=destacados_db)

@public_bp.route('/quienes-somos')
def quienes_somos():
    return render_template('quienes_somos.html')

@public_bp.route('/emprender')
def emprender():
    return render_template('emprender.html')