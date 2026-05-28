
# backend/create_superadmin.py
"""
One‑off script that creates the Super‑Admin role and user
in the Supabase/PostgreSQL database used by the EduFlow backend.
Run it once (or whenever you need to reset the admin account):

    python backend/create_superadmin.py
"""

import os
import sys
import bcrypt

# Make the project root importable so we can import the Flask app package
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import create_app
from app.database import db
from app.models import Role, User

# Initialise the Flask app (loads config, DB, etc.)
app = create_app()


def create_superadmin():
    """Create the `superadmin` role (level 100) and a user with that role."""
    with app.app_context():
        # ---------- 1️⃣ Ensure the role exists ----------
        role_name = "superadmin"
        role = Role.query.filter_by(name=role_name).first()
        if not role:
            role = Role(name=role_name, level=100)
            db.session.add(role)
            db.session.commit()
            print(f"✅ Role '{role_name}' created (id={role.id}).")
        else:
            print(f"ℹ️ Role '{role_name}' already exists (id={role.id}).")

        # ---------- 2️⃣ Ensure the Super‑Admin user exists ----------
        email = "superadmin@school.com"
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            print(f"⚠️ Super‑Admin user already exists (id={existing_user.id}).")
            return

        # Create a bcrypt hash for the password
        raw_password = "StrongPass!23"
        salt = bcrypt.gensalt()
        pwd_hash = bcrypt.hashpw(raw_password.encode("utf-8"), salt).decode("utf-8")

        # Insert the new user
        super_user = User(
            email=email,
            password_hash=pwd_hash,
            role_id=role.id,
            must_change_password=False,   # set True if you want a forced password change on first login
        )
        db.session.add(super_user)
        db.session.commit()
        print(f"✅ Super‑Admin user created (id={super_user.id}).")


if __name__ == "__main__":
    create_superadmin()