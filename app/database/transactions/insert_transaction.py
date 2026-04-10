from ..connection import get_connection


def insert_transaction(
    usuario_id,
    date,
    transaction_type,
    category,
    description,
    value,
    status,
    recorrente,
    parcelas,
):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO transactions (
            usuario_id,
            date,
            type,
            category,
            description,
            value,
            status,
            recorrente,
            parcelas
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            usuario_id,
            date,
            transaction_type,
            category,
            description,
            value,
            status,
            recorrente,
            parcelas,
        ),
    )

    conn.commit()
    conn.close()
