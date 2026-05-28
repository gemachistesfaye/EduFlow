from flask import Blueprint, jsonify, request
from ..middleware.auth import rbac
from ..models import db, User, Role, Profile, School
from ..utils.security import hash_password

bp = Blueprint('superadmin', __name__)

@bp.get('/dashboard')
@rbac(100)
def dashboard():
    return jsonify({"message": "Superadmin dashboard"})

@bp.get('/system-overview')
@rbac(100)
def system_overview():
    try:
        schools = School.query.all()
        branches_data = []
        for s in schools:
            # Find the school director user
            director = User.query.filter_by(school_id=s.id).join(Role).filter(Role.name == 'school_director').first()
            director_name = director.profile.full_name if (director and director.profile) else "No Director"
            director_email = director.email if director else "N/A"
            
            # Count the students (profiles registered for this school)
            student_count = Profile.query.filter_by(school_id=s.id).join(User).join(Role).filter(Role.name == 'student').count()
            # If no student profiles exist, fall back to counting total profiles minus director/admin
            if student_count == 0:
                student_count = Profile.query.filter_by(school_id=s.id).count()
                if director:
                    student_count = max(0, student_count - 1)
            
            branches_data.append({
                "id": s.id,
                "name": s.name,
                "location": s.location,
                "director_name": director_name,
                "director_email": director_email,
                "students": student_count
            })
            
        return jsonify({
            "total_schools": len(schools),
            "revenue": "24,500.00",
            "uptime": "99.9%",
            "branches": branches_data
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@bp.post('/create-user')
@rbac(100)
def create_user():
    data = request.json
    email = data.get('email')
    password = data.get('password')
    full_name = data.get('full_name')
    role_name = data.get('role')  # 'admin' or 'school_director'

    if not all([email, password, full_name, role_name]):
        return jsonify({"error": "Missing required fields"}), 400

    # Ensure role exists or create it
    role = Role.query.filter_by(name=role_name).first()
    if not role:
        level = 80 if role_name in ['admin', 'school_director'] else 10
        role = Role(name=role_name, level=level)
        db.session.add(role)
        db.session.commit()

    if User.query.filter_by(email=email).first():
        return jsonify({"error": "Email already registered"}), 409

    pwd_hash = hash_password(password)
    user = User(email=email, password_hash=pwd_hash, role_id=role.id)
    db.session.add(user)
    db.session.commit()

    profile = Profile(user_id=user.id, full_name=full_name, school_id=1)
    db.session.add(profile)
    db.session.commit()

    return jsonify({"message": f"User {full_name} created successfully as {role_name}"}), 201

# Create a school branch and its director
@bp.post('/create-branch')
@rbac(100)
def create_branch():
    data = request.json
    required = ['campus_name', 'location', 'director_name', 'director_email', 'password']
    if not all(k in data and data[k] for k in required):
        return jsonify({"error": "Missing required fields"}), 400
    
    try:
        # Create school
        school = School(name=data['campus_name'], location=data['location'])
        db.session.add(school)
        db.session.flush()  # get school.id without committing
        
        # Ensure director role exists
        role = Role.query.filter_by(name='school_director').first()
        if not role:
            role = Role(name='school_director', level=80)
            db.session.add(role)
            db.session.flush()
            
        # Create user for director
        pwd_hash = hash_password(data['password'])
        user = User(email=data['director_email'], password_hash=pwd_hash,
                    role_id=role.id, school_id=school.id)
        db.session.add(user)
        db.session.flush()
        
        # Create profile for director
        profile = Profile(user_id=user.id, full_name=data['director_name'], school_id=school.id)
        db.session.add(profile)
        db.session.commit()
        return jsonify({"message": f"School branch '{school.name}' and Director {data['director_name']} created successfully."}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

# Delete a school branch
@bp.delete('/delete-branch/<int:school_id>')
@rbac(100)
def delete_branch(school_id):
    school = School.query.get(school_id)
    if not school:
        return jsonify({"error": "Branch not found"}), 404
        
    try:
        # Delete related profiles and users first to avoid FK constraint violations
        users_to_delete = User.query.filter_by(school_id=school_id).all()
        user_ids = [u.id for u in users_to_delete]
        if user_ids:
            Profile.query.filter(Profile.user_id.in_(user_ids)).delete(synchronize_session=False)
            User.query.filter(User.id.in_(user_ids)).delete(synchronize_session=False)
            
        db.session.delete(school)
        db.session.commit()
        return jsonify({"message": f"School branch '{school.name}' deleted successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

