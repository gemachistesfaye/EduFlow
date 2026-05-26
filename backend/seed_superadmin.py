import os
import sys

# Ensure backend package can be imported
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.app.database import db, init_db
from backend.app.models import Role, User
from backend.app.utils.security import hash_password
from backend.app import create_app

app = create_app()

def main():
    with app.app_context():

        try:
            # 1. Ensure the Super-Admin role exists
            super_role = db.session.query(Role).filter_by(name="superadmin").first()
            if not super_role:
                super_role = Role(name="superadmin", level=100)
                db.session.add(super_role)
                db.session.commit()
                print("Created superadmin role")
            else:
                print("Superadmin role already exists")

            # 2. Create the Super-Admin user
            email = "superadmin@school.com"
            plain_pwd = "StrongPass!23"
            pwd_hash = hash_password(plain_pwd)

            existing = db.session.query(User).filter_by(email=email).first()
            if existing:
                print(f"User {email} already exists")
            else:
                user = User(email=email, password_hash=pwd_hash, role_id=super_role.id)
                db.session.add(user)
                db.session.commit()
                print(f"Super-Admin user {email} created with password: {plain_pwd}")
                
        except Exception as e:
            print(f"An error occurred: {e}")
            db.session.rollback()

if __name__ == "__main__":
    main()
