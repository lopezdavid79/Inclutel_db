import sqlite3
import logging

class GestionSocio:
    def __init__(self, db_nombre="inclutel.db"):
        """Inicializa la clase y establece la conexión con la base de datos."""
        try:
            self.conexion = sqlite3.connect(db_nombre)
            self.cursor = self.conexion.cursor()
            self.cursor.execute("PRAGMA foreign_keys = 1")
            self.conexion.commit()
            logging.info("Conexión a la base de datos establecida.")
        except sqlite3.Error as e:
            logging.error(f"Error al conectar a la base de datos: {e}")
            self.conexion = None

    def cerrar_conexion(self):
        """Cierra la conexión con la base de datos."""
        if self.conexion:
            self.conexion.close()
            logging.info("Conexión a la base de datos cerrada.")

    def registrar_socio(self, nombre, domicilio, telefono, n_socio):
        """Registra un nuevo socio en la base de datos."""
        try:
            self.cursor.execute("INSERT INTO socios (nombre, domicilio, telefono, n_socio) VALUES (?, ?, ?, ?)",
                                (nombre, domicilio, telefono, n_socio))
            self.conexion.commit()
            logging.info(f"Socio {n_socio} registrado.")
            return True
        except sqlite3.IntegrityError:
            logging.warning(f"El número de socio {n_socio} ya existe.")
            return False
        except sqlite3.Error as e:
            logging.error(f"Error al registrar socio: {e}")
            return False
    def obtener_todos(self):
        """Recupera todos los socios de la base de datos."""
        try:
            self.cursor.execute("SELECT id, nombre, domicilio, telefono, n_socio FROM socios")
            socios = {str(row[0]): {"nombre": row[1], "domicilio": row[2], "telefono": row[3], "n_socio": row[4]}
                      for row in self.cursor.fetchall()}

            # Depurador: Imprimir los datos de los socios
            print("Datos de los socios:")
            for id_socio, datos_socio in socios.items():
                print(f"  ID: {id_socio}")
                print(f"  Nombre: {datos_socio['nombre']}")
                print(f"  Domicilio: {datos_socio['domicilio']}")
                print(f"  Teléfono: {datos_socio['telefono']}")
                print(f"  Número de socio: {datos_socio['n_socio']}")
                print("-" * 20)

            return socios
        except sqlite3.Error as e:
            logging.error(f"Error al obtener socios: {e}")
            return {}
        
    def editar_socio(self, id_socio, nombre, domicilio, telefono, n_socio):
        """Actualiza los datos de un socio existente."""
        try:
            self.cursor.execute("UPDATE socios SET nombre = ?, domicilio = ?, telefono = ?, n_socio = ? WHERE id = ?",
                                (nombre, domicilio, telefono, n_socio, id_socio))
            self.conexion.commit()
            logging.info(f"Socio {id_socio} actualizado.")
        except sqlite3.Error as e:
            logging.error(f"Error al editar socio: {e}")

    def eliminar_socio(self, id_socio):
        """Elimina un socio por su ID."""
        try:
            self.cursor.execute("DELETE FROM socios WHERE id = ?", (id_socio,))
            self.conexion.commit()
            logging.info(f"Socio {id_socio} eliminado.")
        except sqlite3.Error as e:
            logging.error(f"Error al eliminar socio: {e}")


    def buscar_socio(self, id_socio):
        """Busca un socio por su ID y devuelve sus datos en un diccionario."""
        try:
            self.cursor.execute("SELECT id, nombre, domicilio, telefono, n_socio FROM socios WHERE id = ?", (id_socio,))
            resultado = self.cursor.fetchone()

            if resultado:
                socio = {
                    "id": resultado[0],
                    "nombre": resultado[1],
                    "domicilio": resultado[2],
                    "telefono": resultado[3],
                    "n_socio": resultado[4]
                }
                return socio
            else:
                return None  # Devuelve None si no se encuentra el socio

        except sqlite3.Error as e:
            logging.error(f"Error al buscar el socio: {e}")
            return None  # Devuelve None en caso de error


    def obtener_socio_por_nombre(self, nombre_socio):
        """Recupera un socio por nombre de la base de datos."""
        try:
            self.cursor.execute("SELECT id, nombre, domicilio, telefono, n_socio FROM socios WHERE nombre = ?", (nombre_socio,))
            socio = self.cursor.fetchone()

            if socio:
                # Convertir el resultado a un diccionario
                socio_dict = {
                    "id": socio[0],
                    "nombre": socio[1],
                    "domicilio": socio[2],
                    "telefono": socio[3],
                    "n_socio": socio[4]
                }
                return socio_dict
            else:
                return None  # Retorna None si no se encuentra el socio

        except sqlite3.Error as e:
            logging.error(f"Error al obtener socio por nombre: {e}")
            return None