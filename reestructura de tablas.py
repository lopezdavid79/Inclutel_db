import sqlite3

def poner_operador_id_en_1():
    conn = sqlite3.connect("inclutel.db")
    cursor = conn.cursor()

    # Actualiza todos los registros para que operador_id sea 1
    cursor.execute("""
        UPDATE reclamos
        SET operador_id = 1
    """)

    conn.commit()
    conn.close()
    print("✅ Todos los operador_id en la tabla reclamos ahora son 1.")

poner_operador_id_en_1()
