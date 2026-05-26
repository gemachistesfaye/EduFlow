# backend/app/models.py
from .database import db
from datetime import datetime

class Role(db.Model):
    __tablename__ = "roles"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True, nullable=False)
    level = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"<Role {self.name} ({self.level})>"

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'), nullable=False)

    role = db.relationship('Role')
    profile = db.relationship('Profile', uselist=False, back_populates='user')

    def __repr__(self):
        return f"<User {self.email} ({self.role.name})>"

class Profile(db.Model):
    """Additional data per user – works for students, teachers, parents"""
    __tablename__ = "profiles"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    full_name = db.Column(db.String(120), nullable=False)
    school_id = db.Column(db.Integer, nullable=False)
    # For student → parent relationship
    parent_id = db.Column(db.Integer, db.ForeignKey('profiles.id'))

    user = db.relationship('User', back_populates='profile')
    parent = db.relationship('Profile', remote_side=[id], backref='children')

    def __repr__(self):
        return f"<Profile {self.full_name} (user={self.user.email})>"
