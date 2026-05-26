from flask import Blueprint, jsonify
from ..middleware.auth import rbac

bp = Blueprint('admin', __name__)

@bp.get('/dashboard')
@rbac(80)
def dashboard():
    return jsonify({"message": "Admin dashboard"})
