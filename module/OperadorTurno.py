from datetime import datetime
import sqlite3
import logging
import os
import sys

# Configuración del logging
logging.basicConfig(filename='mi_programa.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')



class OperadorTurno:
    def __init__(self, fecha,comienzo, fin,operador_id):
        self.operador_id= operador_id
        self.fecha = datetime.now().date()
        self.comienzo = comienzo  # str, ej: "08:00"
        self.fin = fin            # str, ej: "16:00"

    def __str__(self):
        return (f"Operador: {self.operador_id}\n"
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
        """Crea la tabla operadorTurnosi no existe."""
        try:
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS operadorTurno(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre TEXT NOT NULL,
                    fecha TEXT NOT NULL,
                    comienzo TIME NOT NULL,
                    fin TIME NOT NULL
                )
            """)
            self.conexion.commit()
            logging.info("Tabla operadorTurnoverificada/creada.")
        except sqlite3.Error as e:
            logging.error(f"Error al crear la tabla OperadorTurno: {e}")

    def cerrar_conexion(self):
        if self.conexion:
            self.conexion.close()
            logging.info("Conexión cerrada.")



    def desconectar(self):
        if self.conexion:
            self.conexion.close()
            logging.info("Conexión cerrada.")


    def registrar_operador(self, operador: OperadorTurno):
        try:
            # 1. Verificar si el operador_id existe en la tabla 'operador'
            self.cursor.execute("SELECT id FROM operador WHERE id = ?", (operador.operador_id,))
            operador_existe = self.cursor.fetchone()

            if not operador_existe:
                error_message = f"Error al registrar Turno de operador: El operador con ID '{operador.operador_id}' no existe en la tabla 'operador'. Violación de clave foránea."
                logging.error(error_message)
                return False  # Indica que el registro falló debido a la clave foránea

            # 2. Si el operador existe, intentar la inserción del turno
            self.cursor.execute(
                "INSERT INTO operadorTurno(fecha, comienzo, fin, operador_id) VALUES (?, ?, ?, ?)",
                (operador.fecha, operador.comienzo, operador.fin,operador.operador_id)
            )
            self.conexion.commit()
            logging.info(f"Turno para operador con ID '{operador.operador_id}' registrado correctamente.")
            return True

        except sqlite3.IntegrityError as e:
            # Capturar errores de integridad (podría ser otra clave única, aunque menos probable aquí)
            logging.error(f"Error de integridad al registrar Turno de operador: {e}")
            self.conexion.rollback()
            return False

        except sqlite3.Error as e:
            # Capturar otros errores de SQLite
            logging.error(f"Error general al registrar Turno de operador: {e}")
            self.conexion.rollback()
            return False
    def obtener_todos(self):
        try:
            self.cursor.execute("SELECT id,  comienzo, fin, operador_id FROM operadorTurno")
            operadores = {
                str(row[0]): {"comienzo": row[1], "fin": row[2], "operador_id": row[3]}
                for row in self.cursor.fetchall()
            }

            print("📋 Lista de operadores:")
            for id_op, datos in operadores.items():
                print(f"  ID: {id_op}")
                
                print(f"  Comienzo: {datos['comienzo']}")
                print(f"  Fin: {datos['fin']}")
                print(f"  Operador: {datos['operador_id']}")
                print("-" * 20)

            return operadores
        except sqlite3.Error as e:
            logging.error(f"Error al obtener operadores: {e}")
            return {}

    def editar_operador(self, id_op, nombre, comienzo, fin):
        try:
            self.cursor.execute("""
                UPDATE operadorTurnoSET nombre = ?, comienzo = ?, fin = ?
                WHERE id = ?
            """, (nombre, comienzo, fin, id_op))
            self.conexion.commit()
            logging.info(f"Operador {id_op} actualizado.")
        except sqlite3.Error as e:
            logging.error(f"Error al editar operador: {e}")

    def eliminar_operador(self, id_op):
        try:
            self.cursor.execute("DELETE FROM operadorTurnoWHERE id = ?", (id_op,))
            self.conexion.commit()
            logging.info(f"Operador {id_op} eliminado.")
        except sqlite3.Error as e:
            logging.error(f"Error al eliminar operador: {e}")

    def buscar_operador(self, id_op):
        try:
            self.cursor.execute("SELECT id, comienzo, fin,operador_id FROM operadorTurnoWHERE id = ?", (id_op,))
            resultado = self.cursor.fetchone()

            if resultado:
                return {
                    "id": resultado[0],
                    "comienzo": resultado[1],
                    "fin": resultado[2],
                    "operador_id": resultado[3]
                }
            else:
                return None
        except sqlite3.Error as e:
            logging.error(f"Error al buscar operador: {e}")
            return None

    def obtener_por_nombre(self, nombre):
        try:
            self.cursor.execute("SELECT id, nombre, comienzo, fin FROM operadorTurnoWHERE LOWER(nombre) = LOWER(?)", (nombre,))
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
            self.cursor.execute("SELECT id, nombre, comienzo, fin FROM operadorTurnoWHERE LOWER(nombre) LIKE ?", ('%' + parcial.lower() + '%',))
            resultados = self.cursor.fetchall()
            encontrados = [{"id": r[0], "nombre": r[1], "comienzo": r[2], "fin": r[3]} for r in resultados]

            print("🔍 Operadores encontrados:")
            for op in encontrados:
                print(f"  ID: {op['id']} - Nombre: {op['nombre']} - Turno: {op['comienzo']} a {op['fin']}")

            return encontrados
        except sqlite3.Error as e:
            logging.error(f"Error al buscar operadores por nombre parcial: {e}")
            return []


    def existe_turno(self, fecha, comienzo, fin, operador_id):

        try:
            self.cursor.execute("""
                SELECT 1 FROM operadorTurno
                WHERE LOWER(operador_id) = ? AND fecha = ? AND comienzo = ? AND fin = ?
            """, (operador_id.lower(), fecha, comienzo, fin))

            resultado = self.cursor.fetchone()
            existe = resultado is not None

            if existe:
                print(f"⚠️ Ya existe un turno registrado para: {operador_id} - {fecha} ({comienzo} a {fin})")
            else:
                print(f"✅ Turno disponible para: {operador_id} - {fecha} ({comienzo} a {fin})")

            return existe

        except sqlite3.Error as e:
            logging.error(f"Error al verificar existencia del turno: {e}")
            return False





    def existe_y_esta_dentro_del_horario(self, fecha, comienzo, fin, operador_id):
        try:
            self.cursor.execute("""
                SELECT comienzo, fin FROM operadorTurno
                WHERE operador_id = ? AND fecha = ?
            """, (operador_id, fecha))
            
            registros = self.cursor.fetchall()

            if not registros:
                return False, False  # No hay ningún turno en esa fecha para ese operador

            fmt = "%H:%M"
            comienzo_nuevo = datetime.strptime(comienzo, fmt)
            fin_nuevo = datetime.strptime(fin, fmt)

            for r in registros:
                comienzo_existente = datetime.strptime(r[0], fmt)
                fin_existente = datetime.strptime(r[1], fmt)

                # Detectar superposición de horarios
                if comienzo_nuevo < fin_existente and comienzo_existente < fin_nuevo:
                    return True, True  # Ya existe y se superpone

            return True, False  # Existe pero no se superpone

        except sqlite3.Error as e:
            logging.error(f"Error al verificar existencia y horario del turno: {e}")
            return False, False

#permite saber el timpo que falta para terminar el turno
    def tiempo_restante_turno(self, operador_id, fecha_actual=None, hora_actual=None):
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
                WHERE operador_id = ? AND fecha = ?
                ORDER BY id DESC LIMIT 1
            """, (operador_id, fecha_actual))
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


    def obtener_nombre_operador(self, operador_id):
        """
        Obtiene el nombre del operador desde la tabla 'operador' dado su ID.

        Args:
            operador_id (int): El ID del operador en la tabla 'operador'.

        Returns:
            str: El nombre del operador si se encuentra, o None si no se encuentra.
        """
        try:
            self.cursor.execute("SELECT nombre FROM operador WHERE id = ?", (operador_id,))
            resultado = self.cursor.fetchone()
            if resultado:
                return resultado[0]
            else:
                return None
        except sqlite3.Error as e:
            logging.error(f"Error al obtener nombre del operador: {e}")
            return None


    def obtener_nombres_operadores(self):
        """
        Obtiene nombres de operadores desde la tabla 'operador'.

        Returns:
            list: Una lista con los nombres de todos los operadores,
                  o una lista vacía en caso de error.
        """
        nombres_operadores = []
        try:
            self.cursor.execute("SELECT nombre FROM operador ORDER BY nombre")
            resultados = self.cursor.fetchall()
            for resultado in resultados:
                nombres_operadores.append(resultado[0])
            return nombres_operadores
        except sqlite3.Error as e:
            logging.error(f"Error al obtener nombres de operadores: {e}")
            return []


    def obtener_operador_activo(self):
        """
        Obtiene el id_operador del operador que está activo en este momento.

        Returns:
            int: El id_operador del operador activo, o None si no hay ninguno.
        """
        now = datetime.now()
        fecha_actual = now.strftime("%Y-%m-%d")
        hora_actual = now.strftime("%H:%M")
        try:
        #    self._conectar()
            self.cursor.execute("""
                SELECT operador_id
                FROM OperadorTurno
                WHERE fecha = ?
                  AND time(hora_comienzo) <= time(?)
                  AND time(hora_fin) >= time(?)
            """, (fecha_actual, hora_actual, hora_actual))
            resultado = self.cursor.fetchone()
            if resultado:
                return resultado[0]
            else:
                return None
        except sqlite3.Error as e:
            logging.error(f"Error al obtener el operador activo: {e}")
            return None
            

    def obtener_operador_id(self, nombre):
        """
        Obtiene el id del operador desde la tabla 'operador' dado su nombre.

        Args:
            nombre (str): El nombre del operador a buscar.

        Returns:
            int: El ID del operador si se encuentra, o None si no se encuentra.
        """
        try:
            #self.conectar()
            self.cursor.execute("SELECT id FROM operador WHERE nombre = ?", (nombre,))
            resultado = self.cursor.fetchone()
            if resultado:
                return resultado[0]
            else:
                        return None
        except sqlite3.Error as e:
            logging.error(f"Error al obtener ID del operador con nombre '{nombre}': {e}")
            return None
        