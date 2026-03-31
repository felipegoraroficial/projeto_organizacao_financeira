from ..connection import get_connection

def insert_transaction(date, transaction_type, category, description, value, status, recorrente, parcelas):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO transactions (date, type, category, description, value, status, recorrente, parcelas)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (date, transaction_type, category, description, value, status, recorrente, parcelas))

    conn.commit()
    conn.close()