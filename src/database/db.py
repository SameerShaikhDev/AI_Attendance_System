from src.database.config import supabase
import bcrypt
from datetime import datetime, timezone


def hash_pass(pwd):
    return bcrypt.hashpw(pwd.encode(), bcrypt.gensalt()).decode()

def check_pass(password, hashed):
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))


# ── Teachers ──────────────────────────────
def check_techer_exist(username):
    response = supabase.table("teachers").select("username").eq("username", username).execute()
    return len(response.data) > 0

def create_teacher(username, password, name):
    data = {"username": username, "password": hash_pass(password), "name": name}
    response = supabase.table("teachers").insert(data).execute()
    return response.data

def teacher_login(username, password):
    response = supabase.table("teachers").select("*").eq("username", username).execute()
    if response.data:
        teacher = response.data[0]
        if check_pass(password, teacher["password"]):
            return teacher
    return None

def get_teacher_subjects(teacher_id):
    response = supabase.table("subjects").select("*").eq("teacher_id", teacher_id).execute()
    return response.data or []


# ── Students ──────────────────────────────
def get_all_students():
    response = supabase.table("students").select("*").execute()
    return response.data or []

def create_student(new_name, face_embedding=None, voice_embedding=None):
    data = {'name': new_name, 'face_embedding': face_embedding, 'voice_embedding': voice_embedding}
    response = supabase.table('students').insert(data).execute()
    return response.data

def get_students_by_subject(subject_id):
    response = (
        supabase.table("subject_student")
        .select("student_id, students(student_id, name)")
        .eq("subject_id", subject_id)
        .execute()
    )
    students = []
    for row in (response.data or []):
        if row.get("students"):
            students.append(row["students"])
    return students


# ── Attendance ────────────────────────────
def save_attendance(subject_id, results: dict, all_student_ids: list):
    """
    results = {student_id: True}  (present ones)
    all_student_ids = list of every student in that subject
    """
    now = datetime.now(timezone.utc).isoformat()
    rows = []
    for sid in all_student_ids:
        rows.append({
            "subject_id": subject_id,
            "student_id": sid,
            "is_present": sid in results,
            "timestamp": now,
        })
    if rows:
        supabase.table("attendace_logs").insert(rows).execute()

def get_attendance_records(teacher_id, subject_id=None, date_from=None, date_to=None):
    """
    Returns list of attendance log rows joined with student name and subject name.
    Filters by teacher's subjects.
    """
    # get this teacher's subject ids
    teacher_subjects = get_teacher_subjects(teacher_id)
    subject_ids = [s["subject_id"] for s in teacher_subjects]

    if not subject_ids:
        return []

    if subject_id:
        subject_ids = [subject_id] if subject_id in subject_ids else []

    if not subject_ids:
        return []

    query = (
        supabase.table("attendace_logs")
        .select("id, timestamp, is_present, student_id, subject_id, students(name), subjects(name, subject_code, section)")
        .in_("subject_id", subject_ids)
        .order("timestamp", desc=True)
    )

    if date_from:
        query = query.gte("timestamp", date_from)
    if date_to:
        query = query.lte("timestamp", date_to)

    response = query.execute()
    return response.data or []

# ── Student Subject Functions ──────────────────────────────

def get_student_subjects(student_id):
    """Student ke saare enrolled subjects — recent first"""
    response = (
        supabase.table("subject_student")
        .select("subject_id, subjects(subject_id, name, subject_code, section, teacher_id, teachers(name))")
        .eq("student_id", student_id)
        .execute()
    )
    subjects = []
    for row in (response.data or []):
        if row.get("subjects"):
            subjects.append(row["subjects"])
    return subjects

def enroll_student_by_code(student_id, subject_code):
    """Subject code se student ko enroll karo"""
    # subject dhundo
    subj_resp = supabase.table("subjects").select("*").eq("subject_code", subject_code).execute()
    if not subj_resp.data:
        return None, "Subject nahi mila — code check karo"

    subject = subj_resp.data[0]
    subject_id = subject["subject_id"]

    # already enrolled check
    already = (
        supabase.table("subject_student")
        .select("student_id")
        .eq("subject_id", subject_id)
        .eq("student_id", student_id)
        .execute()
    )
    if already.data:
        return None, "Tum already is subject mein enrolled ho"

    # enroll karo
    supabase.table("subject_student").insert({
        "subject_id": subject_id,
        "student_id": student_id
    }).execute()
    return subject, None

def get_student_attendance_summary(student_id):
    """Student ke har subject ki present/total count"""
    response = (
        supabase.table("attendace_logs")
        .select("subject_id, is_present, subjects(name, subject_code, section)")
        .eq("student_id", student_id)
        .execute()
    )
    summary = {}
    for row in (response.data or []):
        sid = row["subject_id"]
        if sid not in summary:
            subj = row.get("subjects") or {}
            summary[sid] = {
                "subject_id": sid,
                "name": subj.get("name", "Unknown"),
                "subject_code": subj.get("subject_code", ""),
                "section": subj.get("section", ""),
                "total": 0,
                "present": 0,
            }
        summary[sid]["total"] += 1
        if row["is_present"]:
            summary[sid]["present"] += 1
    return list(summary.values())

def get_student_recent_attendance(student_id, limit=10):
    """Student ki recent attendance logs — latest first"""
    response = (
        supabase.table("attendace_logs")
        .select("id, timestamp, is_present, subject_id, subjects(name, subject_code, section)")
        .eq("student_id", student_id)
        .order("timestamp", desc=True)
        .limit(limit)
        .execute()
    )
    return response.data or []