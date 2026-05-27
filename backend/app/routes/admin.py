from flask import Blueprint, jsonify, request
from ..middleware.auth import rbac
from ..models import db, Student, Profile, Role, School
from ..utils.security import hash_password
import datetime
bp = Blueprint('admin', __name__)

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
