# backend/app/models.py
"""SQLAlchemy ORM models for the School Management System.
Includes core entities: Role, User, Profile (generic user data),
Student, Teacher, Class, Attendance, Grade, Fee, Exam.
All tables are linked via foreign keys where appropriate.
"""

from .database import db
from datetime import datetime

# ---------------------------------------------------------------------------
# Core authentication models
# ---------------------------------------------------------------------------
class Role(db.Model):
    __tablename__ = "roles"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True, nullable=False)
    level = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"<Role {self.name} ({self.level})>"

# New model for school branches
class School(db.Model):
    __tablename__ = "schools"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    location = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return f"<School {self.name} ({self.location})>"

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'), nullable=False)
    school_id = db.Column(db.Integer, db.ForeignKey('schools.id'))  # link director to school

    role = db.relationship('Role')
    profile = db.relationship('Profile', uselist=False, back_populates='user')
    school = db.relationship('School', foreign_keys=[school_id])  # link user to school

    def __repr__(self):
        return f"<User {self.email} ({self.role.name})>"

class Profile(db.Model):
    """Additional data for any user (students, teachers, parents)."""
    __tablename__ = "profiles"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    full_name = db.Column(db.String(120), nullable=False)
    school_id = db.Column(db.Integer, nullable=False)
    # For student → parent relationship (self‑referencing)
    parent_id = db.Column(db.Integer, db.ForeignKey('profiles.id'))

    user = db.relationship('User', back_populates='profile')
    parent = db.relationship('Profile', remote_side=[id], backref='children')

    def __repr__(self):
        return f"<Profile {self.full_name} (user={self.user.email})>"

# ---------------------------------------------------------------------------
# Core operational tables (9 modules)
# ---------------------------------------------------------------------------
class Class(db.Model):
    __tablename__ = "classes"
    id = db.Column(db.Integer, primary_key=True)
    class_name = db.Column(db.String(50), nullable=False)
    section = db.Column(db.String(10), nullable=False)
    academic_year = db.Column(db.String(9), nullable=False)  # e.g. "2023/2024"

    def __repr__(self):
        return f"<Class {self.class_name}-{self.section} ({self.academic_year})>"

class Student(db.Model):
    __tablename__ = "students"
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.String(20), unique=True, nullable=False)
    name = db.Column(db.String(120), nullable=False)
    gender = db.Column(db.Enum('Male', 'Female', 'Other', name='gender_enum'), nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)
    class_id = db.Column(db.Integer, db.ForeignKey('classes.id'), nullable=False)
    phone = db.Column(db.String(20))
    address = db.Column(db.String(255))
    enrollment_date = db.Column(db.Date, default=datetime.utcnow)
    parent_id = db.Column(db.Integer, db.ForeignKey('profiles.id'))

    class_ = db.relationship('Class')
    parent = db.relationship('Profile', foreign_keys=[parent_id])

    def __repr__(self):
        return f"<Student {self.student_id} {self.name}>"

class Teacher(db.Model):
    __tablename__ = "teachers"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    subject = db.Column(db.String(80), nullable=False)
    phone = db.Column(db.String(20))
    email = db.Column(db.String(120), unique=True)
    hire_date = db.Column(db.Date, default=datetime.utcnow)

    def __repr__(self):
        return f"<Teacher {self.name} ({self.subject})>"

class Attendance(db.Model):
    __tablename__ = "attendance"
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    status = db.Column(db.Enum('Present', 'Absent', 'Late', name='attendance_status_enum'), nullable=False)

    student = db.relationship('Student')

    def __repr__(self):
        return f"<Attendance {self.student_id} {self.date} {self.status}>"

class Grade(db.Model):
    __tablename__ = "grades"
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    subject = db.Column(db.String(80), nullable=False)
    exam_type = db.Column(db.Enum('Quiz', 'Mid', 'Final', name='exam_type_enum'), nullable=False)
    score = db.Column(db.Float, nullable=False)
    total_marks = db.Column(db.Float, nullable=False)

    student = db.relationship('Student')

    def __repr__(self):
        return f"<Grade {self.student_id} {self.subject} {self.exam_type}>"

class Fee(db.Model):
    __tablename__ = "fees"
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    paid_amount = db.Column(db.Float, default=0.0)
    status = db.Column(db.Enum('Paid', 'Pending', name='fee_status_enum'), nullable=False, default='Pending')
    due_date = db.Column(db.Date, nullable=False)

    student = db.relationship('Student')

    def __repr__(self):
        return f"<Fee {self.student_id} {self.amount} {self.status}>"

class Exam(db.Model):
    __tablename__ = "exams"
    id = db.Column(db.Integer, primary_key=True)
    exam_name = db.Column(db.String(120), nullable=False)
    exam_date = db.Column(db.Date, nullable=False)
    academic_year = db.Column(db.String(9), nullable=False)

    def __repr__(self):
        return f"<Exam {self.exam_name} ({self.academic_year})>"
