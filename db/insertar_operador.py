import sqlite3
import logging

class GestionOperador:
    def __init__(self, db_nombre="inclutel.db"):
        self.db_nombre = db_nombre
        self.conexion = None
        self.cursor = None
        self._conectar()

    def _conectar(self):
        """Establece la conexión a la base de datos."""
        try:
            self.conexion = sqlite3.connect(self.db_nombre)
            self.cursor = self.conexion.cursor()
        except sqlite3.Error as e:
            logging.error(f"Error al conectar a la base de datos: {e}")

    def _desconectar(self):
        """Cierra la conexión a la base de datos."""
        if self.conexion:
            self.conexion.close()
            self.conexion = None
            self.cursor = None

    def insertar_operador(self, nombre_operador):
        """
        Inserta un nuevo operador en la tabla 'operador'.

        Args:
            nombre_operador (str): El nombre del operador a insertar.

        Returns:
            bool: True si la inserción fue exitosa, False en caso de error
                  o si el operador ya existe.
        """
        try:
            self._conectar()
            # Verificar si el operador ya existe por nombre (evitar duplicados)
            self.cursor.execute("SELECT id FROM operador WHERE nombre = ?", (nombre_operador,))
            if self.cursor.fetchone() is not None:
                logging.warning(f"El operador '{nombre_operador}' ya existe.")
                return False

            self.cursor.execute("INSERT INTO operador (nombre) VALUES (?)", (nombre_operador,))
            self.conexion.commit()
            logging.info(f"Operador '{nombre_operador}' insertado correctamente.")
            return True
        except sqlite3.Error as e:
            logging.error(f"Error al insertar operador '{nombre_operador}': {e}")
            return False
        finally:
            self._desconectar()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    gestion_operador = GestionOperador()

    operadores_a_insertar = ["Mara","Jonatan", "Bruno", "Julio"]

    for operador in operadores_a_insertar:
        if gestion_operador.insertar_operador(operador):
            print(f"Operador '{operador}' insertado.")
        else:
            print(f"No se pudo insertar el operador '{operador}' (puede que ya exista).")