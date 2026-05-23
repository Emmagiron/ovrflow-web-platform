import sqlite3

def reparacion_total():
    conn = sqlite3.connect('proyecto.db')
    cursor = conn.cursor()
    
    try:
        print("Iniciando actualización de estructura (Agregando columna STOCK)...")
        
        # 1. Renombramos la tabla actual
        cursor.execute("ALTER TABLE productos RENAME TO productos_temp")
        
        # 2. Creamos la tabla con TODAS las columnas que pide tu código
        cursor.execute('''
            CREATE TABLE productos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                descripcion TEXT,
                precio REAL,
                imagen TEXT,
                stock INTEGER DEFAULT 0,  -- <-- Aquí está la columna que falta
                fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # 3. Migramos los datos (ajustamos las columnas según lo que tenías)
        cursor.execute('''
            INSERT INTO productos (id, nombre, descripcion, precio, imagen, fecha_creacion)
            SELECT id, nombre, descripcion, precio, imagen, fecha_creacion FROM productos_temp
        ''')
        
        # 4. Borramos la temporal
        cursor.execute("DROP TABLE productos_temp")
        
        conn.commit()
        print("✅ ¡Estructura actualizada! Columna 'stock' añadida correctamente.")
        
    except Exception as e:
        conn.rollback()
        print(f"❌ Error: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    reparacion_total()