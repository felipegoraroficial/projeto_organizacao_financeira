from app.database.connection import get_connection


def update_transaction(
    transaction_id,
    data,
    categoria,
    descricao,
    valor,
    status,
    recorrente,
    parcelas,
    data_pagamento,
):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE transactions
        SET
            date = ?,
            category = ?,
            description = ?,
            value = ?,
            status = ?,
            recorrente = ?,
            parcelas = ?,
            data_pagamento = ?
        WHERE id = ?
        """,
        (
            data,
            categoria,
            descricao,
            valor,
            status,
            recorrente,
            parcelas,
            data_pagamento,
            transaction_id,
        ),
    )

    conn.commit()
    conn.close()
