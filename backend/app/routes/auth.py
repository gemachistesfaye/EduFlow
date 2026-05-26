from flask import Blueprint, request, jsonify
from ..models import User
from ..utils.security import verify_password, create_access_token

bp = Blueprint('auth', __name__)

@bp.post('/login')
def login():
    data = request.json
    email = data.get('email')
    pwd = data.get('password')
    user = User.query.filter_by(email=email).first()
    if not user or not verify_password(pwd, user.password_hash):
        return jsonify({"error": "Invalid credentials"}), 401

    token = create_access_token(user.id, user.role.name, user.role.level)
    return jsonify({"access_token": token, "role": user.role.name})
