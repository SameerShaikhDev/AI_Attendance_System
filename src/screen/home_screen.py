import streamlit as st
from src.ui.style_base import style_home, style_ui

def home_screen():
    style_ui()
    style_home()

    # Chalk tray top decoration
    st.markdown("""
    <div style="background:#5a4a2a;height:16px;border-radius:4px 4px 0 0;display:flex;align-items:center;padding:0 16px;gap:8px;margin-bottom:0;">
        <div style="width:28px;height:7px;background:#f0e6d0;border-radius:3px;opacity:0.8;"></div>
        <div style="width:20px;height:7px;background:#ffd96a;border-radius:3px;opacity:0.8;"></div>
        <div style="width:24px;height:7px;background:#ffb4c8;border-radius:3px;opacity:0.8;"></div>
        <div style="width:18px;height:7px;background:#90c8ff;border-radius:3px;opacity:0.8;"></div>
    </div>
    <div style="background:#2d4a2d;border:3px solid #5a7a5a;border-radius:0 0 16px 16px;padding:28px 24px 24px;margin-bottom:24px;position:relative;">
        <div style="position:absolute;inset:6px;border:1px dashed rgba(240,230,208,0.08);border-radius:10px;pointer-events:none;"></div>
        <div style="text-align:center;">
            <div style="font-family:'Fredoka One',cursive;font-size:2.4rem;color:#f0e6d0;letter-spacing:1px;margin-bottom:4px;">
                🎓 Smart Attendance
            </div>
            <div style="font-size:0.9rem;color:#8fbc8f;letter-spacing:1px;">
                Face & Voice Recognition System
            </div>
            <div style="display:flex;justify-content:center;gap:10px;margin-top:12px;flex-wrap:wrap;">
                <span style="background:rgba(255,255,255,0.07);border:1px solid rgba(240,230,208,0.18);border-radius:20px;padding:4px 12px;font-size:0.75rem;color:#b8d4b8;">🧠 AI Powered</span>
                <span style="background:rgba(255,255,255,0.07);border:1px solid rgba(240,230,208,0.18);border-radius:20px;padding:4px 12px;font-size:0.75rem;color:#b8d4b8;">📷 Face ID</span>
                <span style="background:rgba(255,255,255,0.07);border:1px solid rgba(240,230,208,0.18);border-radius:20px;padding:4px 12px;font-size:0.75rem;color:#b8d4b8;">🎙️ Voice ID</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<p style="text-align:center;font-family:Fredoka One,cursive;color:rgba(240,230,208,0.4);font-size:0.85rem;letter-spacing:3px;text-transform:uppercase;margin-bottom:16px;">Choose Your Role</p>', unsafe_allow_html=True)

    col1, col2 = st.columns(2, gap="large")

    with col1:
        st.markdown("""
        <div style="text-align:center;padding:8px 0;">
            <div style="font-size:72px;filter:drop-shadow(2px 3px 0 rgba(0,0,0,0.4));line-height:1;margin-bottom:10px;">🧑‍🎓</div>
            <div style="font-family:'Fredoka One',cursive;font-size:1.4rem;color:#f0e6d0;">I'm a Student</div>
            <div style="font-size:0.8rem;color:#8fbc8f;margin-top:4px;">Mark your attendance</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Go to Student Portal →", type="primary", use_container_width=True):
            st.session_state['login_type'] = 'student'
            st.rerun()

    with col2:
        st.markdown("""
        <div style="text-align:center;padding:8px 0;">
            <div style="font-size:72px;filter:drop-shadow(2px 3px 0 rgba(0,0,0,0.4));line-height:1;margin-bottom:10px;">👩‍🏫</div>
            <div style="font-family:'Fredoka One',cursive;font-size:1.4rem;color:#f0e6d0;">I'm a Teacher</div>
            <div style="font-size:0.8rem;color:#8fbc8f;margin-top:4px;">Manage your class</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Go to Teacher Portal →", type="secondary", use_container_width=True):
            st.session_state['login_type'] = 'teacher'
            st.rerun()

    st.markdown("""
    <div style="display:flex;gap:10px;margin-top:24px;flex-wrap:wrap;">
        <div style="flex:1;min-width:120px;background:rgba(45,74,45,0.7);border:1.5px solid #4a6a4a;border-radius:10px;padding:10px 8px;text-align:center;">
            <div style="font-size:22px;">📊</div>
            <div style="font-size:0.72rem;color:#8fbc8f;margin-top:4px;font-weight:700;text-transform:uppercase;letter-spacing:1px;">Reports</div>
        </div>
        <div style="flex:1;min-width:120px;background:rgba(45,74,45,0.7);border:1.5px solid #4a6a4a;border-radius:10px;padding:10px 8px;text-align:center;">
            <div style="font-size:22px;">🔒</div>
            <div style="font-size:0.72rem;color:#8fbc8f;margin-top:4px;font-weight:700;text-transform:uppercase;letter-spacing:1px;">Secure</div>
        </div>
        <div style="flex:1;min-width:120px;background:rgba(45,74,45,0.7);border:1.5px solid #4a6a4a;border-radius:10px;padding:10px 8px;text-align:center;">
            <div style="font-size:22px;">⚡</div>
            <div style="font-size:0.72rem;color:#8fbc8f;margin-top:4px;font-weight:700;text-transform:uppercase;letter-spacing:1px;">Real-time</div>
        </div>
        <div style="flex:1;min-width:120px;background:rgba(45,74,45,0.7);border:1.5px solid #4a6a4a;border-radius:10px;padding:10px 8px;text-align:center;">
            <div style="font-size:22px;">🧠</div>
            <div style="font-size:0.72rem;color:#8fbc8f;margin-top:4px;font-weight:700;text-transform:uppercase;letter-spacing:1px;">AI Model</div>
        </div>
    </div>
    <div style="background:rgba(232,160,32,0.12);border-left:3px solid #e8a020;border-radius:0 8px 8px 0;padding:8px 14px;margin-top:16px;">
        <div style="font-size:0.82rem;color:#f0c060;">📌 New students: Register with Face ID on your first visit!</div>
    </div>
    """, unsafe_allow_html=True)