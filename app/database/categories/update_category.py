from ..connection import get_connection


def update_category(old_name, new_name, new_tipo):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE categories SET name = ?, tipo = ? WHERE name = ?",
        (new_name, new_tipo, old_name),
    )

    conn.commit()
    conn.close()
