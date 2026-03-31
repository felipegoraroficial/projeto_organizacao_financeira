from ..connection import get_connection

def load_categories():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT name, tipo FROM categories ORDER BY name ASC")
    rows = cursor.fetchall()

    conn.close()
    return rows
