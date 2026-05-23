import sqlite3
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DB_PATH = os.path.join(BASE_DIR, 'proyecto.db')

def actualizar_tabla_ventas():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        print("Revisando y actualizando la estructura de la tabla 'ventas'...")
        
        # 1. Borramos la tabla vieja de ventas si quedó mal estructurada o vacía
        # (Es seguro hacerlo ahora ya que estamos en pleno desarrollo local)
        cursor.execute("DROP TABLE IF EXISTS ventas")
        
        # 2. Creamos la tabla 'ventas' con la estructura relacional exacta que pide el panel
        cursor.execute('''
            CREATE TABLE ventas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                producto_id INTEGER NOT NULL,
                talle TEXT NOT NULL,
                cantidad INTEGER NOT NULL,
                precio_unitario REAL NOT NULL,
                total_venta REAL NOT NULL,
                fecha_venta DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (producto_id) REFERENCES productos(id) ON DELETE CASCADE
            )
        ''')
        
        conn.commit()
        print("✅ ¡Estructura corregida con éxito! Columna 'fecha_venta' creada e inicializada.")
        
    except Exception as e:
        conn.rollback()
        print(f"❌ Error al intentar reparar la base de datos: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    actualizar_tabla_ventas()