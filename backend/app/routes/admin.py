from flask import Blueprint, jsonify, request
from ..middleware.auth import rbac
from ..models import db, Student, Teacher, Profile, Role, School, Class, User
from ..utils.security import hash_password
import pandas as pd
import time
bp = Blueprint('admin', __name__)

@bp.post('/bulk-import/teachers')
@rbac(80)
def bulk_import_teachers():
    """Upload an Excel/CSV containing teacher rows.
    Expected columns: email, full_name, subject, school_name
    Generates a temporary password: <lowercase_firstname>123
    """
    file = request.files.get('excel')
    if not file:
        return jsonify(error='No file provided'), 400
    try:
        df = pd.read_excel(file)
    except Exception as e:
        return jsonify(error='Failed to read file'), 400

    created = 0
    errors = []
    for idx, row in df.iterrows():
        try:
            # Basic validation
            email = str(row.get('email')).strip()
            name = str(row.get('full_name')).strip()
            subject = str(row.get('subject')).strip()
            school_name = str(row.get('school_name')).strip()
            if not email or not name or not subject:
                raise ValueError('Missing required fields')

            # Get or create school
            school = School.query.filter_by(name=school_name).first()
            if not school:
                school = School(name=school_name, location='')
                db.session.add(school)
                db.session.flush()

            # Role
            teacher_role = Role.query.filter_by(name='teacher').first()
            if not teacher_role:
                teacher_role = Role(name='teacher', level=30)
                db.session.add(teacher_role)
                db.session.flush()

            # Temporary password based on first name
            first_name = name.split()[0].lower()
            temp_password = f"{first_name}123"
            pwd_hash = hash_password(temp_password)

            # User
            user = User(email=email, password_hash=pwd_hash,
                        role_id=teacher_role.id, school_id=school.id,
                        must_change_password=True)
            db.session.add(user)
            db.session.flush()

            # Profile
            profile = Profile(user_id=user.id, full_name=name, school_id=school.id)
            db.session.add(profile)

            # Teacher record
            teacher = Teacher(name=name, subject=subject, email=email, school_id=school.id)
            db.session.add(teacher)
            created += 1
        except Exception as e:
            errors.append(f"Row {idx+2}: {str(e)}")
    db.session.commit()
    return jsonify(created_teachers=created, errors=errors), 200

@bp.post('/bulk-import/students')
@rbac(80)
def bulk_import_students():
    """Upload an Excel/CSV containing student rows with parent info.
    Expected columns: email, full_name, gender, date_of_birth, class_name, school_name,
                      parent_name, parent_email
    Temporary password: <lowercase_firstname>123
    """
    file = request.files.get('excel')
    if not file:
        return jsonify(error='No file provided'), 400
    try:
        df = pd.read_excel(file)
    except Exception as e:
        return jsonify(error='Failed to read file'), 400

    created_students = 0
    created_parents = 0
    errors = []
    for idx, row in df.iterrows():
        try:
            email = str(row.get('email')).strip()
            name = str(row.get('full_name')).strip()
            gender = str(row.get('gender')).strip()
            dob = row.get('date_of_birth')
            class_name = str(row.get('class_name')).strip()
            school_name = str(row.get('school_name')).strip()
            parent_name = str(row.get('parent_name')).strip()
            parent_email = str(row.get('parent_email')).strip()
            if not all([email, name, gender, dob, class_name, school_name, parent_name, parent_email]):
                raise ValueError('Missing required fields')

            # School
            school = School.query.filter_by(name=school_name).first()
            if not school:
                school = School(name=school_name, location='')
                db.session.add(school)
                db.session.flush()

            # Ensure student role
            student_role = Role.query.filter_by(name='student').first()
            if not student_role:
                student_role = Role(name='student', level=10)
                db.session.add(student_role)
                db.session.flush()

            # Ensure parent role
            parent_role = Role.query.filter_by(name='parent').first()
            if not parent_role:
                parent_role = Role(name='parent', level=10)
                db.session.add(parent_role)
                db.session.flush()

            # Create (or fetch) parent user
            parent_user = User.query.filter_by(email=parent_email).first()
            if not parent_user:
                first_parent = parent_name.split()[0].lower()
                parent_pwd = f"{first_parent}123"
                parent_user = User(email=parent_email,
                                   password_hash=hash_password(parent_pwd),
                                   role_id=parent_role.id,
                                   school_id=school.id,
                                   must_change_password=True)
                db.session.add(parent_user)
                db.session.flush()
                parent_profile = Profile(user_id=parent_user.id,
                                         full_name=parent_name,
                                         school_id=school.id)
                db.session.add(parent_profile)
                db.session.flush()
                created_parents += 1
            else:
                parent_profile = Profile.query.filter_by(user_id=parent_user.id).first()
                if not parent_profile:
                    parent_profile = Profile(user_id=parent_user.id,
                                             full_name=parent_name,
                                             school_id=school.id)
                    db.session.add(parent_profile)
                    db.session.flush()

            # Temporary password for student
            first_student = name.split()[0].lower()
            student_pwd = f"{first_student}123"
            student_user = User(email=email,
                                password_hash=hash_password(student_pwd),
                                role_id=student_role.id,
                                school_id=school.id,
                                must_change_password=True)
            db.session.add(student_user)
            db.session.flush()

            # Profile for student
            student_profile = Profile(user_id=student_user.id,
                                      full_name=name,
                                      school_id=school.id,
                                      parent_id=parent_profile.id)
            db.session.add(student_profile)
            db.session.flush()

            # Class handling
            cls = Class.query.filter_by(class_name=class_name, school_id=school.id).first()
            if not cls:
                cls = Class(class_name=class_name, section='A', academic_year='2023/2024')
                db.session.add(cls)
                db.session.flush()

            # Student record
            student_id = f"STU{int(time.time())}{idx}"
            student = Student(student_id=student_id,
                              name=name,
                              gender=gender,
                              date_of_birth=dob,
                              class_id=cls.id,
                              school_id=school.id,
                              parent_id=parent_profile.id,
                              user_id=student_user.id)
            db.session.add(student)
            created_students += 1
        except Exception as e:
            errors.append(f"Row {idx+2}: {str(e)}")
    db.session.commit()
    return jsonify(created_students=created_students,
                   created_parents=created_parents,
                   errors=errors), 200

@bp.get('/dashboard')
@rbac(80)
def dashboard():
    return jsonify({"message": "Admin dashboard"})

@bp.get('/school-metrics')
@rbac(80)
def school_metrics():
    # Placeholder data for Admin dashboard
    return jsonify({
        "students": 450,
        "teachers": 32,
        "fees_collected": "12,400.00"
    })

@bp.post('/cascade-register')
@rbac(80)
def cascade_register():
    """Create a parent profile and a student linked to that parent.
    Expected payload (mirrors frontend):
    {
        "student": {"email": "..., "name": "..."},
        "parent": {"email": "..., "name": "..."}
    }
    """
    data = request.json
    if not data or 'student' not in data or 'parent' not in data:
        return jsonify({"error": "Invalid payload"}), 400
    student_data = data['student']
    parent_data = data['parent']
    # Basic validation
    if not all(k in student_data for k in ("email", "name")) or not all(k in parent_data for k in ("email", "name")):
        return jsonify({"error": "Missing fields"}), 400
    try:
        # Ensure parent role exists
        parent_role = Role.query.filter_by(name='parent').first()
        if not parent_role:
            parent_role = Role(name='parent', level=10)
            db.session.add(parent_role)
            db.session.flush()
        # Create a user for parent (optional, could be just profile)
        pwd_hash = hash_password('default-pass')  # you may want a generated password
        
        # Simpler: create profile directly without a user (since parent may not log in)
        # Create parent profile
        parent_profile = Profile(full_name=parent_data['name'], school_id=1)  # assuming admin's school_id=1
        db.session.add(parent_profile)
        db.session.flush()
        # Create student profile (optional) then student record
        # For now we just create Student record linking to parent_profile.id
        # Generate a simple student_id
        student_id = f"STU{int(datetime.utcnow().timestamp())}"  # unique-ish
        student = Student(student_id=student_id, name=student_data['name'], gender='Other', date_of_birth='2000-01-01', class_id=1, parent_id=parent_profile.id)
        db.session.add(student)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
    return jsonify({"message": f"Student {student.name} and parent {parent_profile.full_name} created"}), 201
