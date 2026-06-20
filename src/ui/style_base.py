import streamlit as st

_BASE = """
@import url('https://fonts.googleapis.com/css2?family=Fredoka+One&family=Nunito:wght@400;600;700;800&display=swap');

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body, .stApp {
    font-family: 'Nunito', sans-serif !important;
    background: #1a2a1a !important;
    color: #f0e6d0 !important;
}

#MainMenu, header, footer { visibility: hidden !important; }
[data-testid="stToolbar"] { display: none !important; }

.block-container {
    padding-top: 2rem !important;
    padding-bottom: 3rem !important;
    max-width: 1100px !important;
}

/* ══ TYPOGRAPHY ══ */
h1, h2, h3,
[data-testid="stMarkdownContainer"] h1,
[data-testid="stMarkdownContainer"] h2,
[data-testid="stMarkdownContainer"] h3 {
    font-family: 'Fredoka One', cursive !important;
    color: #f0e6d0 !important;
    letter-spacing: 0.5px !important;
}

h1, [data-testid="stMarkdownContainer"] h1 { font-size: 2.2rem !important; }
h2, [data-testid="stMarkdownContainer"] h2 { font-size: 1.6rem !important; }
h3, [data-testid="stMarkdownContainer"] h3 { font-size: 1.2rem !important; }

p, span, label,
[data-testid="stMarkdownContainer"] p {
    font-family: 'Nunito', sans-serif !important;
    color: #b8d4b8 !important;
    font-size: 0.95rem !important;
    line-height: 1.6 !important;
}

/* ══ INPUTS ══ */
.stTextInput label,
.stSelectbox label,
.stTextArea label,
.stFileUploader label,
.stCheckbox label {
    font-family: 'Nunito', sans-serif !important;
    font-size: 0.85rem !important;
    font-weight: 700 !important;
    color: #b8d4b8 !important;
    letter-spacing: 0.03em !important;
}

.stTextInput input,
.stSelectbox select,
.stTextArea textarea {
    background: rgba(240,230,208,0.08) !important;
    border: 2px solid rgba(240,230,208,0.2) !important;
    border-radius: 10px !important;
    color: #f0e6d0 !important;
    font-family: 'Nunito', sans-serif !important;
    font-size: 0.95rem !important;
    padding: 10px 14px !important;
    transition: border-color 0.2s !important;
}

.stTextInput input:focus,
.stTextArea textarea:focus {
    border-color: #8fbc8f !important;
    box-shadow: 0 0 0 3px rgba(143,188,143,0.2) !important;
    outline: none !important;
}

.stTextInput input::placeholder,
.stTextArea textarea::placeholder {
    color: rgba(240,230,208,0.3) !important;
}

/* ══ BUTTONS ══ */
.stButton > button[kind="primary"] {
    font-family: 'Fredoka One', cursive !important;
    font-size: 1rem !important;
    background: #e8a020 !important;
    color: #1a1000 !important;
    border: 2px solid #c87800 !important;
    border-radius: 20px !important;
    padding: 10px 24px !important;
    transition: all 0.2s !important;
    letter-spacing: 0.5px !important;
}
.stButton > button[kind="primary"]:hover {
    background: #f0b030 !important;
    transform: translateY(-2px) !important;
}

.stButton > button[kind="secondary"] {
    font-family: 'Nunito', sans-serif !important;
    font-weight: 700 !important;
    font-size: 0.9rem !important;
    background: rgba(240,230,208,0.07) !important;
    color: #b8d4b8 !important;
    border: 1.5px solid rgba(240,230,208,0.2) !important;
    border-radius: 20px !important;
    padding: 10px 22px !important;
    transition: all 0.2s !important;
}
.stButton > button[kind="secondary"]:hover {
    background: rgba(240,230,208,0.14) !important;
    border-color: rgba(240,230,208,0.4) !important;
    color: #f0e6d0 !important;
}

/* ══ ALERTS ══ */
.stAlert {
    border-radius: 12px !important;
    font-family: 'Nunito', sans-serif !important;
    font-size: 0.9rem !important;
}

/* ══ SELECTBOX ══ */
[data-testid="stSelectbox"] > div > div {
    background: rgba(240,230,208,0.08) !important;
    border: 2px solid rgba(240,230,208,0.2) !important;
    border-radius: 10px !important;
    color: #f0e6d0 !important;
}

/* ══ FILE UPLOADER ══ */
[data-testid="stFileUploader"] {
    background: rgba(240,230,208,0.05) !important;
    border: 2px dashed rgba(240,230,208,0.2) !important;
    border-radius: 12px !important;
    padding: 12px !important;
}

/* ══ PROGRESS BAR ══ */
[data-testid="stProgressBar"] > div > div {
    background: #e8a020 !important;
}

/* ══ DATAFRAME ══ */
[data-testid="stDataFrame"] {
    border: 1.5px solid rgba(143,188,143,0.3) !important;
    border-radius: 12px !important;
    overflow: hidden !important;
}

/* ══ DIVIDER ══ */
hr {
    border: none !important;
    border-top: 1px dashed rgba(240,230,208,0.15) !important;
    margin: 1.5rem 0 !important;
}

/* ══ TOAST ══ */
[data-testid="stToast"] {
    background: #2d4a2d !important;
    border: 1.5px solid #4a6a4a !important;
    border-radius: 12px !important;
    color: #f0e6d0 !important;
    font-family: 'Nunito', sans-serif !important;
}

/* ══ SCROLLBAR ══ */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: #1a2a1a; }
::-webkit-scrollbar-thumb { background: #4a6a4a; border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: #8fbc8f; }

/* ══ SPINNER ══ */
[data-testid="stSpinner"] { color: #8fbc8f !important; }

/* ══ EXPANDER ══ */
[data-testid="stExpander"] {
    background: rgba(240,230,208,0.04) !important;
    border: 1.5px solid rgba(240,230,208,0.12) !important;
    border-radius: 12px !important;
}
[data-testid="stExpander"] summary {
    color: #b8d4b8 !important;
    font-family: 'Nunito', sans-serif !important;
    font-weight: 700 !important;
}

/* ══ CHECKBOX ══ */
[data-testid="stCheckbox"] label {
    color: #b8d4b8 !important;
    font-family: 'Nunito', sans-serif !important;
}

/* ══ CAMERA INPUT ══ */
[data-testid="stCameraInput"] {
    border: 2px dashed rgba(240,230,208,0.2) !important;
    border-radius: 12px !important;
}

/* ══ UTILITY CLASSES ══ */

/* Blackboard card */
.bb-card {
    background: #2d4a2d;
    border: 2px solid #4a6a4a;
    border-radius: 16px;
    padding: 24px 20px;
    margin-bottom: 16px;
    position: relative;
}
.bb-card::before {
    content: '';
    position: absolute;
    inset: 4px;
    border: 1px dashed rgba(240,230,208,0.08);
    border-radius: 12px;
    pointer-events: none;
}

/* Chalk title */
.chalk-title {
    font-family: 'Fredoka One', cursive;
    color: #f0e6d0;
    font-size: 1.8rem;
    text-align: center;
    letter-spacing: 1px;
}

/* Section label */
.bb-label {
    font-family: 'Nunito', sans-serif;
    font-size: 0.72rem;
    font-weight: 800;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: rgba(240,230,208,0.35);
    margin-bottom: 12px;
}

/* Stat chip */
.bb-stat {
    background: rgba(45,74,45,0.8);
    border: 1.5px solid #4a6a4a;
    border-radius: 14px;
    padding: 16px 20px;
    text-align: center;
}
.bb-stat-num {
    font-family: 'Fredoka One', cursive;
    font-size: 2rem;
    color: #e8a020;
    line-height: 1;
}
.bb-stat-label {
    font-size: 0.72rem;
    font-weight: 700;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: rgba(240,230,208,0.4);
    margin-top: 4px;
}

/* Chalk tray decoration */
.chalk-tray {
    background: #5a4a2a;
    height: 16px;
    border-radius: 0 0 4px 4px;
    display: flex;
    align-items: center;
    padding: 0 16px;
    gap: 8px;
    margin-bottom: 16px;
}

/* Result cards */
.bb-present {
    background: rgba(34,197,94,0.12);
    border: 1.5px solid rgba(34,197,94,0.3);
    border-radius: 12px;
    padding: 12px 16px;
    margin-bottom: 8px;
    display: flex;
    align-items: center;
    gap: 12px;
    color: #f0e6d0;
    font-family: 'Nunito', sans-serif;
    font-weight: 700;
}
.bb-absent {
    background: rgba(239,68,68,0.1);
    border: 1.5px solid rgba(239,68,68,0.25);
    border-radius: 12px;
    padding: 12px 16px;
    margin-bottom: 8px;
    display: flex;
    align-items: center;
    gap: 12px;
    color: #f0e6d0;
    font-family: 'Nunito', sans-serif;
    font-weight: 700;
}

/* Summary box */
.bb-summary {
    background: rgba(45,74,45,0.6);
    border: 1.5px solid #4a6a4a;
    border-radius: 14px;
    padding: 16px 20px;
    margin-bottom: 20px;
    display: flex;
    gap: 28px;
    align-items: center;
    flex-wrap: wrap;
}
.bb-sum-num { font-family: 'Fredoka One', cursive; font-size: 2rem; }
.bb-sum-label { font-size: 0.75rem; color: rgba(240,230,208,0.45); margin-top: 2px; font-weight: 700; text-transform: uppercase; letter-spacing: 1px; }
"""


def style_ui():
    st.markdown(f"<style>{_BASE}</style>", unsafe_allow_html=True)


def style_page():
    pass


def style_home():
    st.markdown("""
    <style>
        .stApp { background: #1a2a1a !important; }
        [data-testid="stColumn"] > div {
            background: #2d4a2d;
            border: 2px solid #4a6a4a;
            border-radius: 16px;
            padding: 1.5rem !important;
            transition: border-color 0.2s;
        }
        [data-testid="stColumn"] > div:hover {
            border-color: #8fbc8f;
        }
    </style>
    """, unsafe_allow_html=True)