from ..connection import get_connection


def get_saldo_inicial(ano, mes):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT saldo FROM saldos_iniciais
        WHERE ano = ? AND mes = ?
    """,
        (ano, mes),
    )

    row = cursor.fetchone()
    conn.close()

    return row[0] if row else 0.0
