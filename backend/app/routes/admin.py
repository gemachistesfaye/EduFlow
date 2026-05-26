from flask import Blueprint, jsonify
from ..middleware.auth import rbac

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
    data = request.json
    # Logic for cascading registration would go here
    return jsonify({"message": "Registration successful"}), 201
