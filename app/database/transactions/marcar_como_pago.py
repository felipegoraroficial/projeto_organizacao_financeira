from ..connection import get_connection


def marcar_como_pago(transaction_id, data_pagamento):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE transactions
        SET status = 'pago',
            data_pagamento = ?
        WHERE id = ?
    """,
        (data_pagamento, transaction_id),
    )

    conn.commit()
    conn.close()
