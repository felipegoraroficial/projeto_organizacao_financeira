from .connection import get_connection


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
            parcelas INTEGER DEFAULT 1
        )
    """)

    conn.commit()
    conn.close()


def insert_transaction(date, transaction_type, category, description, value, status, recorrente, parcelas):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO transactions (date, type, category, description, value, status, recorrente, parcelas)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (date, transaction_type, category, description, value, status, recorrente, parcelas))

    conn.commit()
    conn.close()


def load_transactions():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM transactions ORDER BY date DESC")
    rows = cursor.fetchall()

    conn.close()
    return rows


def delete_transaction(transaction_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM transactions WHERE id = ?", (transaction_id,))

    conn.commit()
    conn.close()