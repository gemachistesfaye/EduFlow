# backend/app/utils/mysql_pool.py
"""MySQL connection pool using mysql-connector-python.
Provides a lightweight wrapper for raw queries where SQLAlchemy is not needed
(e.g., for high‑performance bulk export or stored‑procedure calls).
"""

import mysql.connector
from mysql.connector import pooling
import os
from pathlib import Path

# Load .env values (same as Config) – keep in sync with backend/app/config.py
BASE_DIR = Path(__file__).resolve().parents[3]
# Simple env loader (fallback to os.getenv if .env not present)
if (BASE_DIR / ".env").exists():
    from dotenv import load_dotenv
    load_dotenv(BASE_DIR / ".env")

pool = pooling.MySQLConnectionPool(
    pool_name="xamp_pool",
    pool_size=5,
    host=os.getenv("MYSQL_HOST", "localhost"),
    port=int(os.getenv("MYSQL_PORT", "3306")),
    user=os.getenv("MYSQL_USER", "root"),
    password=os.getenv("MYSQL_PASSWORD", ""),
    database=os.getenv("MYSQL_DB", "school_management"),
    charset="utf8mb4",
    use_unicode=True,
)

def get_connection():
    """Return a pooled MySQLConnection instance.
    Caller is responsible for closing the connection when done.
    """
    return pool.get_connection()

def execute_query(query, params=None, fetch=False):
    """Execute a single query safely.
    - *query*: SQL string with placeholders (%s).
    - *params*: tuple/list of parameters.
    - *fetch*: if True, returns fetched rows as list of dicts.
    """
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute(query, params or ())
        if fetch:
            result = cursor.fetchall()
        else:
            conn.commit()
            result = None
    finally:
        cursor.close()
        conn.close()
    return result
