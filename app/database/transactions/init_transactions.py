from ..connection import get_connection


def init_transactions():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario_id INTEGER NOT NULL,
            data TEXT NOT NULL,
            tipo TEXT NOT NULL,
            categoria TEXT NOT NULL,
            descricao TEXT,
            valor REAL NOT NULL,
            status TEXT NOT NULL,
            recorrente TEXT,
            parcelas INTEGER,
            data_pagamento TEXT,
            FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
        )
    """
    )

    conn.commit()
    conn.close()
