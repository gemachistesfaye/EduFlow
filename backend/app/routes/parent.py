from flask import Blueprint, jsonify
from ..middleware.auth import rbac

bp = Blueprint('parent', __name__)

@bp.get('/dashboard')
@rbac(10)
def dashboard():
    return jsonify({"message": "Parent dashboard"})
