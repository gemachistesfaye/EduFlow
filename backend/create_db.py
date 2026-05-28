import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent
# Load .env from backend directory first, then fallback to root if necessary
load_dotenv(BASE_DIR / '.env')
load_dotenv(BASE_DIR.parent / '.env')

db_url = os.getenv('DATABASE_URL') or os.getenv('SQLALCHEMY_DATABASE_URI')

if db_url and ("postgres" in db_url or "supabase" in db_url):
    print("Remote PostgreSQL/Supabase database detected.")
    print("No local MySQL database creation needed.")
    print("Tables will be created automatically when you run 'seed_superadmin.py' or start the server.")
else:
    # Fallback to local MySQL database creation
    import pymysql
    host = os.getenv('MYSQL_HOST', '127.0.0.1')
    port = int(os.getenv('MYSQL_PORT', 3306))
    user = os.getenv('MYSQL_USER', 'root')
    password = os.getenv('MYSQL_PASSWORD', '')

    try:
        conn = pymysql.connect(host=host, port=port, user=user, password=password)
        cursor = conn.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS school_management;")
        conn.commit()
        conn.close()
        print("Local MySQL Database ensured.")
    except Exception as e:
        print("Error connecting to or creating local MySQL database:", e)

