import hashlib

from app.database.connection import get_connection


def hash_senha(senha: str) -> str:
    return hashlib.sha256(senha.encode()).hexdigest()


def autenticar_usuario(email: str, senha: str):
    conn = get_connection()
    cursor = conn.cursor()

    senha_hash = hash_senha(senha)

    cursor.execute(
        """
        SELECT id, nome, email FROM usuarios
        WHERE email = ? AND senha_hash = ?
    """,
        (email, senha_hash),
    )

    usuario = cursor.fetchone()
    conn.close()

    if usuario:
        return {"id": usuario[0], "nome": usuario[1], "email": usuario[2]}

    return None
