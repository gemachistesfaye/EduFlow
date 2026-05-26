from flask import Blueprint, jsonify
from ..middleware.auth import rbac

bp = Blueprint('teacher', __name__)

@bp.get('/dashboard')
@rbac(50)
def dashboard():
    return jsonify({"message": "Teacher dashboard"})
