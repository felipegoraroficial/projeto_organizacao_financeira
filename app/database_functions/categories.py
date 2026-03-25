from .connection import get_connection

def init_categories():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL
        )
    """)

    cursor.execute("SELECT COUNT(*) FROM categories")
    if cursor.fetchone()[0] == 0:
        default_categories = [
            "Salário", "Investimentos", "Alimentação", "Moradia",
            "Transporte", "Lazer", "Saúde", "Educação", "Outros"
        ]
        cursor.executemany(
            "INSERT INTO categories (name) VALUES (?)",
            [(c,) for c in default_categories]
        )

    conn.commit()
    conn.close()


def load_categories():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT name FROM categories ORDER BY name ASC")
    rows = [row[0] for row in cursor.fetchall()]

    conn.close()
    return rows


def insert_category(name):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("INSERT OR IGNORE INTO categories (name) VALUES (?)", (name,))

    conn.commit()
    conn.close()


def update_category(old_name, new_name):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("UPDATE categories SET name = ? WHERE name = ?", (new_name, old_name))

    conn.commit()
    conn.close()


def delete_category(name):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM categories WHERE name = ?", (name,))

    conn.commit()
    conn.close()