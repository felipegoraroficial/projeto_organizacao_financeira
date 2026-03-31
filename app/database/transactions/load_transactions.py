from ..connection import get_connection


def load_transactions():
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
        ORDER BY date DESC
    """
    )

    rows = cursor.fetchall()
    conn.close()
    return rows
