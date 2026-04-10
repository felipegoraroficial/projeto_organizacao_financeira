import os
import sqlite3

DB_PATH = "data/finance.db"

os.makedirs("data", exist_ok=True)


def get_connection():
    return sqlite3.connect(DB_PATH)
