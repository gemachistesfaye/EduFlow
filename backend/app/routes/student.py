from flask import Blueprint, jsonify
from ..middleware.auth import rbac

bp = Blueprint('student', __name__)

@bp.get('/dashboard')
@rbac(10)
def dashboard():
    return jsonify({"message": "Student dashboard"})
