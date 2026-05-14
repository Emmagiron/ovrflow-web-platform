import sqlite3
import os
from werkzeug.security import generate_password_hash, check_password_hash

# Configuramos la ruta dinámica para que la DB se cree siempre en la carpeta del proyecto
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DB_PATH = os.path.join(BASE_DIR, 'proyecto.db')

def obtener_conexion():
    """Establece conexión con la base de datos usando rutas relativas."""
    try:
        conexion = sqlite3.connect(DB_PATH)
        conexion.row_factory = sqlite3.Row 
        return conexion
    except sqlite3.Error as e:
        print(f">>> Error al conectar con la base de datos: {e}")
        return None

def crear_tablas():
    """Crea la estructura de tablas para OVRFLOW si no existen."""
    conexion = obtener_conexion()
    if not conexion:
        return

    cursor = conexion.cursor()
    
    # 1. Tabla de Productos mejorada
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS productos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            codigo TEXT UNIQUE NOT NULL,
            nombre TEXT NOT NULL,
            descripcion TEXT,
            precio REAL NOT NULL,
            precio_oferta REAL,
            cantidad_oferta INTEGER,
            talles TEXT,
            stock INTEGER DEFAULT 0,
            imagen TEXT DEFAULT 'default.png',
            fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # 2. Tabla de Usuarios
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            rol TEXT DEFAULT 'admin'
        )
    ''')
    
    # 3. Usuario administrador por defecto seguro
    try:
        # User: admin | Pass: admin123 (Se recomienda cambiar después de instalar)
        pass_hash = generate_password_hash('admin123')
        cursor.execute('INSERT INTO usuarios (username, password, rol) VALUES (?, ?, ?)', 
                       ('admin', pass_hash, 'admin'))
        print(">>> Usuario 'admin' de OVRFLOW configurado.")
    except sqlite3.IntegrityError:
        print(">>> El sistema de usuarios ya está inicializado.")

    conexion.commit()
    conexion.close()
    print(">>> Base de datos lista para usar en la ruta:", DB_PATH)

def verificar_usuario(username, password):
    """Función auxiliar para validar credenciales en app.py."""
    db = obtener_conexion()
    user = db.execute('SELECT * FROM usuarios WHERE username = ?', (username,)).fetchone()
    db.close()
    
    if user and check_password_hash(user['password'], password):
        return True
    return False

def actualizar_producto(id, codigo, nombre, precio, precio_oferta, cantidad_oferta, talles, stock, imagen):
    db = obtener_conexion()
    db.execute('''
        UPDATE productos 
        SET codigo=?, nombre=?, precio=?, precio_oferta=?, cantidad_oferta=?, talles=?, stock=?, imagen=?
        WHERE id=?
    ''', (codigo, nombre, precio, precio_oferta, cantidad_oferta, talles, stock, imagen, id))
    db.commit()
    db.close()

if __name__ == '__main__':
    crear_tablas()