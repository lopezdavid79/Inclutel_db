import sqlite3

def migrar_datos_con_estructura_destino(db_origen_path, db_destino_path):
    """Migra los datos de las tablas coincidentes de la base de datos origen a la base de datos destino,
    respetando la estructura de la base de datos destino."""
    try:
        conn_origen = sqlite3.connect(db_origen_path)
        cursor_origen = conn_origen.cursor()

        conn_destino = sqlite3.connect(db_destino_path)
        cursor_destino = conn_destino.cursor()

        # Obtener la lista de tablas en la base de datos destino
        cursor_destino.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tablas_destino = [row[0] for row in cursor_destino.fetchall()]

        for tabla in tablas_destino:
            print(f"Procesando tabla: {tabla}")

            # Verificar si la tabla existe en la base de datos origen
            cursor_origen.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{tabla}';")
            tabla_origen_existe = cursor_origen.fetchone()

            if tabla_origen_existe:
                print(f"  La tabla '{tabla}' existe en ambas bases de datos. Intentando migrar datos...")

                # Obtener los nombres de las columnas de la tabla destino
                cursor_destino.execute(f"PRAGMA table_info({tabla})")
                columnas_destino_info = cursor_destino.fetchall()
                nombres_columnas_destino = [info[1] for info in columnas_destino_info]
                placeholders = ', '.join(['?'] * len(nombres_columnas_destino))
                insert_sql = f"INSERT INTO {tabla} ({', '.join(nombres_columnas_destino)}) VALUES ({placeholders})"

                # Obtener los datos correspondientes de la tabla origen (seleccionando solo las columnas que existen en destino)
                columnas_origen_info = cursor_origen.execute(f"PRAGMA table_info({tabla})").fetchall()
                nombres_columnas_origen = [info[1] for info in columnas_origen_info]
                columnas_a_seleccionar = [col for col in nombres_columnas_destino if col in nombres_columnas_origen]
                if columnas_a_seleccionar:
                    select_sql = f"SELECT {', '.join(columnas_a_seleccionar)} FROM {tabla}"
                    cursor_origen.execute(select_sql)
                    datos_origen = cursor_origen.fetchall()

                    # Insertar los datos en la tabla destino
                    for fila in datos_origen:
                        try:
                            # Asegurarse de que la fila tenga la misma cantidad de columnas que la sentencia INSERT
                            if len(fila) <= len(nombres_columnas_destino):
                                cursor_destino.execute(insert_sql, fila)
                            else:
                                print(f"  Advertencia: La fila de la tabla '{tabla}' en la base de datos origen tiene más columnas que la tabla destino. Se omitirán las columnas extra.")
                        except sqlite3.Error as e:
                            print(f"  Error al insertar datos en la tabla '{tabla}': {e} - Fila: {fila}")
                            conn_destino.rollback() # Revertir la inserción fallida para esta tabla

                    conn_destino.commit()
                    print(f"  Datos de la tabla '{tabla}' migrados exitosamente.")
                else:
                    print(f"  Advertencia: No hay columnas coincidentes entre las tablas '{tabla}' en las bases de datos origen y destino.")
            else:
                print(f"  La tabla '{tabla}' no existe en la base de datos origen.")

        print("Migración de datos completada.")

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
    db_origen = 'data_inclutel.db'
    db_destino = 'inclutel.db'

    migrar_datos_con_estructura_destino(db_origen, db_destino)