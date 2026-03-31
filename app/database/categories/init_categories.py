from ..connection import get_connection

def init_categories():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            tipo TEXT NOT NULL
        )
    """)

    cursor.execute("SELECT COUNT(*) FROM categories")
    if cursor.fetchone()[0] == 0:
        default_categories = [
            ("Salário", "Receita"),
            ("Rendimentos", "Receita"),
            ("Alimentação", "Despesa"),
            ("Moradia", "Despesa"),
            ("Transporte", "Despesa"),
            ("Lazer", "Despesa"),
            ("Saúde", "Despesa"),
            ("Educação", "Despesa"),
            ("Outros", "Despesa"),
        ]

        cursor.executemany(
            "INSERT INTO categories (name, tipo) VALUES (?, ?)",
            default_categories
        )

    conn.commit()
    conn.close()