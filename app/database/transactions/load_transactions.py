from ..connection import get_connection


def load_transactions(usuario_id: int):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            id,
            date,
            type,
            category,
            description,
            value,
            status,
            recorrente,
            parcelas,
            data_pagamento
        FROM transactions
        WHERE usuario_id = ?
        ORDER BY date DESC
        """,
        (usuario_id,),
    )

    rows = cursor.fetchall()
    conn.close()
    return rows
