from flask import Blueprint
from . import auth, admin, teacher, student, parent, superadmin

def register_routes(app):
    app.register_blueprint(auth.bp, url_prefix='/api/auth')
    app.register_blueprint(admin.bp, url_prefix='/api/admin')
    app.register_blueprint(teacher.bp, url_prefix='/api/teacher')
    app.register_blueprint(student.bp, url_prefix='/api/student')
    app.register_blueprint(parent.bp, url_prefix='/api/parent')
    app.register_blueprint(superadmin.bp, url_prefix='/api/superadmin')
