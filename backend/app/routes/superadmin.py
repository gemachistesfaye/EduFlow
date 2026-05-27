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
    # Placeholder data for the Super Admin dashboard
    return jsonify({
        "total_schools": 3,
        "revenue": "24,500.00",
        "uptime": "99.9%",
        "branches": [
            {"name": "Main Campus", "location": "Downtown", "students": 1250},
            {"name": "North Branch", "location": "Northside", "students": 840},
            {"name": "West Wing", "location": "West End", "students": 620}
        ]
    })

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
    # New endpoint: create a school branch and its director
    @bp.post('/create-branch')
    @rbac(100)
    def create_branch():
        data = request.json
        required = ['campus_name', 'location', 'director_name', 'director_email', 'password']
        if not all(k in data and data[k] for k in required):
            return jsonify({"error": "Missing required fields"}), 400
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
        return jsonify({"message": f"School {school.name} and Director {data['director_name']} created."}), 201
