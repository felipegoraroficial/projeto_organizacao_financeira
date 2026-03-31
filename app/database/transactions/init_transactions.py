from ..connection import get_connection

def init_transactions():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            type TEXT NOT NULL,
            category TEXT NOT NULL,
            description TEXT,
            value REAL NOT NULL,
            status TEXT DEFAULT 'pago',
            recorrente INTEGER DEFAULT 0,
            parcelas INTEGER DEFAULT 1,
            data_pagamento TEXT
        )
    """)

    conn.commit()
    conn.close()