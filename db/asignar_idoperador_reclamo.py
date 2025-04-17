import sqlite3

def asignar_operador_unico_a_reclamos(nombre_db, operador_id):
    """
    Asigna un operador específico a todos los registros de la tabla 'reclamos'.

    Args:
        nombre_db (str): El nombre del archivo de la base de datos.
        operador_id (int): El ID del operador que se asignará a los reclamos.
    """
    conexion = None
    try:
        conexion = sqlite3.connect(nombre_db)
        cursor = conexion.cursor()

        # Verificar si la columna 'operador_id' existe en la tabla 'reclamos'
        cursor.execute("PRAGMA table_info(reclamos)")
        columnas_reclamos = [info[1] for info in cursor.fetchall()]
        if "operador_id" not in columnas_reclamos:
            print(f"Error: La columna 'operador_id' no existe en la tabla 'reclamos' de la base de datos '{nombre_db}'.")
            return

        # Actualizar todos los registros de 'reclamos' con el operador_id proporcionado
        cursor.execute("UPDATE reclamos SET operador_id = ?", (operador_id,))
        conexion.commit()
        print(f"Se asignó el operador con ID {operador_id} a todos los registros de la tabla 'reclamos' en '{nombre_db}'.")

    except sqlite3.Error as e:
        print(f"Error al acceder o modificar la base de datos: {e}")

    finally:
        if conexion:
            conexion.close()

if __name__ == "__main__":
    nombre_base_datos = "inclutel.db"
    id_operador_unico = 1  # Reemplaza con el ID del operador que deseas asignar

    asignar_operador_unico_a_reclamos(nombre_base_datos, id_operador_unico)