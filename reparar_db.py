import sqlite3
import os

# Asegúrate de que la ruta coincida con la de tu database.py
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DB_PATH = os.path.join(BASE_DIR, 'proyecto.db')

def migrar_db():
    conexion = sqlite3.connect(DB_PATH)
    cursor = conexion.cursor()
    
    try:
        print(">>> Intentando agregar la columna 'rol' a la tabla usuarios...")
        cursor.execute('ALTER TABLE usuarios ADD COLUMN rol TEXT DEFAULT "admin"')
        conexion.commit()
        print(">>> Columna 'rol' agregada con éxito.")
    except sqlite3.OperationalError:
        print(">>> La columna 'rol' ya existe o hubo un problema.")
    finally:
        conexion.close()

if __name__ == '__main__':
    migrar_db()