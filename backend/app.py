import os
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import mysql.connector
from mysql.connector import pooling
from config import Config

app = Flask(__name__, static_folder="../public")
app.config.from_object(Config)
CORS(app)

# --------------------------------------------------------------
# MySQL connection pool (reused across requests)
# --------------------------------------------------------------
_dbconfig = {
    "host": Config.MYSQL_HOST,
    "port": Config.MYSQL_PORT,
    "user": Config.MYSQL_USER,
    "password": Config.MYSQL_PASSWORD,
    "database": Config.MYSQL_DB,
}
cnxpool = pooling.MySQLConnectionPool(pool_name="mypool", pool_size=5, **_dbconfig)

def query(sql, params=None):
    cnx = cnxpool.get_connection()
    cursor = cnx.cursor(dictionary=True)
    cursor.execute(sql, params or ())
    rows = cursor.fetchall()
    cursor.close()
    cnx.close()
    return rows

# --------------------------------------------------------------
# Role helper (simple header‑based for demo – replace with JWT in prod)
# --------------------------------------------------------------
_role_map = {
    "superadmin": 100,
    "admin": 80,
    "teacher": 50,
    "student": 10,
    "parent": 10,
}

def get_role():
    return request.headers.get("X-User-Role", "student").lower()

def require_role(min_level):
    role = get_role()
    if _role_map.get(role, 0) < min_level:
        return False
    return True

# --------------------------------------------------------------
# API Endpoints – one per dashboard
# --------------------------------------------------------------
@app.route("/api/superadmin/system-overview")
def superadmin_overview():
    if not require_role(100):
        return jsonify({"error": "Forbidden"}), 403
    data = {
        "total_schools": query("SELECT COUNT(*) AS cnt FROM schools")[0]["cnt"],
        "revenue": query("SELECT SUM(amount) AS rev FROM payments")[0]["rev"] or 0,
        "uptime": os.popen("uptime -p").read().strip() or "N/A",
        "branches": [
            {
                "name": r["name"],
                "location": r["location"],
                "students": r["students"]
            }
            for r in query("SELECT name, location, student_count AS students FROM schools")
        ],
    }
    return jsonify(data)

@app.route("/api/admin/school-metrics")
def admin_metrics():
    if not require_role(80):
        return jsonify({"error": "Forbidden"}), 403
    data = {
        "students": query("SELECT COUNT(*) AS cnt FROM students")[0]["cnt"],
        "teachers": query("SELECT COUNT(*) AS cnt FROM teachers")[0]["cnt"],
        "fees_collected": query(
            "SELECT SUM(amount) AS total FROM payments WHERE type='tuition'"
        )[0]["total"] or 0,
    }
    return jsonify(data)

@app.route("/api/admin/cascade-register", methods=["POST"]) 
def cascade_register():
    if not require_role(80):
        return jsonify({"error": "Forbidden"}), 403
    payload = request.get_json()
    if not payload:
        return jsonify({"error": "Invalid JSON"}), 400
    # Expect: {student:{email, name}, parent:{email, name}}
    student = payload.get("student", {})
    parent = payload.get("parent", {})
    # Simple validation
    if not all([student.get("email"), student.get("name"), parent.get("email"), parent.get("name")]):
        return jsonify({"error": "Missing fields"}), 400
    # Call stored proc (or inline transaction) – this example uses a stored procedure
    cnx = cnxpool.get_connection()
    cursor = cnx.cursor()
    try:
        cursor.callproc(
            "create_student_with_parent",
            [
                # Assuming the school admin's school_id is known – for demo we use 1
                1,
                student["email"],
                "tempPassword123!",  # Password generation would be separate
                student["name"],
                parent["email"],
                parent["name"],
            ],
        )
        cnx.commit()
    except Exception as e:
        cnx.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        cnx.close()
    return jsonify({"message": "Student and parent created successfully"})

@app.route("/api/teacher/classroom-data")
def teacher_data():
    if not require_role(50):
        return jsonify({"error": "Forbidden"}), 403
    # In a real app you would filter by teacher ID from JWT – here we use header X-User-Id
    teacher_id = request.headers.get("X-User-Id")
    data = {
        "today_classes": query(
            "SELECT COUNT(*) AS cnt FROM classes WHERE DATE(date)=CURDATE()"
        )[0]["cnt"],
        "pending_grades": query(
            "SELECT COUNT(*) AS cnt FROM assignments WHERE graded=0"
        )[0]["cnt"],
        "timetable": query(
            "SELECT DAYNAME(date) AS day, period, subject, room FROM classes WHERE teacher_id=%s ORDER BY date, period",
            (teacher_id,)
        ),
    }
    return jsonify(data)

@app.route("/api/student/profile-analytics")
def student_analytics():
    if not require_role(10):
        return jsonify({"error": "Forbidden"}), 403
    student_id = request.headers.get("X-User-Id")
    # GPA – simple average of final grades
    gpa_row = query(
        "SELECT AVG(final_score) AS gpa FROM grades WHERE student_id=%s",
        (student_id,)
    )[0]
    gpa = round(gpa_row["gpa"] or 0, 2)
    # Attendance percentage (assumes attendance table with present flag)
    att = query(
        "SELECT AVG(present) AS att FROM attendance WHERE student_id=%s",
        (student_id,)
    )[0]
    attendance = int(round(att["att"] * 100)) if att["att"] is not None else 0
    # Detailed CA grades per subject
    grades = query(
        """
        SELECT s.name AS subject,
               MAX(CASE WHEN type='ca1' THEN score END) AS ca1,
               MAX(CASE WHEN type='ca2' THEN score END) AS ca2,
               MAX(CASE WHEN type='exam' THEN score END) AS exam,
               MAX(CASE WHEN type='final' THEN score END) AS final
        FROM grades g
        JOIN subjects s ON g.subject_id=s.id
        WHERE g.student_id=%s
        GROUP BY s.name
        """,
        (student_id,)
    )
    return jsonify({"gpa": gpa, "attendance": attendance, "grades": grades})

@app.route("/api/parent/children-tracker")
def parent_tracker():
    if not require_role(10):
        return jsonify({"error": "Forbidden"}), 403
    parent_id = request.headers.get("X-User-Id")
    # List children linked to this parent
    children = query(
        "SELECT id, full_name AS name FROM students WHERE parent_id=%s",
        (parent_id,)
    )
    # Determine which child is requested (default first)
    child_id = request.args.get("child_id") or (children[0]["id"] if children else None)
    if not child_id:
        return jsonify({"children": [], "fees": 0, "trend": []})
    # Fees owed for selected child
    fees_row = query(
        "SELECT SUM(amount) AS total FROM payments WHERE student_id=%s AND status='due'",
        (child_id,)
    )[0]
    fees = fees_row["total"] or 0
    # Simple performance trend – last 6 months average scores
    trend = query(
        """
        SELECT DATE_FORMAT(date, '%Y-%m') AS month,
               AVG(score) AS score
        FROM grades g
        JOIN subjects s ON g.subject_id=s.id
        WHERE g.student_id=%s
        GROUP BY month
        ORDER BY month DESC
        LIMIT 6
        """,
        (child_id,)
    )
    return jsonify({"children": children, "selected_child_id": child_id, "fees": fees, "trend": trend})

# --------------------------------------------------------------
# Serve static dashboard HTML files (fallback to index.html for SPA)
# --------------------------------------------------------------
@app.route("/dashboards/<path:filename>")
def serve_dashboard(filename):
    # The static folder is ../public, which contains the dashboards subfolder
    return send_from_directory(os.path.join(app.static_folder, "dashboards"), filename)

# Root – optional landing (could redirect to login)
@app.route('/')
def root():
    return send_from_directory(app.static_folder, 'index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
