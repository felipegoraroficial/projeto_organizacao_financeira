import hashlib
import sqlite3

from app.database.connection import get_connection


def hash_senha(senha: str) -> str:
    return hashlib.sha256(senha.encode()).hexdigest()


def cadastrar_usuario(nome: str, email: str, senha: str):
    conn = get_connection()
    cursor = conn.cursor()

    senha_hash = hash_senha(senha)

    try:
        cursor.execute(
            """
            INSERT INTO usuarios (nome, email, senha_hash)
            VALUES (?, ?, ?)
        """,
            (nome, email, senha_hash),
        )

        conn.commit()
        return True

    except sqlite3.IntegrityError:
        return False  # email já existe

    finally:
        conn.close()
