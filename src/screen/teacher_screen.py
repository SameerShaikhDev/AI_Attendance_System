import streamlit as st
import time
import numpy as np
from PIL import Image

from src.ui.style_base import style_home, style_page, style_ui
from src.components.header import header_dashbaord
from src.database.db import check_techer_exist, create_teacher, teacher_login, get_all_students
from src.pipelines.face_pipeline import predict_attendance


TEACHER_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Fredoka+One&family=Nunito:wght@400;600;700;800&display=swap');

.auth-card {
    background: #2d4a2d;
    border: 2px solid #5a7a5a;
    border-radius: 20px;
    padding: 40px 36px;
    max-width: 460px;
    margin: 24px auto;
    position: relative;
}
.auth-card::before {
    content: '';
    position: absolute;
    inset: 5px;
    border: 1px dashed rgba(240,230,208,0.08);
    border-radius: 14px;
    pointer-events: none;
}
.auth-icon { text-align: center; font-size: 52px; margin-bottom: 8px; }
.auth-title { text-align: center; font-family: 'Fredoka One', cursive; font-size: 1.8rem; color: #f0e6d0; margin-bottom: 4px; }
.auth-subtitle { text-align: center; font-size: 0.85rem; color: #8fbc8f; margin-bottom: 24px; }

.welcome-banner {
    background: linear-gradient(135deg, rgba(45,74,45,0.9), rgba(74,106,74,0.6));
    border: 2px solid #5a7a5a;
    border-radius: 16px;
    padding: 24px 28px;
    margin-bottom: 24px;
    display: flex;
    align-items: center;
    gap: 16px;
    position: relative;
}
.welcome-banner::before {
    content: '';
    position: absolute;
    inset: 4px;
    border: 1px dashed rgba(240,230,208,0.07);
    border-radius: 10px;
    pointer-events: none;
}
.welcome-avatar { font-size: 52px; line-height: 1; }
.welcome-text-name { font-family: 'Fredoka One', cursive; font-size: 1.6rem; color: #f0e6d0; margin: 0; }
.welcome-text-sub { font-size: 0.82rem; color: #8fbc8f; margin: 4px 0 0; }

.stat-row { display: flex; gap: 12px; margin-bottom: 24px; flex-wrap: wrap; }
.stat-chip {
    background: rgba(45,74,45,0.8);
    border: 1.5px solid #4a6a4a;
    border-radius: 14px;
    padding: 16px 20px;
    flex: 1;
    min-width: 110px;
    text-align: center;
}
.stat-chip-num { font-family: 'Fredoka One', cursive; font-size: 2rem; color: #e8a020; line-height: 1; }
.stat-chip-label { font-size: 0.7rem; font-weight: 800; letter-spacing: 1.5px; text-transform: uppercase; color: rgba(240,230,208,0.4); margin-top: 4px; }

.section-label { font-size: 0.72rem; font-weight: 800; letter-spacing: 2px; text-transform: uppercase; color: rgba(240,230,208,0.35); margin-bottom: 12px; }

.dash-card {
    background: #2d4a2d;
    border: 2px solid #4a6a4a;
    border-radius: 16px;
    padding: 24px 16px;
    text-align: center;
    transition: border-color 0.2s, transform 0.2s;
    cursor: pointer;
    margin-bottom: 8px;
}
.dash-card:hover { border-color: #8fbc8f; transform: translateY(-2px); }
.dash-card-icon { font-size: 36px; margin-bottom: 10px; }
.dash-card-title { font-family: 'Fredoka One', cursive; font-size: 1.1rem; color: #f0e6d0; margin-bottom: 4px; }
.dash-card-desc { font-size: 0.78rem; color: #8fbc8f; }

.att-result-card { border-radius: 12px; padding: 12px 16px; margin-bottom: 8px; display: flex; align-items: center; gap: 12px; }
.att-present { background: rgba(34,197,94,0.12); border: 1.5px solid rgba(34,197,94,0.3); }
.att-absent  { background: rgba(239,68,68,0.1);  border: 1.5px solid rgba(239,68,68,0.25); }
.att-name { font-family: 'Nunito', sans-serif; font-size: 1rem; font-weight: 700; color: #f0e6d0; flex: 1; }
.att-badge-present { background: #16a34a; color: #fff; font-size: 0.7rem; font-weight: 800; padding: 3px 10px; border-radius: 20px; letter-spacing: 1px; }
.att-badge-absent  { background: #dc2626; color: #fff; font-size: 0.7rem; font-weight: 800; padding: 3px 10px; border-radius: 20px; letter-spacing: 1px; }

.summary-box {
    background: rgba(45,74,45,0.7);
    border: 1.5px solid #4a6a4a;
    border-radius: 14px;
    padding: 16px 20px;
    margin-bottom: 20px;
    display: flex;
    gap: 28px;
    align-items: center;
    flex-wrap: wrap;
}
.sum-num { font-family: 'Fredoka One', cursive; font-size: 2rem; }
.sum-label { font-size: 0.7rem; font-weight: 800; text-transform: uppercase; letter-spacing: 1px; color: rgba(240,230,208,0.4); margin-top: 2px; }
</style>
"""


# ─────────────────────────────────────────
#  Router
# ─────────────────────────────────────────
def teacher_screen():
    style_ui()
    style_page()
    st.markdown(TEACHER_CSS, unsafe_allow_html=True)

    if 'teacher_data' not in st.session_state:
        if st.session_state.get('teacher_type') == 'register':
            teacher_register_page()
        else:
            teacher_login_page()
        return

    # sub-page routing inside dashboard
    page = st.session_state.get('teacher_page', 'home')
    if page == 'attendance':
        attendance_page()
    elif page == 'records':
        records_page()
    elif page == 'subjects':
        manage_subjects_page()
    else:
        teacher_dashboard()


# ─────────────────────────────────────────
#  Dashboard
# ─────────────────────────────────────────
def teacher_dashboard():
    teacher = st.session_state.teacher_data

    col_left, col_right = st.columns([6, 1])
    with col_right:
        if st.button("Logout", type="secondary"):
            for k in ['teacher_data', 'user_role', 'is_logged_in', 'login_type', 'teacher_page']:
                st.session_state.pop(k, None)
            st.rerun()

    st.markdown(f"""
    <div class="welcome-banner">
        <div class="welcome-avatar">👩‍🏫</div>
        <div>
            <p class="welcome-text-name">Welcome back, {teacher['name']}!</p>
            <p class="welcome-text-sub">@{teacher['username']} &nbsp;·&nbsp; Teacher Dashboard</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    all_students = get_all_students() or []
    st.markdown(f"""
    <div class="stat-row">
        <div class="stat-chip"><div class="stat-chip-num">{len(all_students)}</div><div class="stat-chip-label">Students</div></div>
        <div class="stat-chip"><div class="stat-chip-num">—</div><div class="stat-chip-label">Subjects</div></div>
        <div class="stat-chip"><div class="stat-chip-num">—</div><div class="stat-chip-label">Classes Today</div></div>
        <div class="stat-chip"><div class="stat-chip-num">—</div><div class="stat-chip-label">Avg Attendance</div></div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<p class="section-label">Quick Actions</p>', unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3, gap="medium")
    with c1:
        st.markdown("""
        <div class="dash-card">
            <div class="dash-card-icon">📋</div>
            <div class="dash-card-title">Take Attendance</div>
            <div class="dash-card-desc">Upload class photos to mark attendance</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Take Attendance →", type="primary", use_container_width=True, key="go_att"):
            st.session_state['teacher_page'] = 'attendance'
            st.rerun()
    with c2:
        st.markdown("""
        <div class="dash-card">
            <div class="dash-card-icon">👥</div>
            <div class="dash-card-title">My Students</div>
            <div class="dash-card-desc">View & manage students</div>
        </div>
        """, unsafe_allow_html=True)
    with c3:
        st.markdown("""
        <div class="dash-card">
            <div class="dash-card-icon">📚</div>
            <div class="dash-card-title">Subjects</div>
            <div class="dash-card-desc">Manage your subjects & enroll students</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Manage Subjects →", type="primary", use_container_width=True, key="go_subj"):
            st.session_state['teacher_page'] = 'subjects'
            st.rerun()

    st.write("")
    st.markdown('<p class="section-label">Reports</p>', unsafe_allow_html=True)
    c4, _ = st.columns([1, 2], gap="medium")
    with c4:
        st.markdown("""
        <div class="dash-card">
            <div class="dash-card-icon">📊</div>
            <div class="dash-card-title">View Records</div>
            <div class="dash-card-desc">Past attendance with date & subject filter</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("View Records →", type="primary", use_container_width=True, key="go_rec"):
            st.session_state['teacher_page'] = 'records'
            st.rerun()


# ─────────────────────────────────────────
#  Manage Subjects Page
# ─────────────────────────────────────────
def manage_subjects_page():
    from src.database.db import get_teacher_subjects, get_all_students
    from src.database.config import supabase

    teacher = st.session_state.teacher_data
    teacher_id = teacher['teacher_id']

    if st.button("← Back to Dashboard", type="secondary", key="subj_back"):
        st.session_state['teacher_page'] = 'home'
        st.rerun()

    st.markdown("## 📚 Manage Subjects")

    # ── Add new subject ──
    with st.container(border=True):
        st.markdown("### ➕ Add New Subject")
        c1, c2, c3 = st.columns(3)
        with c1:
            subj_name = st.text_input("Subject Name", placeholder="e.g. Mathematics")
        with c2:
            subj_code = st.text_input("Subject Code", placeholder="e.g. MATH101")
        with c3:
            subj_section = st.text_input("Section", placeholder="e.g. A")

        if st.button("Add Subject", type="primary"):
            if subj_name and subj_code and subj_section:
                try:
                    supabase.table("subjects").insert({
                        "name": subj_name,
                        "subject_code": subj_code,
                        "section": subj_section,
                        "teacher_id": teacher_id
                    }).execute()
                    st.session_state['show_share_dialog'] = {
                        'name': subj_name,
                        'code': subj_code
                    }
                    st.rerun()
                except Exception as e:
                    st.error(f"Error: {e}")
            else:
                st.warning("Sabhi fields fill karo")

    # Share dialog — subject add hone ke turant baad
    from src.components.share_subject import share_subject
    if 'show_share_dialog' in st.session_state:
        info = st.session_state.pop('show_share_dialog')
        share_subject(info['name'], info['code'])

    st.divider()

    # ── Existing subjects with student enrollment ──
    subjects = get_teacher_subjects(teacher_id)
    if not subjects:
        st.info("Koi subject nahi hai abhi. Upar se add karo.")
        return

    all_students = get_all_students()
    student_map = {s['student_id']: s['name'] for s in all_students}

    st.markdown("### 📋 Your Subjects")
    for subj in subjects:
        with st.expander(f"📖 {subj['name']} ({subj['subject_code']}) - Section {subj['section']}"):
            # currently enrolled
            from src.database.db import get_students_by_subject
            enrolled = get_students_by_subject(subj['subject_id'])
            enrolled_ids = {s['student_id'] for s in enrolled}

            st.markdown(f"**Enrolled Students: {len(enrolled)}**")
            if enrolled:
                for s in enrolled:
                    col_a, col_b = st.columns([4, 1])
                    with col_a:
                        st.write(f"👤 {s['name']}")
                    with col_b:
                        if st.button("Remove", key=f"rem_{subj['subject_id']}_{s['student_id']}"):
                            supabase.table("subject_student").delete()\
                                .eq("subject_id", subj['subject_id'])\
                                .eq("student_id", s['student_id']).execute()
                            st.rerun()

            # enroll new students
            unenrolled = [s for s in all_students if s['student_id'] not in enrolled_ids]
            if unenrolled:
                st.markdown("**Add Student:**")
                options = {s['name']: s['student_id'] for s in unenrolled}
                selected_name = st.selectbox("Select student", list(options.keys()), key=f"enroll_{subj['subject_id']}")
                if st.button("Enroll", key=f"enroll_btn_{subj['subject_id']}", type="primary"):
                    try:
                        supabase.table("subject_student").insert({
                            "subject_id": subj['subject_id'],
                            "student_id": options[selected_name]
                        }).execute()
                        st.success(f"{selected_name} enrolled!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error: {e}")


# ─────────────────────────────────────────
#  Attendance Page
# ─────────────────────────────────────────
def attendance_page():
    if st.button("← Back to Dashboard", type="secondary"):
        st.session_state['teacher_page'] = 'home'
        st.session_state.pop('att_results', None)
        st.rerun()

    st.markdown("## 📋 Take Attendance")
    st.markdown('<p class="section-label">Subject chunno → Lecture number → Photos upload karo</p>', unsafe_allow_html=True)

    from src.database.db import get_teacher_subjects, get_students_by_subject, save_attendance

    teacher = st.session_state.teacher_data
    teacher_id = teacher['teacher_id']

    # ── Step 1: Subject select ──
    subjects = get_teacher_subjects(teacher_id)
    if not subjects:
        st.warning("⚠️ Koi subject nahi mila.")
        st.info("Pehle subject add karo aur students enroll karo.")
        if st.button("📚 Subjects Manage Karo", type="primary"):
            st.session_state['teacher_page'] = 'subjects'
            st.rerun()
        return

    subject_options = {f"{s['name']} ({s['subject_code']}) - Section {s['section']}": s for s in subjects}

    col1, col2 = st.columns(2)
    with col1:
        selected_label = st.selectbox("📖 Subject / Class", list(subject_options.keys()))
        selected_subject = subject_options[selected_label]
        selected_subject_id = selected_subject['subject_id']
    with col2:
        lecture_number = st.number_input(
            "🔢 Lecture Number (aaj ka)",
            min_value=1, max_value=20, value=1, step=1,
            help="Subah se 1st class hai ya 2nd? Woh number daalo"
        )

    # fetch enrolled students
    enrolled_students = get_students_by_subject(selected_subject_id)
    if not enrolled_students:
        st.warning(f"Is subject mein koi student enrolled nahi hai.")
        st.info("Pehle students enroll karo.")
        if st.button("📚 Students Enroll Karo", type="primary"):
            st.session_state['teacher_page'] = 'subjects'
            st.rerun()
        return

    student_map = {s['student_id']: s['name'] for s in enrolled_students}
    all_student_ids = [s['student_id'] for s in enrolled_students]

    st.info(f"👥 **{len(enrolled_students)} students** enrolled  |  📚 **{selected_subject['name']}**  |  🔢 **Lecture #{lecture_number}**")

    # ── Step 2: Photos upload ──
    st.divider()
    st.markdown("### 📸 Class Photos Upload Karo")
    st.caption("Ek ya zyada photos upload karo — jitne angle se leni ho")

    uploaded_files = st.file_uploader(
        "Class ki photos yahan daalo",
        type=["jpg", "jpeg", "png", "webp"],
        accept_multiple_files=True,
    )

    use_camera = st.checkbox("📷 Camera se lo")
    camera_photo = None
    if use_camera:
        camera_photo = st.camera_input("Class photo lo")

    # collect images
    images_to_process = []
    if uploaded_files:
        for f in uploaded_files:
            images_to_process.append(('upload', f.name, np.array(Image.open(f).convert("RGB"))))
    if camera_photo:
        images_to_process.append(('camera', 'Camera Photo', np.array(Image.open(camera_photo).convert("RGB"))))

    if images_to_process:
        st.markdown(f"**✅ {len(images_to_process)} photo(s) ready**")

        thumb_cols = st.columns(min(len(images_to_process), 5))
        for i, (_, name, img_arr) in enumerate(images_to_process):
            with thumb_cols[i % 5]:
                st.image(img_arr, caption=name, width=120)

        st.write("")
        if st.button("🔍 Photos Scan Karo", type="primary", use_container_width=True):
            present_ids = set()
            total_faces = 0
            per_image_log = []

            progress = st.progress(0, text="Photos scan ho rahi hain...")

            for idx, (_, name, img_arr) in enumerate(images_to_process):
                try:
                    detected, all_ids, num_faces = predict_attendance(img_arr)
                    total_faces += num_faces
                    present_ids.update(detected.keys())
                    per_image_log.append({'name': name, 'faces': num_faces, 'detected': list(detected.keys())})
                except Exception as e:
                    per_image_log.append({'name': name, 'faces': 0, 'detected': [], 'error': str(e)})

                progress.progress((idx + 1) / len(images_to_process), text=f"Done {idx+1}/{len(images_to_process)}")

            progress.empty()

            # Sirf preview -- abhi DB mein save NAHI hua. Confirm dabane ke baad hi save hoga.
            st.session_state['att_preview'] = {
                'present_ids': list(present_ids),
                'all_students': enrolled_students,
                'student_map': student_map,
                'total_faces': total_faces,
                'per_image_log': per_image_log,
                'subject_name': selected_subject['name'],
                'lecture_number': lecture_number,
                'subject_id': selected_subject_id,
                'all_student_ids': all_student_ids,
            }
            st.session_state.pop('att_results', None)
            st.rerun()

    # ── Preview + Confirmation (kuch bhi save nahi hota jab tak Confirm na dabao) ──
    if 'att_preview' in st.session_state:
        prev = st.session_state['att_preview']
        preview_present_ids = set(prev['present_ids'])
        students = prev['all_students']
        smap = prev['student_map']

        st.divider()
        st.markdown(f"### 👀 Preview — {prev.get('subject_name','')} | Lecture #{prev.get('lecture_number','')}")
        st.warning("⚠️ Yeh sirf preview hai, abhi tak kuch save nahi hua. Agar kisi ka face detect nahi hua (photo angle/lighting ki wajah se), to neeche manually tick kar do. Sab check karne ke baad Confirm dabao — tabhi attendance database mein lagegi.")

        with st.expander("📁 Per-image breakdown", expanded=False):
            for log in prev['per_image_log']:
                err = log.get('error')
                if err:
                    st.error(f"**{log['name']}** — Error: {err}")
                else:
                    names = [smap.get(i, f"#{i}") for i in log['detected']]
                    st.write(f"**{log['name']}** — {log['faces']} face(s) → {', '.join(names) if names else 'No match'}")

        st.markdown("#### ✏️ Attendance verify/edit karo")
        final_present = {}
        for s in students:
            sid = s['student_id']
            default_checked = sid in preview_present_ids
            final_present[sid] = st.checkbox(
                f"{s['name']}" + ("  ✅ (AI ne detect kiya)" if default_checked else "  — (AI ko nahi mila)"),
                value=default_checked,
                key=f"chk_preview_{sid}"
            )

        st.write("")
        cbtn1, cbtn2 = st.columns(2, gap="small")
        with cbtn1:
            if st.button("✅ Confirm & Attendance Lagao", type="primary", use_container_width=True):
                present_dict = {sid: True for sid, checked in final_present.items() if checked}
                try:
                    save_attendance(prev['subject_id'], present_dict, prev['all_student_ids'])
                    st.toast(f"✅ Attendance saved! Lecture #{prev['lecture_number']} - {prev['subject_name']}")
                except Exception as e:
                    st.warning(f"Save nahi hua: {e}")

                st.session_state['att_results'] = {
                    'present_ids': list(present_dict.keys()),
                    'all_students': students,
                    'student_map': smap,
                    'total_faces': prev['total_faces'],
                    'per_image_log': prev['per_image_log'],
                    'subject_name': prev['subject_name'],
                    'lecture_number': prev['lecture_number'],
                }
                st.session_state.pop('att_preview', None)
                st.rerun()
        with cbtn2:
            if st.button("🔄 Cancel / Dobara Photo Lo", type="secondary", use_container_width=True):
                st.session_state.pop('att_preview', None)
                st.rerun()

    # ── Results (final, saved) ──
    if 'att_results' in st.session_state:
        res = st.session_state['att_results']
        present_ids = set(res['present_ids'])
        students = res['all_students']
        smap = res['student_map']
        absent_ids = {s['student_id'] for s in students} - present_ids

        present_count = len(present_ids)
        absent_count = len(absent_ids)
        total_count = len(students)
        pct = int((present_count / total_count) * 100) if total_count else 0

        st.divider()
        st.markdown(f"### 📊 Result — {res.get('subject_name','')} | Lecture #{res.get('lecture_number','')}")

        st.markdown(f"""
        <div class="summary-box">
            <div><div class="sum-num" style="color:#22c55e">{present_count}</div><div class="sum-label">Present</div></div>
            <div><div class="sum-num" style="color:#ef4444">{absent_count}</div><div class="sum-label">Absent</div></div>
            <div><div class="sum-num" style="color:#7c6ff7">{total_count}</div><div class="sum-label">Total</div></div>
            <div><div class="sum-num" style="color:#f59e0b">{pct}%</div><div class="sum-label">Attendance</div></div>
        </div>
        """, unsafe_allow_html=True)

        if present_ids:
            st.markdown("#### ✅ Present")
            for sid in present_ids:
                name = smap.get(sid, f"Student #{sid}")
                st.markdown(f"""
                <div class="att-result-card att-present">
                    <span style="font-size:24px">🟢</span>
                    <span class="att-name">{name}</span>
                    <span class="att-badge-present">PRESENT</span>
                </div>
                """, unsafe_allow_html=True)

        if absent_ids:
            st.markdown("#### ❌ Absent")
            for sid in absent_ids:
                name = smap.get(sid, f"Student #{sid}")
                st.markdown(f"""
                <div class="att-result-card att-absent">
                    <span style="font-size:24px">🔴</span>
                    <span class="att-name">{name}</span>
                    <span class="att-badge-absent">ABSENT</span>
                </div>
                """, unsafe_allow_html=True)

        with st.expander("📁 Per-image breakdown"):
            for log in res['per_image_log']:
                err = log.get('error')
                if err:
                    st.error(f"**{log['name']}** — Error: {err}")
                else:
                    names = [smap.get(i, f"#{i}") for i in log['detected']]
                    st.write(f"**{log['name']}** — {log['faces']} face(s) → {', '.join(names) if names else 'No match'}")

        if st.button("🔄 Dobara Lo", type="secondary"):
            st.session_state.pop('att_results', None)
            st.rerun()


# ─────────────────────────────────────────
#  Login
# ─────────────────────────────────────────
def login_teacher(username, password):
    if not username or not password:
        return False
    teacher = teacher_login(username, password)
    if teacher:
        st.session_state.user_role = 'teacher'
        st.session_state.teacher_data = teacher
        st.session_state.is_logged_in = True
        return True
    return False


def teacher_login_page():
    if st.button("← Home", type="secondary", key='logintohome1'):
        st.session_state['login_type'] = None
        st.rerun()

    st.markdown("""
    <div class="auth-card">
        <div class="auth-icon">🔐</div>
        <div class="auth-title">Teacher Login</div>
        <div class="auth-subtitle">Sign in to your dashboard</div>
    </div>
    """, unsafe_allow_html=True)

    _, mid, _ = st.columns([1, 2, 1])
    with mid:
        teacher_username = st.text_input("Username", placeholder="your username")
        teacher_password = st.text_input("Password", placeholder="your password", type='password')
        st.write("")
        btn1, btn2 = st.columns(2, gap="small")
        with btn1:
            if st.button("Login", icon=':material/passkey:', type="primary", use_container_width=True):
                if login_teacher(teacher_username, teacher_password):
                    st.rerun()
                else:
                    st.error("Wrong username or password")
        with btn2:
            if st.button("Register", type="secondary", use_container_width=True):
                st.session_state['teacher_type'] = 'register'
                st.rerun()


# ─────────────────────────────────────────
#  Register
# ─────────────────────────────────────────
def register_teacher(teacher_name, teacher_username, teacher_password, teacher_confirm_password):
    if not all([teacher_name, teacher_username, teacher_password, teacher_confirm_password]):
        return False, "All fields are required"
    if check_techer_exist(teacher_username):
        return False, "Username already taken"
    if teacher_password != teacher_confirm_password:
        return False, "Passwords don't match"
    try:
        create_teacher(teacher_username, teacher_password, teacher_name)
        return True, "Account created! Please login."
    except Exception as e:
        return False, str(e)


def teacher_register_page():
    if st.button("← Back to Login", type="secondary", key='logintohome'):
        st.session_state['teacher_type'] = 'login'
        st.rerun()

    st.markdown("""
    <div class="auth-card">
        <div class="auth-icon">📝</div>
        <div class="auth-title">Create Account</div>
        <div class="auth-subtitle">Register as a teacher</div>
    </div>
    """, unsafe_allow_html=True)

    _, mid, _ = st.columns([1, 2, 1])
    with mid:
        teacher_name     = st.text_input("Full Name",        placeholder="e.g. Priya Sharma",  key='t_name')
        teacher_username = st.text_input("Username",         placeholder="e.g. priya123",       key='t_username')
        teacher_password = st.text_input("Password",         placeholder="min 6 characters",    type='password', key='t_password')
        teacher_confirm  = st.text_input("Confirm Password", placeholder="repeat password",      type='password', key='t_confirm')
        st.write("")
        btn1, btn2 = st.columns(2, gap="small")
        with btn1:
            if st.button("Create Account", type="primary", use_container_width=True):
                success, message = register_teacher(teacher_name, teacher_username, teacher_password, teacher_confirm)
                if success:
                    st.success(message)
                    time.sleep(1.5)
                    st.session_state.teacher_type = 'login'
                    st.rerun()
                else:
                    st.error(message)
        with btn2:
            if st.button("Login Instead", type="secondary", use_container_width=True):
                st.session_state.teacher_type = 'login'
                st.rerun()


# ─────────────────────────────────────────
#  Records Page
# ─────────────────────────────────────────
def records_page():
    from src.database.db import get_teacher_subjects, get_attendance_records
    import pandas as pd
    from datetime import date, timedelta

    teacher = st.session_state.teacher_data
    teacher_id = teacher['teacher_id']

    if st.button("← Back to Dashboard", type="secondary", key="rec_back"):
        st.session_state['teacher_page'] = 'home'
        st.rerun()

    st.markdown("## 📊 Attendance Records")
    st.markdown('<p class="section-label">Filter & view past attendance</p>', unsafe_allow_html=True)

    # fetch subjects
    subjects = get_teacher_subjects(teacher_id)
    if not subjects:
        st.warning("No subjects found. Add subjects first.")
        return

    subject_options = {"All Subjects": None}
    for s in subjects:
        label = f"{s['name']} ({s['subject_code']}) - {s['section']}"
        subject_options[label] = s['subject_id']

    # ── Filters ──
    col1, col2, col3 = st.columns(3)
    with col1:
        selected_subject_label = st.selectbox("Subject", list(subject_options.keys()))
        selected_subject_id = subject_options[selected_subject_label]
    with col2:
        date_from = st.date_input("From Date", value=date.today() - timedelta(days=30))
    with col3:
        date_to = st.date_input("To Date", value=date.today())

    st.write("")

    if st.button("🔍 Fetch Records", type="primary"):
        with st.spinner("Fetching records..."):
            records = get_attendance_records(
                teacher_id=teacher_id,
                subject_id=selected_subject_id,
                date_from=date_from.isoformat(),
                date_to=(date_to.isoformat() + "T23:59:59"),
            )

        if not records:
            st.info("No records found for the selected filters.")
            return

        # ── Build pivot table ──
        rows = []
        for r in records:
            student_name = r.get("students", {}).get("name", f"#{r['student_id']}") if r.get("students") else f"#{r['student_id']}"
            subject_name = ""
            if r.get("subjects"):
                subject_name = f"{r['subjects']['name']} ({r['subjects']['subject_code']})"
            ts = r.get("timestamp", "")
            date_str = ts[:10] if ts else "—"
            rows.append({
                "Date": date_str,
                "Subject": subject_name,
                "Student": student_name,
                "Status": "✅ Present" if r["is_present"] else "❌ Absent",
                "is_present": r["is_present"],
            })

        df = pd.DataFrame(rows)

        # ── Summary stats ──
        total = len(df)
        present = df["is_present"].sum()
        absent = total - present
        pct = int((present / total) * 100) if total else 0

        st.markdown(f"""
        <div class="summary-box">
            <div><div class="sum-num" style="color:#22c55e">{present}</div><div class="sum-label">Present</div></div>
            <div><div class="sum-num" style="color:#ef4444">{absent}</div><div class="sum-label">Absent</div></div>
            <div><div class="sum-num" style="color:#7c6ff7">{total}</div><div class="sum-label">Total Records</div></div>
            <div><div class="sum-num" style="color:#f59e0b">{pct}%</div><div class="sum-label">Avg Attendance</div></div>
        </div>
        """, unsafe_allow_html=True)

        # ── Pivot Table — Students as rows, Dates as columns ──
        st.markdown("#### 🗓️ Attendance Sheet")

        pivot = df.pivot_table(
            index="Student",
            columns="Date",
            values="is_present",
            aggfunc="max"
        )
        pivot = pivot.fillna(False)
        display_pivot = pivot.applymap(lambda x: "✅" if x else "❌")

        # add total column
        display_pivot["Total Present"] = pivot.sum(axis=1).astype(int)
        display_pivot["Total Days"] = pivot.shape[1]
        display_pivot["Attendance %"] = ((pivot.sum(axis=1) / pivot.shape[1]) * 100).round(1).astype(str) + "%"

        st.dataframe(
            display_pivot,
            use_container_width=True,
            height=min(400, (len(display_pivot) + 1) * 40),
        )

        # ── Per-subject breakdown ──
        if selected_subject_id is None and df["Subject"].nunique() > 1:
            st.markdown("#### 📚 Per Subject Summary")
            subject_summary = df.groupby("Subject")["is_present"].agg(
                Present="sum",
                Total="count"
            ).reset_index()
            subject_summary["Absent"] = subject_summary["Total"] - subject_summary["Present"]
            subject_summary["Attendance %"] = ((subject_summary["Present"] / subject_summary["Total"]) * 100).round(1).astype(str) + "%"
            st.dataframe(subject_summary[["Subject", "Present", "Absent", "Total", "Attendance %"]], use_container_width=True)

        # ── Download ──
        st.markdown("#### ⬇️ Download")
        csv = display_pivot.reset_index().to_csv(index=False).encode("utf-8")
        st.download_button(
            label="Download as CSV",
            data=csv,
            file_name=f"attendance_{date_from}_{date_to}.csv",
            mime="text/csv",
            type="secondary"
        )