# backend/scripts/seed_courses_with_languages.py
"""
Seed script:
- Creates a super‑admin (if not present) – name/email/password unchanged.
- Creates the main school "Main Campus".
- Adds the 10 core courses (Mathematics … Art & Design).
- Adds language courses (Amharic, Afaan Oromo) for grades 9‑12.
  * For grades 9‑10 the language courses are mandatory (the script creates them automatically).
  * For grades 11‑12 the same language courses exist so students can choose one of them.
Run with:
    python backend/scripts/seed_courses_with_languages.py
"""

import os
import sys

# Ensure the repo root is in PYTHONPATH
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.append(BASE_DIR)

from app import create_app
from app.models import db, Role, User, School, Course, Teacher
from app.utils.security import hash_password


def get_or_create_role(name: str, level: int):
    role = Role.query.filter_by(name=name).first()
    if not role:
        role = Role(name=name, level=level)
        db.session.add(role)
        db.session.flush()
        print(f"✔ Created role '{name}' (level={level})")
    else:
        print(f"ℹ Role '{name}' already exists")
    return role


def get_or_create_school(name: str, location: str = "Headquarters"):
    school = School.query.filter_by(name=name).first()
    if not school:
        school = School(name=name, location=location)
        db.session.add(school)
        db.session.flush()
        print(f"✔ Created school '{name}'")
    else:
        print(f"ℹ School '{name}' already exists")
    return school


def get_or_create_teacher(email: str, name: str, subject: str = "General"):
    teacher = Teacher.query.filter_by(email=email).first()
    if not teacher:
        teacher = Teacher(name=name, subject=subject, email=email)
        db.session.add(teacher)
        db.session.flush()
        print(f"✔ Created placeholder teacher '{name}' ({email})")
    return teacher


def create_superadmin():
    superadmin_role = get_or_create_role("superadmin", level=80)
    superadmin_email = "superadmin@school.com"
    admin_user = User.query.filter_by(email=superadmin_email).first()
    if not admin_user:
        temp_pwd = "superadmin123"
        admin_user = User(
            email=superadmin_email,
            password_hash=hash_password(temp_pwd),
            role_id=superadmin_role.id,
            must_change_password=True,
            school_id=None,
        )
        db.session.add(admin_user)
        db.session.flush()
        print("✔ Created super‑admin user (temporary password: superadmin123)")
    else:
        print("ℹ Super‑admin user already exists")


def create_core_courses(school):
    # Core courses with stream distinction
    core_courses = [
        # Mathematics split by stream
        ("Mathematics (Natural)", "C101N", "natural"),
        ("Mathematics (Social)", "C101S", "social"),
        ("English Language", "C102", None),
        ("Physics", "C103", "natural"),
        ("Chemistry", "C104", "natural"),
        ("Biology", "C105", "natural"),
        ("History", "C106", "social"),
        ("Geography", "C107", "social"),
        ("Computer Science", "C108", None),
        ("Physical Education", "C109", None),
        ("Civics", "C110", None),
    ]

    # Remove any legacy courses that should no longer exist
    for legacy_code in ["C109", "C110"]:
        legacy_course = Course.query.filter_by(code=legacy_code).first()
        if legacy_course:
            db.session.delete(legacy_course)
            print(f"🗑️ Deleted legacy course with code {legacy_code}")

    for name, code, stream in core_courses:
        if not Course.query.filter_by(code=code).first():
            teacher = get_or_create_teacher(
                email=f"teacher_{code.lower()}@school.com",
                name=f"Teacher {code}",
                subject="General",
            )
            course = Course(name=name, code=code, school_id=school.id,
                            teacher_id=teacher.id, stream=stream)
            db.session.add(course)
            print(f"✔ Created course '{name}' ({code}) stream={stream}")
        else:
            print(f"ℹ Course '{name}' ({code}) already exists")


def create_language_courses(school):
    languages = ["Amharic", "Afaan Oromo"]
    grades = [9, 10, 11, 12]
    for grade in grades:
        for lang in languages:
            name = f"{lang} (Grade {grade})"
            code = f"L{grade}{lang.replace(' ', '')[:2].upper()}"  # e.g., L9AM, L9AF
            if not Course.query.filter_by(code=code).first():
                teacher = get_or_create_teacher(
                    email=f"{lang.replace(' ', '').lower()}_g{grade}@school.com",
                    name=f"{lang} Teacher G{grade}",
                    subject=lang,
                )
                course = Course(name=name, code=code, school_id=school.id, teacher_id=teacher.id)
                db.session.add(course)
                print(f"✔ Created language course '{name}' ({code})")
            else:
                print(f"ℹ Language course '{name}' ({code}) already exists")


def main():
    app = create_app()
    with app.app_context():
        # 1. Super‑admin (unchanged)
        create_superadmin()
        # 2. Main Campus school
        main_school = get_or_create_school("Main Campus")
        # 3. Core academic courses
        create_core_courses(main_school)
        # 4. Language courses for grades 9‑12
        create_language_courses(main_school)
        # Commit all changes
        db.session.commit()
        print("\n✅ Seeding complete – super‑admin, 10 core courses, and language courses added.")

if __name__ == "__main__":
    main()
