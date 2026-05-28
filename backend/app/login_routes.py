from flask import Blueprint, render_template, request, abort, redirect, url_for, flash
from werkzeug.security import check_password_hash

# Blueprint – register in app factory (app/__init__.py) via app.register_blueprint(login_bp)
login_bp = Blueprint('login', __name__)

# --------------------------------------------------------------
# Configuration for each portal – titles, placeholders, etc.
# --------------------------------------------------------------
PORTAL_CONFIG = {
    "staff": {
        "title": "Staff Login",
        "subtitle": "Manage classes, attendance & grades",
        "email_label": "Work Email",
        "email_placeholder": "staff@example.edu",
        "password_label": "Password",
        "password_placeholder": "••••••••",
        "footer_note": "Need help? Contact the admin desk.",
        "logo": "/static/img/logo_staff.svg",
    },
    "student": {
        "title": "Student Login",
        "subtitle": "Access timetable & grades",
        "email_label": "Student Email",
        "email_placeholder": "student@example.edu",
        "password_label": "Password",
        "password_placeholder": "••••••••",
        "footer_note": "Forgot password? Ask your teacher.",
        "logo": "/static/img/logo_student.svg",
    },
    "parent": {
        "title": "Parent Login",
        "subtitle": "View your child's progress",
        "email_label": "Parent Email",
        "email_placeholder": "parent@example.edu",
        "password_label": "Password",
        "password_placeholder": "••••••••",
        "footer_note": "Support: support@eduflow.com",
        "logo": "/static/img/logo_parent.svg",
    },
}

# --------------------------------------------------------------
# GET – render unified login template based on ?portal query param
# --------------------------------------------------------------
@login_bp.route('/login')
def login_get():
    portal = request.args.get('portal', 'staff').lower()
    if portal not in PORTAL_CONFIG:
        abort(404, description='Invalid portal')
    config = PORTAL_CONFIG[portal]
    return render_template('login.html', config=config, portal=portal)

# --------------------------------------------------------------
# POST – process login (placeholder logic – replace with real auth)
# --------------------------------------------------------------
@login_bp.route('/login', methods=['POST'])
def login_post():
    portal = request.form.get('role', '').lower()
    if portal not in PORTAL_CONFIG:
        abort(400, description='Invalid role')
    email = request.form.get('email', '').strip()
    password = request.form.get('password', '')
    # TODO: Replace with actual DB lookup and password verification
    # user = User.query.filter_by(email=email, role=portal).first()
    # if not user or not check_password_hash(user.password_hash, password):
    #     flash('Invalid credentials', 'error')
    #     return redirect(url_for('login.login_get', portal=portal))
    flash(f'Welcome, {portal.title()}!', 'success')
    # Redirect to a role‑specific dashboard – adjust route names as needed
    return redirect(url_for(f'{portal}.dashboard'))
