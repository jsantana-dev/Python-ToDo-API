import sqlite3
from contextlib import contextmanager

DB_PATH = "tasks.db"

CREATE_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    description TEXT,
    status TEXT NOT NULL DEFAULT 'pendente',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""

def init_database():
    """Inicializa o banco de dados criando as tabelas necessárias"""
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.executescript(CREATE_TABLE_SQL)
    conn.commit()
    conn.close()
    print(f"✓ Banco de dados inicializado: {DB_PATH}")

@contextmanager
def get_connection():
    """
    Context manager para conexão com banco de dados.
    Garante que a conexão será fechada após o uso.
    
    Uso:
        with get_connection() as conn:
            cur = conn.cursor()
            cur.execute(...)
    """
    conn = sqlite3.connect(DB_PATH)
    try:
        yield conn
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()