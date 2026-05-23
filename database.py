import sqlite3
import os
from werkzeug.security import generate_password_hash, check_password_hash

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DB_PATH = os.path.join(BASE_DIR, 'proyecto.db')

def obtener_conexion():
    try:
        conexion = sqlite3.connect(DB_PATH)
        conexion.row_factory = sqlite3.Row 
        return conexion
    except sqlite3.Error as e:
        print(f">>> Error al conectar con la base de datos: {e}")
        return None

def crear_tablas():
    conexion = obtener_conexion()
    if not conexion:
        return

    cursor = conexion.cursor()
    
    # 1. Tabla de Productos (Estructura Limpia Relacional)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS productos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            codigo TEXT UNIQUE,
            nombre TEXT NOT NULL,
            descripcion TEXT,
            precio REAL NOT NULL,
            precio_oferta REAL,
            cantidad_oferta INTEGER,
            imagen TEXT DEFAULT 'default.png',
            fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # NUEVA: Tabla relacional para controlar el stock real de cada talle individual
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS stock_talles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            producto_id INTEGER NOT NULL,
            talle TEXT NOT NULL,
            cantidad INTEGER DEFAULT 0,
            FOREIGN KEY (producto_id) REFERENCES productos(id) ON DELETE CASCADE,
            UNIQUE(producto_id, talle)
        )
    ''')

    # 3. Tabla de Ventas e Historial Diario
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS ventas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            producto_id INTEGER,
            talle TEXT NOT NULL,
            cantidad INTEGER NOT NULL,
            precio_unitario REAL NOT NULL,
            total_venta REAL NOT NULL,
            fecha_hora DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (producto_id) REFERENCES productos(id)
        )
    ''')
    
    # 4. Tabla de Usuarios
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            rol TEXT DEFAULT 'admin'
        )
    ''')
    
    
    try:
        pass_hash = generate_password_hash('admin123')
        cursor.execute('INSERT INTO usuarios (username, password, rol) VALUES (?, ?, ?)', 
                       ('admin', pass_hash, 'admin'))
        print(">>> Usuario 'admin' de OVRFLOW configurado.")
    except sqlite3.IntegrityError:
        pass

    # Creamos los índices de velocidad
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_ventas_fecha ON ventas(fecha_venta)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_stock_producto ON stock_talles(producto_id)")

    conexion.commit()
    conexion.close()
    print(">>> Base de datos lista para usar en la ruta:", DB_PATH)

def actualizar_producto(id, codigo, nombre, precio, precio_oferta, cantidad_oferta, descripcion, stock_talles_dict, imagen=None):
    db = obtener_conexion()
    cursor = db.cursor()
    
    # 1. Actualizamos los datos generales en la tabla productos
    if imagen:
        cursor.execute('''
            UPDATE productos 
            SET codigo=?, nombre=?, precio=?, precio_oferta=?, cantidad_oferta=?, descripcion=?, imagen=?
            WHERE id=?
        ''', (codigo, nombre, precio, precio_oferta, cantidad_oferta, descripcion, imagen, id))
    else:
        cursor.execute('''
            UPDATE productos 
            SET codigo=?, nombre=?, precio=?, precio_oferta=?, cantidad_oferta=?, descripcion=?
            WHERE id=?
        ''', (codigo, nombre, precio, precio_oferta, cantidad_oferta, descripcion, id))
        
    # 2. Actualizamos o insertamos el stock correspondiente a cada talle enviado
    for talle, cantidad in stock_talles_dict.items():
        cursor.execute('''
            INSERT INTO stock_talles (producto_id, talle, cantidad)
            VALUES (?, ?, ?)
            ON CONFLICT(producto_id, talle) DO UPDATE SET cantidad = excluded.cantidad
        ''', (id, talle, int(cantidad if cantidad else 0)))
        
    db.commit()
    db.close()

# Removimos la función vieja de actualizar_producto ya que ahora la lógica modular
# vive directamente adentro del POST de tus Blueprints en routes/admin.py