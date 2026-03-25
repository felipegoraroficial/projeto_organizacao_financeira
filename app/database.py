import sqlite3
import os

DB_PATH = "data/finance.db"

# Garante que a pasta data/ existe
os.makedirs("data", exist_ok=True)

# -----------------------------
#   TABELAS
# -----------------------------
def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Tabela de transações
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

    # Tabela de categorias
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL
        )
    """)

    # Inserir categorias padrão se a tabela estiver vazia
    cursor.execute("SELECT COUNT(*) FROM categories")
    if cursor.fetchone()[0] == 0:
        default_categories = [
            "Salário", "Investimentos", "Alimentação", "Moradia",
            "Transporte", "Lazer", "Saúde", "Educação", "Outros"
        ]
        cursor.executemany("INSERT INTO categories (name) VALUES (?)",
                           [(c,) for c in default_categories])

    conn.commit()
    conn.close()


# -----------------------------
#   SALDOS INICIAIS
# -----------------------------
def init_saldos():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS saldos_iniciais (
            ano INTEGER NOT NULL,
            mes INTEGER NOT NULL,
            saldo REAL NOT NULL,
            PRIMARY KEY (ano, mes)
        )
    """)

    conn.commit()
    conn.close()


def set_saldo_inicial(ano, mes, saldo):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT OR REPLACE INTO saldos_iniciais (ano, mes, saldo)
        VALUES (?, ?, ?)
    """, (ano, mes, saldo))

    conn.commit()
    conn.close()


def get_saldo_inicial(ano, mes):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT saldo FROM saldos_iniciais
        WHERE ano = ? AND mes = ?
    """, (ano, mes))

    row = cursor.fetchone()
    conn.close()

    return row[0] if row else 0.0


# -----------------------------
#   TRANSAÇÕES
# -----------------------------
def insert_transaction(date, type, category, description, value, status, recorrente, parcelas):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO transactions (date, type, category, description, value, status, recorrente, parcelas)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (date, type, category, description, value, status, recorrente, parcelas))

    conn.commit()
    conn.close()


def load_transactions():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM transactions ORDER BY date DESC")
    rows = cursor.fetchall()

    conn.close()
    return rows


def delete_transaction(id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("DELETE FROM transactions WHERE id = ?", (id,))

    conn.commit()
    conn.close()


# -----------------------------
#   CATEGORIAS
# -----------------------------
def load_categories():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT name FROM categories ORDER BY name ASC")
    rows = [row[0] for row in cursor.fetchall()]

    conn.close()
    return rows


def insert_category(name):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("INSERT OR IGNORE INTO categories (name) VALUES (?)", (name,))

    conn.commit()
    conn.close()


def update_category(old_name, new_name):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("UPDATE categories SET name = ? WHERE name = ?", (new_name, old_name))

    conn.commit()
    conn.close()


def delete_category(name):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("DELETE FROM categories WHERE name = ?", (name,))

    conn.commit()
    conn.close()