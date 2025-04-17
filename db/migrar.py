import sqlite3
import os

def migrar_base_de_datos(db_origen_path, db_destino_path):
    """Migra todos los datos de todas las tablas de una base de datos SQLite a otra."""
    try:
        conn_origen = sqlite3.connect(db_origen_path)
        cursor_origen = conn_origen.cursor()

        conn_destino = sqlite3.connect(db_destino_path)
        cursor_destino = conn_destino.cursor()

        # Obtener la lista de todas las tablas en la base de datos origen
        cursor_origen.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tablas_origen = [row[0] for row in cursor_origen.fetchall()]

        if not os.path.exists(db_destino_path):
            print(f"Creando la base de datos destino: {db_destino_path}")

        for tabla in tablas_origen:
            print(f"Migrando tabla: {tabla}")

            # Obtener todos los datos de la tabla origen
            cursor_origen.execute(f"SELECT * FROM {tabla}")
            datos = cursor_origen.fetchall()

            # Obtener la estructura de la tabla origen (nombres de las columnas)
            cursor_origen.execute(f"PRAGMA table_info({tabla})")
            columnas_info = cursor_origen.fetchall()
            nombres_columnas = [info[1] for info in columnas_info]
            placeholders = ', '.join(['?'] * len(nombres_columnas))
            insert_sql = f"INSERT INTO {tabla} ({', '.join(nombres_columnas)}) VALUES ({placeholders})"

            # Crear la tabla en la base de datos destino si no existe (copiando la estructura)
            cursor_origen.execute(f"SELECT sql FROM sqlite_master WHERE type='table' AND name='{tabla}'")
            create_table_sql = cursor_origen.fetchone()
            if create_table_sql:
                try:
                    cursor_destino.execute(create_table_sql[0])
                    conn_destino.commit()
                except sqlite3.OperationalError as e:
                    print(f"Advertencia: No se pudo crear la tabla '{tabla}' en la base de datos destino. Puede que ya exista o haya un error en la definición: {e}")

            # Insertar los datos en la tabla destino
            for fila in datos:
                try:
                    cursor_destino.execute(insert_sql, fila)
                except sqlite3.Error as e:
                    print(f"Error al insertar datos en la tabla '{tabla}': {e} - Fila: {fila}")
                    conn_destino.rollback() # Revertir la inserción fallida para esta tabla

            conn_destino.commit()
            print(f"Tabla '{tabla}' migrada exitosamente.")

        print("Migración de base de datos completada.")

    except sqlite3.Error as e:
        if conn_destino:
            conn_destino.rollback()
        print(f"Error general durante la migración: {e}")

    finally:
        if conn_origen:
            conn_origen.close()
        if conn_destino:
            conn_destino.close()

if __name__ == '__main__':
    db_origen = 'backupps/data_inclutel.db'
    db_destino = 'inclutel.db'

    migrar_base_de_datos(db_origen, db_destino)