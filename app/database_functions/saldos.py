from .connection import get_connection

def init_saldos():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS saldos_iniciais (
            ano INTEGER NOT NULL,
            mes INTEGER NOT NULL,
            saldo REAL NOT NULL,
            PRIMARY KEY (ano, mes)
        )
    """)

    conn.commit()
    conn.close()


def set_saldo_inicial(ano, mes, saldo):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT OR REPLACE INTO saldos_iniciais (ano, mes, saldo)
        VALUES (?, ?, ?)
    """, (ano, mes, saldo))

    conn.commit()
    conn.close()


def get_saldo_inicial(ano, mes):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT saldo FROM saldos_iniciais
        WHERE ano = ? AND mes = ?
    """, (ano, mes))

    row = cursor.fetchone()
    conn.close()

    return row[0] if row else 0.0