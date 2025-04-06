from datetime import datetime
import sqlite3
import logging
import os
import sys

# Configuración del logging
logging.basicConfig(filename='mi_programa.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')



class OperadorTurno:
    def __init__(self, nombre, fecha,comienzo, fin):
        self.nombre = nombre
        self.fecha = datetime.now().date()
        self.comienzo = comienzo  # str, ej: "08:00"
        self.fin = fin            # str, ej: "16:00"

    def __str__(self):
        return (f"Operador: {self.nombre}\n"
                f"Fecha: {self.fecha.strftime('%d/%m/%Y')}\n"
                f"Hora de comienzo: {self.hora_comienzo}\n"
                f"Hora de fin: {self.hora_fin}")

class GestionOperadorTurno:
    def __init__(self, db_nombre="inclutel.db"):
        try:
            db_path = os.path.join(getattr(sys, '_MEIPASS', os.path.abspath('.')), db_nombre)
            self.conexion = sqlite3.connect(db_path)
            self.cursor = self.conexion.cursor()
            self.cursor.execute("PRAGMA foreign_keys = 1")
            self.conexion.commit()
            self.crear_tabla()
            logging.info(f"Conexión a la base de datos establecida en: {db_path}")
        except sqlite3.Error as e:
            logging.error(f"Error al conectar a la base de datos: {e}")
            self.conexion = None

    def crear_tabla(self):
        """Crea la tabla OperadorTurno si no existe."""
        try:
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS OperadorTurno (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre TEXT NOT NULL,
                    fecha TEXT NOT NULL,
                    comienzo TIME NOT NULL,
                    fin TIME NOT NULL
                )
            """)
            self.conexion.commit()
            logging.info("Tabla OperadorTurno verificada/creada.")
        except sqlite3.Error as e:
            logging.error(f"Error al crear la tabla OperadorTurno: {e}")

    def cerrar_conexion(self):
        if self.conexion:
            self.conexion.close()
            logging.info("Conexión cerrada.")


    def registrar_operador(self, operador: OperadorTurno):
        try:
            self.cursor.execute(
                "INSERT INTO OperadorTurno (nombre, fecha, comienzo, fin) VALUES (?, ?, ?, ?)",
                (operador.nombre, operador.fecha, operador.comienzo, operador.fin)
            )
            self.conexion.commit()
            logging.info(f"Operador '{operador.nombre}' registrado correctamente.")
            return True
        except sqlite3.Error as e:
            logging.error(f"Error al registrar operador: {e}")
            return False

    def obtener_todos(self):
        try:
            self.cursor.execute("SELECT id, nombre, comienzo, fin FROM OperadorTurno")
            operadores = {
                str(row[0]): {"nombre": row[1], "comienzo": row[2], "fin": row[3]}
                for row in self.cursor.fetchall()
            }

            print("📋 Lista de operadores:")
            for id_op, datos in operadores.items():
                print(f"  ID: {id_op}")
                print(f"  Nombre: {datos['nombre']}")
                print(f"  Comienzo: {datos['comienzo']}")
                print(f"  Fin: {datos['fin']}")
                print("-" * 20)

            return operadores
        except sqlite3.Error as e:
            logging.error(f"Error al obtener operadores: {e}")
            return {}

    def editar_operador(self, id_op, nombre, comienzo, fin):
        try:
            self.cursor.execute("""
                UPDATE OperadorTurno SET nombre = ?, comienzo = ?, fin = ?
                WHERE id = ?
            """, (nombre, comienzo, fin, id_op))
            self.conexion.commit()
            logging.info(f"Operador {id_op} actualizado.")
        except sqlite3.Error as e:
            logging.error(f"Error al editar operador: {e}")

    def eliminar_operador(self, id_op):
        try:
            self.cursor.execute("DELETE FROM OperadorTurno WHERE id = ?", (id_op,))
            self.conexion.commit()
            logging.info(f"Operador {id_op} eliminado.")
        except sqlite3.Error as e:
            logging.error(f"Error al eliminar operador: {e}")

    def buscar_operador(self, id_op):
        try:
            self.cursor.execute("SELECT id, nombre, comienzo, fin FROM OperadorTurno WHERE id = ?", (id_op,))
            resultado = self.cursor.fetchone()

            if resultado:
                return {
                    "id": resultado[0],
                    "nombre": resultado[1],
                    "comienzo": resultado[2],
                    "fin": resultado[3]
                }
            else:
                return None
        except sqlite3.Error as e:
            logging.error(f"Error al buscar operador: {e}")
            return None

    def obtener_por_nombre(self, nombre):
        try:
            self.cursor.execute("SELECT id, nombre, comienzo, fin FROM OperadorTurno WHERE LOWER(nombre) = LOWER(?)", (nombre,))
            resultado = self.cursor.fetchone()
            if resultado:
                return {
                    "id": resultado[0],
                    "nombre": resultado[1],
                    "comienzo": resultado[2],
                    "fin": resultado[3]
                }
            return None
        except sqlite3.Error as e:
            logging.error(f"Error al buscar por nombre: {e}")
            return None

    def buscar_por_nombre_parcial(self, parcial):
        try:
            self.cursor.execute("SELECT id, nombre, comienzo, fin FROM OperadorTurno WHERE LOWER(nombre) LIKE ?", ('%' + parcial.lower() + '%',))
            resultados = self.cursor.fetchall()
            encontrados = [{"id": r[0], "nombre": r[1], "comienzo": r[2], "fin": r[3]} for r in resultados]

            print("🔍 Operadores encontrados:")
            for op in encontrados:
                print(f"  ID: {op['id']} - Nombre: {op['nombre']} - Turno: {op['comienzo']} a {op['fin']}")

            return encontrados
        except sqlite3.Error as e:
            logging.error(f"Error al buscar operadores por nombre parcial: {e}")
            return []


    def existe_turno(self, nombre, fecha, comienzo, fin):

        try:
            self.cursor.execute("""
                SELECT 1 FROM OperadorTurno 
                WHERE LOWER(nombre) = ? AND fecha = ? AND comienzo = ? AND fin = ?
            """, (nombre.lower(), fecha, comienzo, fin))

            resultado = self.cursor.fetchone()
            existe = resultado is not None

            if existe:
                print(f"⚠️ Ya existe un turno registrado para: {nombre} - {fecha} ({comienzo} a {fin})")
            else:
                print(f"✅ Turno disponible para: {nombre} - {fecha} ({comienzo} a {fin})")

            return existe

        except sqlite3.Error as e:
            logging.error(f"Error al verificar existencia del turno: {e}")
            return False





    def existe_y_esta_dentro_del_horario(self, nombre, fecha, comienzo, fin):
        try:
            self.cursor.execute("""
                SELECT comienzo, fin FROM OperadorTurno
                WHERE LOWER(nombre) = ? AND fecha = ?
            """, (nombre.lower(), fecha))
            
            registros = self.cursor.fetchall()

            if not registros:
                return False, False  # No existe ningún turno para ese día

            # Convertimos los horarios a objetos datetime para comparar
            fmt = "%H:%M"  # Ajustá el formato si usás segundos, ej. %H:%M:%S
            comienzo_nuevo = datetime.strptime(comienzo, fmt)
            fin_nuevo = datetime.strptime(fin, fmt)

            for r in registros:
                comienzo_existente = datetime.strptime(r[0], fmt)
                fin_existente = datetime.strptime(r[1], fmt)

                if comienzo_existente <= comienzo_nuevo and fin_nuevo <= fin_existente:
                    return True, True  # Ya existe y está dentro del horario

            return True, False  # Existe pero no está dentro del horario permitido

        except sqlite3.Error as e:
            logging.error(f"Error al verificar existencia y horario del turno: {e}")
            return False, False


#permite saber el timpo que falta para terminar el turno
    def tiempo_restante_turno(self, nombre, fecha_actual=None, hora_actual=None):
        """
        Calcula el tiempo restante hasta el final del turno actual del operador.
        Retorna una tupla (existe, tiempo_restante_str)
        """

        try:
            if fecha_actual is None:
                fecha_actual = datetime.now().strftime("%Y-%m-%d")
            if hora_actual is None:
                hora_actual = datetime.now().strftime("%H:%M")

            self.cursor.execute("""
                SELECT comienzo, fin FROM OperadorTurno
                WHERE nombre = ? AND fecha = ?
                ORDER BY id DESC LIMIT 1
            """, (nombre, fecha_actual))
            resultado = self.cursor.fetchone()

            if not resultado:
                return False, "❌ No se encontró turno activo."

            comienzo_str, fin_str = resultado

            # Parsear horarios
            hora_fin = datetime.strptime(f"{fecha_actual} {fin_str}", "%Y-%m-%d %H:%M")
            hora_actual_dt = datetime.strptime(f"{fecha_actual} {hora_actual}", "%Y-%m-%d %H:%M")

            if hora_actual_dt >= hora_fin:
                return True, "⏱️ El turno ya finalizó."

            # Calcular diferencia
            tiempo_restante = hora_fin - hora_actual_dt
            horas, resto = divmod(tiempo_restante.total_seconds(), 3600)
            minutos = resto // 60

            return True, f"⏳ Tiempo restante: {int(horas)}h {int(minutos)}min"

        except Exception as e:
            import logging
            logging.error(f"Error al calcular tiempo restante del turno: {e}")
            return False, "⚠️ Error al calcular el tiempo restante."
