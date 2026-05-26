from flask import Blueprint, jsonify, request
from ..middleware.auth import rbac
from ..models import db, User, Role, Profile
from ..utils.security import hash_password

bp = Blueprint('superadmin', __name__)

@bp.get('/dashboard')
@rbac(100)
def dashboard():
    return jsonify({"message": "Superadmin dashboard"})

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
