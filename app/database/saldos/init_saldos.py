from ..connection import get_connection


def init_saldos():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS saldos_iniciais (
            ano INTEGER NOT NULL,
            mes INTEGER NOT NULL,
            saldo REAL NOT NULL,
            PRIMARY KEY (ano, mes)
        )
    """
    )

    conn.commit()
    conn.close()
