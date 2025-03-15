from datetime import date
import sqlite3
import logging
from module.Reclamo import Reclamo  # Importa la clase Reclamo

class GestionReclamo:
    def __init__(self, db_nombre='inclutel.db'):
        self.db_nombre = db_nombre
        self.conexion = sqlite3.connect(self.db_nombre)
        self.cursor = self.conexion.cursor()

    def registrar_reclamo(self, fecha, servicio, detalle, socio, estado):
        """Registra un nuevo reclamo en la base de datos."""
        try:
            fecha_actual = date.today()  # Obtiene la fecha actual
            print(f"Fecha a insertar: {fecha_actual}")  # Línea de depuración
            self.cursor.execute("""
                INSERT INTO reclamos (fecha, servicio, detalle, socio, estado)
                VALUES (?, ?, ?, ?, ?)
            """, (fecha_actual, servicio, detalle, socio, estado))
            self.conexion.commit()
            reclamo_id = self.cursor.lastrowid  # Obtiene el ID generado
            print(f"Reclamo registrado con ID: {reclamo_id}")
            return Reclamo(reclamo_id, fecha, servicio, detalle, socio, estado)
        except sqlite3.Error as e:
            print(f"Error al registrar reclamo: {e}")
            return None

    def editar_reclamo(self, id_reclamo, fecha=None, socio=None, detalle=None, estado=None):
        """Edita un reclamo existente en la base de datos."""
        try:
            consulta = "UPDATE reclamos SET "
            parametros = []
            if fecha:
                consulta += "fecha = ?, "
                parametros.append(fecha)
            if socio:
                consulta += "socio = ?, "
                parametros.append(socio)
            if detalle:
                consulta += "detalle = ?, "
                parametros.append(detalle)
            if estado:
                consulta += "estado = ?, "
                parametros.append(estado)

            consulta = consulta.rstrip(', ') + " WHERE id = ?"
            parametros.append(id_reclamo)

            self.cursor.execute(consulta, parametros)
            self.conexion.commit()
            print(f"Reclamo con ID {id_reclamo} actualizado.")
        except sqlite3.Error as e:
            print(f"Error al editar reclamo: {e}")

    def buscar_reclamo(self, id_reclamo):
        """Busca un reclamo por su ID y devuelve su información."""
        self.cursor.execute("SELECT * FROM reclamos WHERE id = ?", (id_reclamo,))
        row = self.cursor.fetchone()
        if row:
            return Reclamo(*row).a_diccionario()
        return None

    def eliminar_reclamo(self, id_reclamo):
        """Elimina un reclamo por su ID."""
        try:
            self.cursor.execute("DELETE FROM reclamos WHERE id = ?", (id_reclamo,))
            self.conexion.commit()
            print(f"Reclamo con ID {id_reclamo} eliminado.")
            return True
        except sqlite3.Error as e:
            print(f"Error al eliminar reclamo: {e}")
            return False

    def cerrar_conexion(self):
        """Cierra la conexión a la base de datos."""
        self.conexion.close()

    def obtener_todos(self):
        """Devuelve todos los reclamos como un diccionario indexado."""
        try:
            self.cursor.execute("SELECT id, fecha, servicio, detalle, socio, estado FROM reclamos")
            reclamos = {}
            for row in self.cursor.fetchall():
                reclamo = {
                    "id": row[0],
                    "fecha": row[1],
                    "servicio": row[2],
                    "detalle": row[3],
                    "socio": row[4],
                    "estado": row[5]
                }
                reclamos[str(row[0])] = reclamo
            return reclamos
        except sqlite3.Error as e:
            logging.error(f"Error al obtener todos los reclamos: {e}")
            return {}

    def obtener_nombre_socio(self, id_socio):
        """Obtiene el nombre de un socio por su ID."""
        try:
            self.cursor.execute("SELECT nombre FROM socios WHERE id = ?", (id_socio,))
            row = self.cursor.fetchone()
            if row:
                return row[0]
            return None
        except sqlite3.Error as e:
            logging.error(f"Error al obtener nombre del socio: {e}")
            return None