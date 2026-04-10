import hashlib
import sqlite3


def hash_senha(senha: str) -> str:
    return hashlib.sha256(senha.encode()).hexdigest()


def atualizar_senha(email: str, nova_senha: str):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    senha_hash = hash_senha(nova_senha)

    cursor.execute(
        """
        UPDATE usuarios
        SET senha_hash = ?
        WHERE email = ?
    """,
        (senha_hash, email),
    )

    conn.commit()
    conn.close()

    return cursor.rowcount > 0
