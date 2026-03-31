from ..connection import get_connection


def insert_category(name, tipo):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT OR IGNORE INTO categories (name, tipo) VALUES (?, ?)", (name, tipo)
    )

    conn.commit()
    conn.close()
