import sqlite3

def migrar_operadores():
    """
    Migra la información de operadores a una tabla separada ('operador') y actualiza
    las referencias en las tablas 'reclamo' y 'operadorturno'.

    Asume que las tablas 'reclamo' y 'operadorturno' ya existen.
    """
    try:
        # 1. Conexión a la base de datos SQLite
        conexion = sqlite3.connect("inclutel.db")
        cursor = conexion.cursor()

        # 2. Crear la tabla 'operador' si no existe
        #    Esta tabla contendrá los nombres únicos de los operadores y un ID autoincremental.
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS operador (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL UNIQUE
            )
        """)
        conexion.commit()
        print("Tabla 'operador' creada (si no existía).")

        # 3. Poblar la tabla 'operador' desde la tabla 'operadorturno'
        #    Selecciona los nombres de operador únicos de 'operadorturno' y los inserta en 'operador'.
        cursor.execute("SELECT DISTINCT nombre FROM operadorturno")
        nombres_operadores_turno = [row[0] for row in cursor.fetchall()]
        for nombre in nombres_operadores_turno:
            try:
                cursor.execute("INSERT INTO operador (nombre) VALUES (?)", (nombre,))
            except sqlite3.IntegrityError:
                # Ignora los errores si el nombre del operador ya existe en la tabla 'operador'
                pass
        conexion.commit()
        print("Tabla 'operador' poblada desde 'operadorturno'.")

                # 4. Agregar la columna 'operador_id' a la tabla 'reclamos' si no existe
        #    Esta columna se utilizará para referenciar al operador responsable del reclamo.
        cursor.execute("PRAGMA table_info(reclamos)")
        columnas_reclamo = [info[1] for info in cursor.fetchall()]
        if "operador_id" not in columnas_reclamo:
            cursor.execute("ALTER TABLE reclamos ADD COLUMN operador_id INTEGER")
            conexion.commit()
            print("Columna 'operador_id' agregada a la tabla 'reclamos'.")

        # 5. Actualizar la tabla 'reclamos' asignando el operador_id
        #    Se relaciona cada registro de 'reclamos' con el 'id' correspondiente
        #    de la tabla 'operador' basándose en la coincidencia del nombre (si existía).
        cursor.execute("PRAGMA table_info(reclamos)")
        columnas_reclamo_pre_update = [info[1] for info in cursor.fetchall()]
        if "operador" in columnas_reclamo_pre_update:
            cursor.execute("SELECT id, operador FROM reclamos")
            reclamos_con_nombre = cursor.fetchall()
            for reclamo_id, operador_nombre in reclamos_con_nombre:
                cursor.execute("SELECT id FROM operador WHERE nombre = ?", (operador_nombre,))
                operador_resultado = cursor.fetchone()
                if operador_resultado:
                    operador_id = operador_resultado[0]
                    cursor.execute("UPDATE reclamos SET operador_id = ? WHERE id = ?", (operador_id, reclamo_id))
            conexion.commit()
            print("Tabla 'reclamos' actualizada con 'operador_id' basado en la columna 'operador'.")

            # 6. (Opcional) Eliminar la columna antigua de operador de 'reclamos'
            cursor.execute("PRAGMA table_info(reclamos)")
            columnas_reclamo_post_update = [info[1] for info in cursor.fetchall()]
            if "operador" in columnas_reclamo_post_update:
                cursor.execute("ALTER TABLE reclamos DROP COLUMN operador")
                conexion.commit()
                print("Columna 'operador' eliminada de 'reclamos'.")

        # 7. Agregar la columna 'operador_id' a la tabla 'operadorturno' si no existe
        cursor.execute("PRAGMA table_info(operadorturno)")
        columnas_turno = [info[1] for info in cursor.fetchall()]
        if "operador_id" not in columnas_turno:
            cursor.execute("ALTER TABLE operadorturno ADD COLUMN operador_id INTEGER")
            conexion.commit()
            print("Columna 'operador_id' agregada a la tabla 'operadorturno'.")

        # 8. Actualizar la tabla 'OperadorTurno' asignando el operador_id
        cursor.execute("SELECT id, nombre FROM operadorturno")
        turnos_con_nombre = cursor.fetchall()
        for turno_id, operador_nombre in turnos_con_nombre:
            cursor.execute("SELECT id FROM operador WHERE nombre = ?", (operador_nombre,))
            operador_resultado = cursor.fetchone()
            if operador_resultado:
                operador_id = operador_resultado[0]
                cursor.execute("UPDATE operadorturno SET operador_id = ? WHERE id = ?", (operador_id, turno_id))
        conexion.commit()
        print("Tabla 'operadorturno' actualizada con 'operador_id'.")

        # 9. Eliminar la columna 'nombre' de 'OperadorTurno'
        cursor.execute("PRAGMA table_info(operadorturno)")
        columnas_turno_post_add = [info[1] for info in cursor.fetchall()]
        if "nombre" in columnas_turno_post_add:
            cursor.execute("ALTER TABLE operadorturno DROP COLUMN nombre")
            conexion.commit()
            print("Columna 'nombre' eliminada de 'operadorturno'.")

# 10. Agregar la clave foránea a 'operador_id' en 'operadorturno'
        cursor.execute("""
            ALTER TABLE operadorturno
            ADD CONSTRAINT fk_operador_turno
            FOREIGN KEY (operador_id) REFERENCES operador(id)
            ON DELETE CASCADE
        """)
        conexion.commit()
        print("Clave foránea agregada para 'operador_id' en la tabla 'operadorturno'.")
        # 11. Agregar la clave foránea a 'operador_id' en 'reclamo'
        cursor.execute("""
            ALTER TABLE reclamo
            ADD FOREIGN KEY (operador_id) REFERENCES operador(id)
            ON DELETE SET NULL
        """)
        conexion.commit()
        print("Clave foránea agregada para 'operador_id' en la tabla 'reclamo'.")

    except sqlite3.Error as e:
        print(f"Error durante la migración: {e}")

    finally:
        # 12. Cerrar la conexión a la base de datos
        if conexion:
            conexion.close()

if __name__ == '__main__':
    migrar_operadores()