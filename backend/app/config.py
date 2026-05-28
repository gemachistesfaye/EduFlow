# backend/app/config.py
import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parents[2]
# Load .env from backend directory first (override=True ensures .env always wins over system env vars)
_backend_env = Path(__file__).resolve().parents[1] / '.env'
load_dotenv(_backend_env, override=True)
load_dotenv(BASE_DIR / '.env', override=False)  # root fallback only if not already set

class Config:
    # Flask secret
    SECRET_KEY = os.getenv('FLASK_SECRET', 'dev-secret')

    # Database Connection (Supabase/PostgreSQL or MySQL)
    _db_url = os.getenv('DATABASE_URL') or os.getenv('SQLALCHEMY_DATABASE_URI')
    if _db_url:
        # SQLAlchemy requires postgresql:// instead of postgres://
        if _db_url.startswith("postgres://"):
            _db_url = _db_url.replace("postgres://", "postgresql://", 1)
        SQLALCHEMY_DATABASE_URI = _db_url
    else:
        # Fallback to MySQL connection
        MYSQL_USER = os.getenv('MYSQL_USER', 'root')
        MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD', '')
        MYSQL_HOST = os.getenv('MYSQL_HOST', 'localhost')
        MYSQL_PORT = os.getenv('MYSQL_PORT', '3306')
        MYSQL_DB = os.getenv('MYSQL_DB', 'school_management')
        SQLALCHEMY_DATABASE_URI = (
            f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}?charset=utf8mb4"
        )
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_POOL_SIZE = 10
    SQLALCHEMY_MAX_OVERFLOW = 20

    # JWT settings
    JWT_SECRET = os.getenv('JWT_SECRET', 'change-me-please')
    JWT_ALGORITHM = 'HS256'
    JWT_ACCESS_EXPIRES = 3600  # seconds
