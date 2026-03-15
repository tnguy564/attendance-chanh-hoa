from flask import Blueprint, request, jsonify, current_app
from datetime import datetime
import time

attendance_bp = Blueprint("attendance", __name__)

# ------------------------- GET ATTENDANCE -------------------------
@attendance_bp.route('/api/attendance', methods=['GET'])
def get_attendance():
    db = current_app.config.get("ATTENDANCE_DB")
    attendance_col = db.attendance_records
    students_col = db.students

    date = request.args.get('date')
    subject = request.args.get('subject')
    student_id = request.args.get('student_id')
    role = request.args.get('role')

    try:
        # Query attendance collection - find ALL matching sessions
        query = {}
        if date: query["date"] = date
        if subject: query["subject"] = subject

        attendance_docs = list(attendance_col.find(query))

        attendance_list = []

        for attendance_doc in attendance_docs:
            doc_date = str(attendance_doc.get("date", ""))
            doc_subject = str(attendance_doc.get("subject", ""))
            seen_students = set()

            for s in attendance_doc.get("students", []):
                sid = s.get("student_id")
                srole = s.get("role")

                if not sid or sid in seen_students:
                    continue
                seen_students.add(sid)

                # Apply filters
                if student_id and sid != student_id:
                    continue
                if role and srole != role:
                    continue

                present = bool(s.get("present"))
                marked_at = s.get("marked_at")
                if marked_at is not None:
                    try:
                        marked_at = marked_at.isoformat()
                    except Exception:
                        marked_at = str(marked_at)

                attendance_list.append({
                    "studentId": str(sid),
                    "studentName": s.get("student_name") or "",
                    "buddhaName": s.get("buddha_name") or "",
                    "role": str(srole) if srole else "",
                    "date": doc_date,
                    "subject": doc_subject,
                    "status": "present" if present else "absent",
                    "markedAt": marked_at
                })

        total = len(attendance_list)
        present_count = sum(1 for r in attendance_list if r["status"] == "present")
        absent_count = total - present_count
        rate = round((present_count / total * 100) if total > 0 else 0, 1)

        return jsonify({
            "success": True,
            "attendance": attendance_list,
            "stats": {
                "totalStudents": total,
                "presentToday": present_count,
                "absentToday": absent_count,
                "attendanceRate": rate
            }
        })

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


# ------------------------- EXPORT TO EXCEL -------------------------
@attendance_bp.route('/api/attendance/export', methods=['GET'])
def export_attendance():
    db = current_app.config.get("ATTENDANCE_DB")
    attendance_col = db.attendance_records
    students_col = db.students

    date = request.args.get('date')
    subject = request.args.get('subject')
    student_id = request.args.get('student_id')
    role = request.args.get('role')

    try:
        # Query attendance collection - find ALL matching sessions
        query = {}
        if date: query["date"] = date
        if subject: query["subject"] = subject

        attendance_docs = list(attendance_col.find(query))

        attendance_list = []

        for attendance_doc in attendance_docs:
            doc_date = str(attendance_doc.get("date", ""))
            doc_subject = str(attendance_doc.get("subject", ""))
            seen_students = set()

            for s in attendance_doc.get("students", []):
                sid = s.get("student_id")
                srole = s.get("role")

                if not sid or sid in seen_students:
                    continue
                seen_students.add(sid)

                if student_id and sid != student_id:
                    continue
                if role and srole != role:
                    continue

                present = bool(s.get("present"))
                marked_at = s.get("marked_at")
                if marked_at is not None:
                    try:
                        marked_at = marked_at.isoformat()
                    except Exception:
                        marked_at = str(marked_at)

                attendance_list.append({
                    "ID": str(sid),
                    "name": s.get("student_name") or "",
                    "buddha name": s.get("buddha_name") or "",
                    "role": str(srole) if srole else "",
                    "date": doc_date,
                    "subject": doc_subject,
                    "status": "present" if present else "absent",
                    "time": marked_at
                })

        return jsonify({"success": True, "data": attendance_list})

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500