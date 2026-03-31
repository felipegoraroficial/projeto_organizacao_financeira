from ..connection import get_connection

def set_saldo_inicial(ano, mes, saldo):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT OR REPLACE INTO saldos_iniciais (ano, mes, saldo)
        VALUES (?, ?, ?)
    """, (ano, mes, saldo))

    conn.commit()
    conn.close()