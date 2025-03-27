import sqlite3

def crear_tablas():
    """Crea las tablas 'socios' y 'reclamos' en la base de datos si no existen."""
    try:
        conexion = sqlite3.connect("inclutel.db")
        cursor = conexion.cursor()

        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS socios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT,
                domicilio TEXT,
                telefono INTEGER,
                n_socio TEXT NULL
            )
        """)

        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS reclamos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                fecha DATE,
                servicio TEXT,
                detalle TEXT,
                socio INTEGER,  -- Clave foránea que referencia a socios.id
                estado TEXT,
                FOREIGN KEY (socio) REFERENCES socios(id)  -- Define la clave foránea
            )
        """)

        conexion.commit()  
        print("Tablas 'socios' y 'reclamos' creadas correctamente.")

    except sqlite3.Error as e:
        print(f"Error al crear las tablas: {e}")

    finally:
        if conexion:
            conexion.close()

if __name__ == "__main__":
    crear_tablas()