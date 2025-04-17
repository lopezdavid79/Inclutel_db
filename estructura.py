import sqlite3

def mostrar_estructura_db(nombre_db):
    """
    Muestra la estructura de las tablas en una base de datos SQLite.

    Args:
        nombre_db (str): El nombre del archivo de la base de datos.
    """
    try:
        conexion = sqlite3.connect(nombre_db)
        cursor = conexion.cursor()

        # Obtener la lista de tablas
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tablas = cursor.fetchall()

        if not tablas:
            print(f"La base de datos '{nombre_db}' no contiene tablas.")
            return

        print(f"Estructura de la base de datos '{nombre_db}':\n")

        for tabla in tablas:
            nombre_tabla = tabla[0]
            print(f"Tabla: {nombre_tabla}")

            # Obtener información de las columnas de cada tabla
            cursor.execute(f"PRAGMA table_info({nombre_tabla})")
            columnas = cursor.fetchall()

            if columnas:
                print("  Columnas:")
                for columna in columnas:
                    # Índice, Nombre, Tipo, ¿Nullable?, Clave Primaria, Valor por Defecto
                    indice, nombre, tipo, notnull, pk, defecto = columna
                    print(f"    - {nombre} ({tipo})", end="")
                    if notnull:
                        print(" NOT NULL", end="")
                    if pk:
                        print(" PRIMARY KEY", end="")
                    if defecto is not None:
                        print(f" DEFAULT '{defecto}'", end="")
                    print()
            else:
                print("  (La tabla no tiene columnas)")
            print("-" * 30)

        # Obtener información de las claves foráneas
        print("\nClaves Foráneas:")
        for tabla in tablas:
            nombre_tabla = tabla[0]
            cursor.execute(f"PRAGMA foreign_key_list({nombre_tabla})")
            claves_foraneas = cursor.fetchall()
            if claves_foraneas:
                print(f"  Tabla: {nombre_tabla}")
                for fk in claves_foraneas:
                    # id, seq, table, from, to, on_update, on_delete, match
                    id_fk, seq, tabla_ref, columna_local, columna_ref, on_update, on_delete, match = fk
                    print(f"    - Columna Local: {columna_local}, Referencia a Tabla: {tabla_ref}({columna_ref}), ON UPDATE: {on_update}, ON DELETE: {on_delete}")
            else:
                print(f"  Tabla: {nombre_tabla} - No tiene claves foráneas.")

    except sqlite3.Error as e:
        print(f"Error al acceder a la base de datos: {e}")
    finally:
        if conexion:
            conexion.close()

if __name__ == "__main__":
    nombre_base_datos = "inclutel.db"
    mostrar_estructura_db(nombre_base_datos)

    