import sqlite3

def mostrar_operadores(nombre_db):
    """
    Muestra todos los datos de la tabla 'operador' en una base de datos SQLite.

    Args:
        nombre_db (str): El nombre del archivo de la base de datos.
    """
    try:
        conexion = sqlite3.connect(nombre_db)
        cursor = conexion.cursor()

        cursor.execute("SELECT * FROM operador")
        operadores = cursor.fetchall()

        if operadores:
            print("Datos de la tabla 'operador':")
            for operador in operadores:
                print(operador)
        else:
            print("La tabla 'operador' está vacía.")

        # Mostrar datos de la tabla 'OperadorTurno'
        print("Datos de la tabla 'OperadorTurno':")
        cursor.execute("SELECT * FROM OperadorTurno")
        operadores_turno = cursor.fetchall()
        if operadores_turno:
            for turno in operadores_turno:
                print(turno)
        else:
            print("La tabla 'OperadorTurno' está vacía.")

        # Mostrar datos de la tabla 'reclamos'
        input("presionar enter para seguir")
        print("Datos de la tabla 'reclamos':")
        cursor.execute("SELECT * FROM reclamos")
        reclamos = cursor.fetchall()
        if reclamos:
            for reclamo in reclamos:
                print(reclamo)
        else:
            print("La tabla 'reclamos' está vacía.")

    except sqlite3.Error as e:
        print(f"Error al acceder a la base de datos: {e}")


    finally:
        if conexion:
            conexion.close()

if __name__ == "__main__":
    nombre_base_datos = "inclutel.db"
    mostrar_operadores(nombre_base_datos)