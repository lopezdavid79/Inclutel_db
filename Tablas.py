import sqlite3

def crear_tablas():
    """Crea las tablas 'socios', 'reclamos' y 'operador' en la base de datos si no existen."""
    try:
        conexion = sqlite3.connect("inclutel.db")
        cursor = conexion.cursor()

        # Crear la tabla 'socios'
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS socios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT,
                domicilio TEXT,
                telefono INTEGER,
                n_socio TEXT NULL
            )
        """)
        print("Tabla 'socios' creada (si no existía).")

        # Crear la tabla 'operador'
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS operador (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL UNIQUE
            )
        """)
        print("Tabla 'operador' creada (si no existía).")

        # Crear la tabla 'reclamos'
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS reclamos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                fecha DATE,
                servicio TEXT,
                detalle TEXT,
                socio INTEGER,  -- Clave foránea que referencia a socios.id
                estado TEXT,
                operador_id INTEGER,
                FOREIGN KEY (socio) REFERENCES socios(id),  -- Define la clave foránea
                FOREIGN KEY (operador_id) REFERENCES operador(id)  -- Define la clave foránea
            )
        """)
        print("Tabla 'reclamos' creada (si no existía).")

        # Crear la tabla 'operadorturno'
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS operadorturno (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                fecha TEXT NOT NULL,
                comienzo TIME NOT NULL,
                fin TIME NOT NULL,
                operador_id INTEGER,
                FOREIGN KEY (operador_id) REFERENCES operador(id)  -- Define la clave foránea
            )
        """)
        print("Tabla 'operadorturno' creada (si no existía).")

        conexion.commit()
        print("Todas las tablas verificadas y/o creadas correctamente.")

    except sqlite3.Error as e:
        print(f"Error al crear las tablas: {e}")

    finally:
        if conexion:
            conexion.close()

if __name__ == '__main__':
    crear_tablas()