from ..connection import get_connection


def delete_category(name):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM categories WHERE name = ?", (name,))

    conn.commit()
    conn.close()
