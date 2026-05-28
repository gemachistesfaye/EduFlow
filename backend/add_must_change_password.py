# backend/add_must_change_password.py
"""
Idempotent script that adds the `must_change_password` column to the
`users` table on the Supabase database (or any PostgreSQL DB).
"""
import os
import sys

# Make the project root importable
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import create_app
from app.database import db
from sqlalchemy import text

app = create_app()

def add_column():
    with app.app_context():
        # PostgreSQL‑specific “add column if not exists” guard
        sql = text(
            """
            DO $$
            BEGIN
                IF NOT EXISTS (
                    SELECT 1
                    FROM information_schema.columns
                    WHERE table_name = 'users'
                      AND column_name = 'must_change_password'
                ) THEN
                    ALTER TABLE users
                        ADD COLUMN must_change_password BOOLEAN NOT NULL DEFAULT TRUE;
                END IF;
            END $$;
            """
        )
        try:
            db.session.execute(sql)
            db.session.commit()
            print("✅ Column `must_change_password` is now present (or already existed).")
        except Exception as exc:
            db.session.rollback()
            print("❌ Failed to add column:", exc)

if __name__ == "__main__":
    add_column()
