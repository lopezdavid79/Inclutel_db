import sqlite3

# Ruta a tu archivo de base de datos
ruta_db = "Inclutel.db"  # Cambiala si usás otra

try:
    # Conexión a la base de datos
    conexion = sqlite3.connect(ruta_db)
    cursor = conexion.cursor()

    # Eliminar la tabla si existe
    cursor.execute("DROP TABLE IF EXISTS OperadorTurno")
    conexion.commit()

    print("✅ Tabla 'OperadorTurno' eliminada exitosamente.")

except sqlite3.Error as error:
    print(f"❌ Error al eliminar la tabla: {error}")

finally:
    if conexion:
        conexion.close()
