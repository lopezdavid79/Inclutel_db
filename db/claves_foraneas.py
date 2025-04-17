import sqlite3

def agregar_claves_foraneas_operador():
    """
    Agrega las claves foráneas para la columna 'operador_id' en las tablas
    'reclamos' y 'operadorturno' referenciando la tabla 'operador' mediante
    la recreación de las tablas.

    Asume que la tabla 'operador' ya existe y está poblada, y que las tablas
    'reclamos' y 'operadorturno' ya tienen la columna 'operador_id' poblada.
    """
    conexion = None
    try:
        # 1. Conexión a la base de datos SQLite
        conexion = sqlite3.connect("inclutel.db")
        cursor = conexion.cursor()

        # --- Agregar clave foránea a la tabla 'reclamos' ---
        print("Agregando clave foránea a la tabla 'reclamos'...")
        cursor.execute("PRAGMA table_info(reclamos)")
        columnas_reclamos_info = cursor.fetchall()
        columnas_reclamos = [info[1] for info in columnas_reclamos_info]

        # Crear la definición de las columnas de la tabla 'reclamos'
        columnas_definicion_reclamos = []
        for info in columnas_reclamos_info:
            name = info[1]
            type = info[2]
            nullable = "NOT NULL" if info[3] == 0 else ""
            primary_key = "PRIMARY KEY AUTOINCREMENT" if info[5] == 1 else ""
            columnas_definicion_reclamos.append(f"{name} {type} {nullable} {primary_key}".strip())
        definicion_columnas_reclamos = ", ".join(columnas_definicion_reclamos)

        # Crear la nueva tabla 'reclamos_temp' con la clave foránea
        cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS reclamos_temp (
                {definicion_columnas_reclamos},
                FOREIGN KEY (operador_id) REFERENCES operador(id) ON DELETE SET NULL
            )
        """)
        conexion.commit()
        print("Tabla temporal 'reclamos_temp' creada.")

        # Migrar los datos de 'reclamos' a 'reclamos_temp'
        cursor.execute(f"INSERT INTO reclamos_temp ({', '.join(columnas_reclamos)}) SELECT * FROM reclamos")
        conexion.commit()
        print("Datos migrados de 'reclamos' a 'reclamos_temp'.")

        # Eliminar la tabla 'reclamos' antigua
        cursor.execute("DROP TABLE reclamos")
        conexion.commit()
        print("Tabla 'reclamos' antigua eliminada.")

        # Renombrar la tabla temporal a 'reclamos'
        cursor.execute("ALTER TABLE reclamos_temp RENAME TO reclamos")
        conexion.commit()
        print("Tabla 'reclamos_temp' renombrada a 'reclamos'.")

        # --- Agregar clave foránea a la tabla 'operadorturno' ---
        print("\nAgregando clave foránea a la tabla 'operadorturno'...")
        cursor.execute("PRAGMA table_info(operadorturno)")
        columnas_turno_info = cursor.fetchall()
        columnas_turno = [info[1] for info in columnas_turno_info]

        # Crear la definición de las columnas de la tabla 'operadorturno'
        columnas_definicion_turno = []
        for info in columnas_turno_info:
            name = info[1]
            type = info[2]
            nullable = "NOT NULL" if info[3] == 0 else ""
            primary_key = "PRIMARY KEY AUTOINCREMENT" if info[5] == 1 else ""
            columnas_definicion_turno.append(f"{name} {type} {nullable} {primary_key}".strip())
        definicion_columnas_turno = ", ".join(columnas_definicion_turno)

        # Crear la nueva tabla 'operadorturno_temp' con la clave foránea
        cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS operadorturno_temp (
                {definicion_columnas_turno},
                FOREIGN KEY (operador_id) REFERENCES operador(id) ON DELETE CASCADE
            )
        """)
        conexion.commit()
        print("Tabla temporal 'operadorturno_temp' creada.")

        # Migrar los datos de 'operadorturno' a 'operadorturno_temp'
        cursor.execute(f"INSERT INTO operadorturno_temp ({', '.join(columnas_turno)}) SELECT * FROM operadorturno")
        conexion.commit()
        print("Datos migrados de 'operadorturno' a 'operadorturno_temp'.")

        # Eliminar la tabla 'operadorturno' antigua
        cursor.execute("DROP TABLE operadorturno")
        conexion.commit()
        print("Tabla 'operadorturno' antigua eliminada.")

        # Renombrar la tabla temporal a 'operadorturno'
        cursor.execute("ALTER TABLE operadorturno_temp RENAME TO operadorTurno")
        conexion.commit()
        print("Tabla 'operadorturno_temp' renombrada a 'operadorTurno'.")

        print("Proceso de adición de claves foráneas completado mediante recreación de tablas.")

    except sqlite3.Error as e:
        print(f"Error durante el proceso: {e}")

    finally:
        if conexion:
            conexion.close()

if __name__ == '__main__':
    agregar_claves_foraneas_operador()