import streamlit as st
import time

from src.ui.style_base import style_home, style_page, style_ui  
from src.components.header import header_dashbaord

from PIL import Image
import numpy as np

from src.database.db import (
    get_all_students, create_student,
    get_student_subjects, get_student_attendance_summary,
    get_student_recent_attendance, enroll_student_by_code
)

# ── Updated imports: predict_attendance (typo fix), no train_classifier ──
from src.pipelines.face_pipeline import predict_attendance, get_face_embeddings, get_registration_embedding
from src.pipelines.voice_pipeline import get_voice_embedding


def student_dashboard():
    from src.database.db import (
        get_student_subjects, get_student_attendance_summary,
        get_student_recent_attendance, enroll_student_by_code
    )

    student = st.session_state.student_data
    student_id = student["student_id"]
    student_name = student["name"]

    # ── Header ──
    col_h1, col_h2 = st.columns([3, 1])
    with col_h1:
        st.markdown(f"## 👋 Welcome, {student_name}!")
        st.caption(f"Student ID: #{student_id}")
    with col_h2:
        if st.button("🚪 Logout", type="secondary"):
            for key in ["student_data", "is_logged_in", "user_role"]:
                st.session_state.pop(key, None)
            st.rerun()

    st.divider()

    # ── Tabs ──
    tab1, tab2, tab3 = st.tabs(["📊 My Classes", "✅ Recent Attendance", "➕ Enroll in Class"])

    # ════════════════════════════════
    # Tab 1: Enrolled subjects + attendance %
    # ════════════════════════════════
    with tab1:
        summary = get_student_attendance_summary(student_id)
        enrolled = get_student_subjects(student_id)

        if not enrolled:
            st.info("Abhi kisi class mein enrolled nahi ho.")
            st.caption("'Enroll in Class' tab se join karo.")
        else:
            att_map = {s["subject_id"]: s for s in summary}

            st.markdown(f"**{len(enrolled)} class(es) enrolled**")
            st.write("")

            for subj in enrolled:
                sid = subj["subject_id"]
                att = att_map.get(sid, {"total": 0, "present": 0})
                total = att["total"]
                present = att["present"]
                pct = int((present / total) * 100) if total > 0 else None

                teacher_info = subj.get("teachers") or {}
                teacher_name = teacher_info.get("name", "Unknown")

                with st.container(border=True):
                    c1, c2 = st.columns([3, 1])
                    with c1:
                        st.markdown(f"#### 📚 {subj['name']}")
                        st.caption(f"Code: `{subj['subject_code']}` | Section: {subj['section']} | Teacher: {teacher_name}")
                        if total > 0:
                            st.progress(present / total, text=f"{present}/{total} classes attended")
                        else:
                            st.caption("Abhi koi attendance record nahi")
                    with c2:
                        if pct is not None:
                            color = "#22c55e" if pct >= 75 else "#f59e0b" if pct >= 50 else "#ef4444"
                            st.markdown(f"""
                            <div style="text-align:center; padding:16px; background:{color}22;
                                border-radius:12px; border: 1.5px solid {color}">
                                <div style="font-size:28px; font-weight:700; color:{color}">{pct}%</div>
                                <div style="font-size:12px; color:{color}">Attendance</div>
                            </div>
                            """, unsafe_allow_html=True)
                        else:
                            st.markdown("""
                            <div style="text-align:center; padding:16px; background:#ffffff11;
                                border-radius:12px;">
                                <div style="font-size:20px">—</div>
                                <div style="font-size:12px; opacity:0.5">No data</div>
                            </div>
                            """, unsafe_allow_html=True)

    # ════════════════════════════════
    # Tab 2: Recent attendance log
    # ════════════════════════════════
    with tab2:
        recent = get_student_recent_attendance(student_id, limit=20)
        if not recent:
            st.info("Koi attendance record nahi mila abhi tak.")
        else:
            for log in recent:
                subj = log.get("subjects") or {}
                subj_name = subj.get("name", "Unknown")
                subj_code = subj.get("subject_code", "")
                is_present = log["is_present"]
                ts = log["timestamp"]

                try:
                    from datetime import datetime, timezone
                    dt = datetime.fromisoformat(ts).astimezone(timezone.utc)
                    ts_str = dt.strftime("%d %b %Y, %I:%M %p")
                except Exception:
                    ts_str = ts

                icon = "🟢" if is_present else "🔴"
                badge_color = "#22c55e" if is_present else "#ef4444"
                badge_text = "PRESENT" if is_present else "ABSENT"

                st.markdown(f"""
                <div style="display:flex; align-items:center; gap:14px; padding:12px 16px;
                    margin-bottom:8px; border-radius:10px; background:#ffffff08;
                    border-left: 4px solid {badge_color}">
                    <span style="font-size:22px">{icon}</span>
                    <div style="flex:1">
                        <div style="font-weight:600">{subj_name} <span style="opacity:0.5; font-size:12px">({subj_code})</span></div>
                        <div style="font-size:12px; opacity:0.55">{ts_str}</div>
                    </div>
                    <span style="font-size:11px; font-weight:700; color:{badge_color};
                        border:1.5px solid {badge_color}; border-radius:6px; padding:2px 8px">{badge_text}</span>
                </div>
                """, unsafe_allow_html=True)

    # ════════════════════════════════
    # Tab 3: Enroll by code
    # ════════════════════════════════
    with tab3:
        st.markdown("### 🔑 Join a Class")
        st.caption("Teacher se subject code lo aur yahan enter karo")

        with st.container(border=True):
            code_input = st.text_input(
                "Subject Code",
                placeholder="e.g. MATH101",
                max_chars=20
            ).strip().upper()

            if st.button("Enroll Now →", type="primary", use_container_width=True):
                if code_input:
                    with st.spinner("Joining class..."):
                        subject, error = enroll_student_by_code(student_id, code_input)
                    if error:
                        st.error(f"❌ {error}")
                    else:
                        st.success(f"✅ Successfully joined **{subject['name']}** ({subject['subject_code']})")
                        st.balloons()
                        time.sleep(1)
                        st.rerun()
                else:
                    st.warning("Subject code daalo pehle")

        st.divider()
        st.caption("💡 QR code bhi scan kar sakte ho — teacher ke phone se link ya QR lo")


def student_screen():

    style_page()
    style_ui()

    if 'student_data' in st.session_state:
        student_dashboard()
        return

    col1, col2 = st.columns(2, gap="large", vertical_alignment='center')
    with col1:
        header_dashbaord()
    with col2:
        if st.button("← Home", type="secondary", key='logintohome1'):
            st.session_state['login_type'] = None
            st.rerun()

    st.header("Login using Face ID")
    st.write("")
    photo = st.camera_input("Position your face at center")

    show_registration = False

    if photo:
        image = np.array(Image.open(photo))

        with st.spinner("AI is Scanning..."):
            # ── predict_attendance (fixed typo, new pipeline) ──
            detected, all_ids, num_faces = predict_attendance(image)

            if num_faces == 0:
                st.warning("Face not found. Camera ke saamne seedha baitho aur light achhi rakho.")
            elif num_faces > 1:
                st.warning("Multiple faces found. Akele login karo.")
            else:
                if detected:
                    student_id = list(detected.keys())[0]
                    confidence = detected[student_id]

                    all_student = get_all_students()
                    student = next((s for s in all_student if s['student_id'] == student_id), None)

                    if student:
                        st.session_state.is_logged_in = True
                        st.session_state.user_role = 'student'
                        st.session_state.student_data = student
                        st.toast(f"Welcome back, {student['name']}! (confidence: {confidence:.0%})")
                        time.sleep(1)
                        st.rerun()
                else:
                    st.info("Face not recognized. Naya student ho? Neeche register karo.")
                    show_registration = True

    if show_registration:
        with st.container(border=True):
            st.header("Create your Profile")
            new_name = st.text_input("Enter your name", placeholder="Eg. Alex Joe")

            st.subheader("Optional: Voice Enrollment")
            st.info("Voice enrollment se voice-only attendance bhi de sakte ho")

            audio_data = None
            try:
                audio_data = st.audio_input("Record a short sentence — e.g. 'I am present today'")
            except Exception:
                st.warning("Audio recording supported nahi hai is device pe")

            if st.button("Create Student Account", type='primary'):
                if not new_name:
                    st.warning("Pehle apna naam daalo")
                else:
                    with st.spinner("Profile ban raha hai..."):
                        img = np.array(Image.open(photo))

                        # ── get_registration_embedding: ensures exactly 1 face ──
                        face_emb_arr = get_registration_embedding(img)

                        if face_emb_arr is None:
                            # get_registration_embedding already shows st.warning
                            st.error("Face capture nahi hua. Dobara photo lo.")
                        else:
                            face_emb = face_emb_arr.tolist()

                            voice_emb = None
                            if audio_data:
                                voice_emb = get_voice_embedding(audio_data.read())

                            response_data = create_student(
                                new_name,
                                face_embedding=face_emb,
                                voice_embedding=voice_emb,
                            )

                            if response_data:
                                # ── No train_classifier() needed — InsightFace is instant ──
                                st.session_state.is_logged_in = True
                                st.session_state.user_role = 'student'
                                st.session_state.student_data = response_data[0]
                                st.toast(f"Profile ban gaya! Welcome, {new_name} 🎉")
                                time.sleep(1)
                                st.rerun()
                            else:
                                st.error("DB mein save nahi hua. Admin se baat karo.")