import pymysql
import os
from dotenv import load_dotenv

load_dotenv('e:/GitHub Repo/school-management-system/backend/.env')

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
    print("Database ensured.")
except Exception as e:
    print("Error creating database:", e)
