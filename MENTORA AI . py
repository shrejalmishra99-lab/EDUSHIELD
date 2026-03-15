# -*- coding: utf-8 -*-
import streamlit as st
from groq import Groq
import pandas as pd
import json
import re
import os
import csv
from datetime import datetime, date as dt_date
from io import BytesIO

# PDF generation
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER

# ─────────────────────────────────────────────
# 1. PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="MENTORA AI",
    layout="wide",
    page_icon="🎓",
    initial_sidebar_state="auto"
)

# ─────────────────────────────────────────────
# 2. CUSTOM CSS
# ─────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@700;900&family=Poppins:wght@300;400;500;600;700&family=Inter:wght@400;500;600&display=swap');

    /* ══ HIDE STREAMLIT CHROME ══ */
    [data-testid="collapsedControl"],
    [data-testid="stSidebarCollapseButton"] { display: none !important; }
    header[data-testid="stHeader"] { height: 0 !important; overflow: hidden !important; }
    #MainMenu, footer { visibility: hidden !important; }

    /* ══ PAGE BACKGROUND ══ */
    .stApp {
        background: #f8f7ff !important;
        font-family: 'Poppins', sans-serif !important;
    }
    .main .block-container { padding-top: 1rem !important; max-width: 1200px !important; }

    /* ══ GLOBAL TEXT — ALWAYS DARK ON LIGHT BG ══ */
    .stApp, .stApp * {
        color: #1a1a2e !important;
    }
    /* Override only where white text is needed (handled inline) */

    /* ══ HEADINGS ══ */
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Poppins', sans-serif !important;
        font-weight: 700 !important;
        color: #3b0764 !important;
    }

    /* ══ INPUTS — white bg, dark text ══ */
    .stTextInput > div > div > input,
    .stNumberInput > div > div > input,
    .stTextArea > div > div > textarea,
    .stDateInput > div > div > input {
        background: #ffffff !important;
        color: #1a1a2e !important;
        border: 2px solid #7c3aed !important;
        border-radius: 10px !important;
        font-family: 'Inter', sans-serif !important;
        font-size: 0.92rem !important;
        padding: 10px 14px !important;
    }
    .stTextInput > div > div > input:focus,
    .stNumberInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: #4f46e5 !important;
        box-shadow: 0 0 0 3px rgba(124,58,237,0.18) !important;
        outline: none !important;
    }
    /* Placeholder text */
    .stTextInput > div > div > input::placeholder,
    .stTextArea > div > div > textarea::placeholder { color: #9ca3af !important; }

    /* ══ SELECTBOX ══ */
    .stSelectbox > div > div,
    [data-baseweb="select"] > div {
        background: #ffffff !important;
        color: #1a1a2e !important;
        border: 2px solid #7c3aed !important;
        border-radius: 10px !important;
    }
    [data-baseweb="popover"] li,
    [role="option"] {
        background: #ffffff !important;
        color: #1a1a2e !important;
    }
    [role="option"]:hover { background: #f5f3ff !important; }

    /* ══ LABELS ══ */
    .stTextInput label, .stTextArea label, .stNumberInput label,
    .stSelectbox label, .stSlider label, .stRadio label,
    .stDateInput label, .stCheckbox label, .stMultiSelect label {
        color: #4c1d95 !important;
        font-weight: 600 !important;
        font-size: 0.87rem !important;
    }

    /* ══ RADIO & CHECKBOX ══ */
    .stRadio > div > label { color: #1a1a2e !important; }
    .stRadio > div > label > div > p { color: #1a1a2e !important; }
    .stCheckbox > label > div > p { color: #1a1a2e !important; }

    /* ══ BUTTONS — purple, white text ══ */
    .stButton > button {
        background: linear-gradient(135deg, #7c3aed, #4f46e5) !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 12px !important;
        font-weight: 700 !important;
        font-size: 0.88rem !important;
        padding: 0.5rem 1.4rem !important;
        transition: all 0.25s ease !important;
        box-shadow: 0 4px 12px rgba(124,58,237,0.3) !important;
    }
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 24px rgba(124,58,237,0.45) !important;
        background: linear-gradient(135deg, #6d28d9, #4338ca) !important;
    }
    .stButton > button p,
    .stButton > button span,
    .stButton > button div { color: #ffffff !important; }

    /* Form submit */
    .stFormSubmitButton > button {
        background: linear-gradient(135deg, #059669, #047857) !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 12px !important;
        font-weight: 700 !important;
        padding: 0.5rem 1.4rem !important;
        box-shadow: 0 4px 12px rgba(5,150,105,0.3) !important;
    }
    .stFormSubmitButton > button p,
    .stFormSubmitButton > button span { color: #ffffff !important; }
    .stFormSubmitButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 20px rgba(5,150,105,0.45) !important;
    }

    /* ══ TABS ══ */
    .stTabs [data-baseweb="tab-list"] {
        background: #ede9fe !important;
        border-radius: 12px !important;
        padding: 4px !important;
        gap: 4px !important;
    }
    .stTabs [data-baseweb="tab"] {
        color: #4c1d95 !important;
        font-weight: 600 !important;
        font-size: 0.82rem !important;
        border-radius: 8px !important;
        padding: 6px 14px !important;
        background: transparent !important;
    }
    .stTabs [aria-selected="true"] {
        background: #7c3aed !important;
        color: #ffffff !important;
        font-weight: 700 !important;
    }
    .stTabs [aria-selected="true"] * { color: #ffffff !important; }

    /* ══ SIDEBAR ══ */
    [data-testid="stSidebar"] {
        background: #ffffff !important;
        border-right: 2px solid #ede9fe !important;
        box-shadow: 2px 0 12px rgba(124,58,237,0.08) !important;
    }
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] span,
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] div { color: #1a1a2e !important; }
    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3 { color: #3b0764 !important; }
    [data-testid="stSidebar"] .stTextInput > div > div > input,
    [data-testid="stSidebar"] .stNumberInput > div > div > input {
        background: #f5f3ff !important;
        color: #1a1a2e !important;
        border: 1.5px solid #7c3aed !important;
        border-radius: 10px !important;
    }
    [data-testid="stSidebar"] .stSelectbox > div > div {
        background: #f5f3ff !important;
        border: 1.5px solid #7c3aed !important;
        border-radius: 10px !important;
    }

    /* ══ EXPANDER (used only for PYQ Solutions now) ══ */
    [data-testid="stExpander"] {
        border: 1.5px solid #ddd6fe !important;
        border-radius: 12px !important;
        background: #ffffff !important;
        margin-bottom: 8px !important;
    }
    [data-testid="stExpander"] details summary {
        background: #f5f3ff !important;
        border-radius: 10px !important;
        padding: 12px 16px !important;
        font-weight: 600 !important;
    }
    [data-testid="stExpander"] details summary:hover { background: #ede9fe !important; }
    [data-testid="stExpander"] details summary p,
    [data-testid="stExpander"] details summary span { color: #4c1d95 !important; font-weight: 600 !important; }
    /* Hide the raw text arrow node completely, show only SVG */
    [data-testid="stExpanderToggleIcon"] {
        display: none !important;
        visibility: hidden !important;
        width: 0 !important;
        height: 0 !important;
        overflow: hidden !important;
        font-size: 0 !important;
        color: transparent !important;
    }

    /* ══ ALERTS ══ */
    .stAlert { border-radius: 12px !important; }
    .stAlert p, .stAlert div, .stAlert span { color: #1a1a2e !important; }
    /* Info */
    [data-testid="stNotification"][kind="info"] { background: #eff6ff !important; border-left: 4px solid #3b82f6 !important; }
    /* Success */
    [data-testid="stNotification"][kind="success"] { background: #f0fdf4 !important; border-left: 4px solid #22c55e !important; }
    /* Warning */
    [data-testid="stNotification"][kind="warning"] { background: #fffbeb !important; border-left: 4px solid #f59e0b !important; }
    /* Error */
    [data-testid="stNotification"][kind="error"] { background: #fef2f2 !important; border-left: 4px solid #ef4444 !important; }

    /* ══ DATAFRAME ══ */
    .stDataFrame { border-radius: 12px !important; overflow: hidden !important; }
    .stDataFrame td, .stDataFrame th { color: #1a1a2e !important; }

    /* ══ METRICS (st.metric) ══ */
    [data-testid="stMetric"] {
        background: #ffffff !important;
        border: 2px solid #c4b5fd !important;
        border-radius: 14px !important;
        padding: 16px !important;
    }
    [data-testid="stMetricValue"] { color: #7c3aed !important; font-weight: 700 !important; }
    [data-testid="stMetricLabel"] { color: #4c1d95 !important; }
    [data-testid="stMetricDelta"] { color: #059669 !important; }

    /* ══ CHAT BUBBLES ══ */
    .chat-user {
        background: linear-gradient(135deg, #ede9fe, #ddd6fe) !important;
        border-radius: 18px 18px 4px 18px !important;
        padding: 12px 18px !important;
        margin: 8px 0 4px 30px !important;
        border-left: 4px solid #7c3aed !important;
        font-size: 0.9rem !important;
    }
    .chat-ai {
        background: linear-gradient(135deg, #f0fdf4, #dcfce7) !important;
        border-radius: 18px 18px 18px 4px !important;
        padding: 12px 18px !important;
        margin: 4px 30px 8px 0 !important;
        border-left: 4px solid #16a34a !important;
        font-size: 0.9rem !important;
    }
    .chat-user *, .chat-ai * { color: #1a1a2e !important; }

    /* ══ CUSTOM CARDS ══ */
    .metric-card {
        background: #ffffff !important;
        border: 2px solid #c4b5fd !important;
        border-radius: 18px !important;
        padding: 22px !important;
        text-align: center !important;
        box-shadow: 0 4px 16px rgba(124,58,237,0.1) !important;
        margin-bottom: 10px !important;
    }
    .metric-card h2 { color: #7c3aed !important; font-size: 1.8rem !important; margin: 0 !important; font-family: 'Orbitron', sans-serif !important; }
    .metric-card p  { color: #4c1d95 !important; margin: 6px 0 0 0 !important; font-size: 0.85rem !important; font-weight: 500 !important; }
    .badge-green  { background: linear-gradient(135deg,#16a34a,#15803d); color: #fff !important; border-radius: 8px; padding: 5px 14px; font-weight: 700; display:inline-block; }
    .badge-orange { background: linear-gradient(135deg,#d97706,#b45309); color: #fff !important; border-radius: 8px; padding: 5px 14px; font-weight: 700; display:inline-block; }
    .badge-red    { background: linear-gradient(135deg,#dc2626,#b91c1c); color: #fff !important; border-radius: 8px; padding: 5px 14px; font-weight: 700; display:inline-block; }

    /* ══ PHASE HEADER & BRANDING ══ */
    .phase-header { background: linear-gradient(90deg,#7c3aed,#4f46e5,#0ea5e9); border-radius: 14px; padding: 16px 24px; margin-bottom: 20px; color: #ffffff !important; font-size: 1.2rem; font-weight: 700; box-shadow: 0 6px 20px rgba(124,58,237,0.3); }
    .phase-header * { color: #ffffff !important; }
    .mentora-logo { font-family: 'Orbitron', sans-serif !important; font-size: 2.8rem; font-weight: 900; background: linear-gradient(135deg,#7c3aed,#4f46e5,#06b6d4); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; letter-spacing: 3px; text-align: center; display: block; padding: 10px 0 0 0; }
    .mentora-tagline { font-size: 0.85rem; color: #7c3aed !important; text-align: center; letter-spacing: 4px; text-transform: uppercase; display: block; margin-top: -4px; }
    .mentora-divider { height: 3px; background: linear-gradient(90deg,transparent,#7c3aed,#4f46e5,#06b6d4,transparent); border: none; border-radius: 2px; margin: 8px auto 16px auto; width: 80%; }
    .login-logo { font-family: 'Orbitron', sans-serif !important; font-size: 2.4rem; font-weight: 900; background: linear-gradient(135deg,#7c3aed,#4f46e5,#06b6d4); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; letter-spacing: 3px; text-align: center; display: block; margin-bottom: 4px; }
    .login-tagline { font-size: 0.78rem; color: #7c3aed !important; letter-spacing: 3px; text-transform: uppercase; text-align: center; display: block; margin-bottom: 4px; }
    .login-divider { height: 3px; background: linear-gradient(90deg,transparent,#7c3aed,#06b6d4,transparent); border: none; border-radius: 2px; margin: 8px auto 28px auto; width: 55%; }
    .login-card { background: #ffffff; border: 2px solid #c4b5fd; border-radius: 24px; padding: 32px 30px 26px 30px; box-shadow: 0 12px 40px rgba(124,58,237,0.15); }
    .login-card-title { font-size: 1.2rem; font-weight: 700; color: #4c1d95; text-align: center; margin: 0 0 6px 0; }
    .login-card-sub { font-size: 0.78rem; color: #6b7280; text-align: center; margin: 0 0 22px 0; }
    .demo-box { background: linear-gradient(135deg,#f5f3ff,#ede9fe); border: 1px solid #ddd6fe; border-radius: 12px; padding: 12px 16px; margin-top: 16px; font-size: 0.76rem; color: #4c1d95; text-align: center; line-height: 1.8; }
    .features-strip { display: flex; justify-content: center; gap: 16px; flex-wrap: wrap; margin: 22px 0 0 0; }
    .feature-pill { background: linear-gradient(135deg,#f5f3ff,#ede9fe); border: 1px solid #c4b5fd; border-radius: 20px; padding: 5px 14px; font-size: 0.73rem; color: #7c3aed; font-weight: 500; }
    .home-bg { background: linear-gradient(135deg,#f8f4ff 0%,#ede9fe 40%,#e0f2fe 100%); border-radius: 24px; padding: 40px 30px 30px 30px; margin-bottom: 20px; text-align: center; }
    .home-logo { font-family: 'Orbitron', sans-serif !important; font-size: 2.6rem; font-weight: 900; background: linear-gradient(135deg,#7c3aed,#4f46e5,#06b6d4); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; letter-spacing: 4px; margin-bottom: 6px; }
    .home-sub { font-size: 0.9rem; color: #7c3aed !important; letter-spacing: 3px; text-transform: uppercase; margin-bottom: 6px; }
    .home-divider { height: 3px; background: linear-gradient(90deg,transparent,#7c3aed,#4f46e5,#06b6d4,transparent); border-radius: 2px; margin: 10px auto 20px auto; width: 60%; border: none; }
    .home-tagline { font-size: 1.15rem; color: #4c1d95; font-weight: 600; margin-bottom: 4px; }
    .home-desc { font-size: 0.85rem; color: #4b5563; margin-bottom: 0; }
    .stat-num { font-size: 1.5rem; font-weight: 700; color: #7c3aed; display: block; }
    .stat-label { font-size: 0.72rem; color: #6b7280; text-transform: uppercase; letter-spacing: 1px; }
    .path-card-purple { background: linear-gradient(145deg,#7c3aed,#4f46e5,#3730a3); border-radius: 24px; padding: 36px 24px 28px 24px; text-align: center; box-shadow: 0 12px 40px rgba(124,58,237,0.35); }
    .path-card-cyan   { background: linear-gradient(145deg,#0891b2,#0e7490,#155e75); border-radius: 24px; padding: 36px 24px 28px 24px; text-align: center; box-shadow: 0 12px 40px rgba(8,145,178,0.35); }
    .card-title { font-size: 1.3rem; font-weight: 700; color: #ffffff !important; margin: 0 0 10px 0; }
    .card-features-purple, .card-features-cyan { color: #ffffff !important; font-size: 0.8rem; line-height: 1.9; }
    .card-badge { display: inline-block; background: rgba(255,255,255,0.25); border: 1px solid rgba(255,255,255,0.4); border-radius: 20px; padding: 3px 12px; font-size: 0.72rem; color: #ffffff !important; margin: 2px; }

    /* ══ MISC ══ */
    hr { border-color: #ddd6fe !important; }
    .stCaption { color: #6d28d9 !important; font-size: 0.8rem !important; }
    .stProgress > div > div { background: linear-gradient(90deg,#7c3aed,#06b6d4) !important; border-radius: 10px !important; }
    .stDataFrame td, .stDataFrame th { color: #1a1a2e !important; }
    ::-webkit-scrollbar { width: 6px; }
    ::-webkit-scrollbar-track { background: #f5f3ff; }
    ::-webkit-scrollbar-thumb { background: #7c3aed; border-radius: 10px; }
</style>
""", unsafe_allow_html=True)

# ── MENTORA AI Header Banner
st.markdown("""
<div style="text-align:center; padding: 10px 0 5px 0;">
    <span class="mentora-logo">🎓 MENTORA AI</span>
    <span class="mentora-tagline">✦ MENTORA AI ✦</span>
    <div class="mentora-divider"></div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# 3. GROQ CLIENT — supports secrets.toml, env var, or manual input
# ─────────────────────────────────────────────
import os

def _get_api_key():
    # 1️⃣ Try Streamlit secrets (Streamlit Cloud deployment)
    try:
        if "GROQ_API_KEY" in st.secrets and st.secrets["GROQ_API_KEY"]:
            return st.secrets["GROQ_API_KEY"]
    except Exception:
        pass
    # 2️⃣ Try environment variable (local .env or system)
    key = os.environ.get("GROQ_API_KEY", "")
    if key:
        return key
    # 3️⃣ Try session state (user entered it in the UI)
    return st.session_state.get("_groq_api_key", "")

_api_key = _get_api_key()

if not _api_key:
    st.markdown("""
    <div style="background:#fff7ed;border:2px solid #f97316;border-radius:16px;
    padding:24px 28px;max-width:520px;margin:40px auto;text-align:center;">
    <div style="font-size:2.5rem;">🔑</div>
    <h3 style="color:#c2410c;margin:10px 0 6px 0;font-family:Poppins,sans-serif;">GROQ API Key Required</h3>
    <p style="color:#6b7280;font-size:0.85rem;margin:0 0 16px 0;">
    Get your FREE key at <b>console.groq.com</b> → API Keys → Create Key
    </p>
    </div>
    """, unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        entered_key = st.text_input(
            "🔑 Enter your GROQ API Key:",
            type="password",
            placeholder="gsk_xxxxxxxxxxxxxxxxxxxxxxxx",
            key="groq_key_input"
        )
        if st.button("✅ Connect to AI", key="connect_ai_btn", use_container_width=True):
            if entered_key.strip().startswith("gsk_"):
                st.session_state["_groq_api_key"] = entered_key.strip()
                st.success("✅ API Key saved! Loading MENTORA AI...")
                st.rerun()
            else:
                st.error("❌ Invalid key format. GROQ keys start with 'gsk_'")
        st.markdown("""
        <div style="background:#f0fdf4;border:1px solid #bbf7d0;border-radius:10px;
        padding:12px 16px;margin-top:12px;font-size:0.78rem;color:#166534;text-align:left;">
        <b>How to get your free key:</b><br>
        1. Go to <b>console.groq.com</b><br>
        2. Sign up free → API Keys → Create API Key<br>
        3. Copy & paste the key above<br>
        4. The key is stored only for this session
        </div>
        """, unsafe_allow_html=True)
    st.stop()

try:
    client = Groq(api_key=_api_key)
    # Quick validation test
    _test = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": "hi"}],
        max_tokens=5
    )
except Exception as _e:
    err_str = str(_e)
    if "401" in err_str or "invalid_api_key" in err_str.lower() or "authentication" in err_str.lower():
        st.error("❌ Invalid API Key. Please check your GROQ key and try again.")
        if "_groq_api_key" in st.session_state:
            del st.session_state["_groq_api_key"]
    else:
        st.warning(f"⚠️ API connection issue: {err_str}. AI features may not work.")
    try:
        client = Groq(api_key=_api_key)
    except Exception:
        st.stop()

# Use latest working model with fallback
MODEL = "llama-3.3-70b-versatile"
FALLBACK_MODELS = ["llama-3.3-70b-versatile", "llama3-70b-8192", "mixtral-8x7b-32768"]

def safe_chat(messages, temperature=0.4, max_tokens=1500, json_mode=False):
    """Call Groq with automatic model fallback. Returns content string or None."""
    kwargs = {"messages": messages, "temperature": temperature, "max_tokens": max_tokens}
    if json_mode:
        kwargs["response_format"] = {"type": "json_object"}
    for model in FALLBACK_MODELS:
        try:
            r = client.chat.completions.create(model=model, **kwargs)
            return r.choices[0].message.content.strip()
        except Exception as e:
            err = str(e)
            if "401" in err or "invalid_api_key" in err.lower():
                raise  # no point retrying other models
            continue
    return None

# ─────────────────────────────────────────────
# 4. SESSION STATE
# ─────────────────────────────────────────────
DEFAULTS = {
    # ── Auth & Navigation
    "logged_in": False,
    "login_username": "",
    "app_mode": None,
    # ── Coding Practice
    "coding_lang": None,
    "coding_chapter": None,
    "code_mcqs": [],
    "code_mcq_score": None,
    # ── Subject Test
    "subtest_branch": "Computer Engineering",
    "subtest_subject": "",
    "subtest_num_q": 10,
    "subtest_mcqs": [],
    "subtest_score": None,
    "subtest_answers": {},
    # ── GATE Prep
    "gate_branch": "CSE",
    "gate_exam_date": "",
    "gate_timetable": {},
    "gate_tab": "timetable",
    # ── Daily Schedule
    "schedule_tasks": {},
    "schedule_date": "",
    # ── Tracker
    "phase": "input",
    "subjects_data": {},
    "quiz_data": [],
    "post_quiz_data": [],
    "pre_score": 0,
    "post_score": 0,
    "weakest_subject": "",
    "daily_plan_objectives": [],
    "daily_scores": {},
    "user_year": "First Year",
    "user_branch": "Computer Engineering",
    "student_name": "",
    "roll_no": "",
    "university_name": "",
    "attendance": 75,
    "chat_history": [],
    "activities": "",
    "pre_quiz_sets": [],
    "pre_set_scores": [],
    "pre_set_index": 0,
    "current_day_mcqs": [],
    "streak": 0,
    "last_active_day": 0,
    "badges": [],
    "history_log": [],
    "current_day_idx": -1,
    "ai_feedback_text": "",
    "feedback_cache_key": "",
    "pdf_bytes": b"",
    "pdf_cache_key": "",
    "pending_chat_msg": "",
    # ── Mock Interview
    "interview_branch": "Computer Engineering",
    "interview_history": [],
    "interview_score": None,
    "interview_active": False,
    # ── Notes Organiser
    "notes": [],          # list of {id, title, subject, content, tags, created}
    "note_view": "list",  # "list" | "edit" | "view"
    "note_editing_id": None,
    # ── CGPA Calculator
    "cgpa_semesters": [],
    "cgpa_branch": "Computer Engineering",
    # ── Leaderboard
    "lb_scores": [],      # list of {name, score, subject, date}
    "lb_my_name": "",
    # ── Exam Countdown
    "exams": [],          # list of {name, date, subject}
    # ── PYQ Bank
    "pyq_branch": "Computer Engineering",
    "pyq_subject": "",
    "pyq_year": "2023",
    "pyq_questions": [],
    # ── Syllabus Tracker
    "syllabus_branch": "Computer Engineering",
    "syllabus_subject": "",
    "syllabus_topics": {},  # {subject: {topic: bool}}
    # ── Smart Reminders
    "reminders": [],
}
for k, v in DEFAULTS.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ─────────────────────────────────────────────
# 5. HELPERS & AI FUNCTIONS
# ─────────────────────────────────────────────

def risk_label(avg_pct):
    if avg_pct >= 60:  return "Low",    "badge-green"
    if avg_pct >= 40:  return "Medium", "badge-orange"
    return "High", "badge-red"

def improvement_pct(ut1, ut2):
    if ut1 == 0 and ut2 == 0: return 0.0
    if ut1 == 0: return 100.0   # started from 0, any score is 100% improvement
    return round(((ut2 - ut1) / ut1) * 100, 1)

def validate_marks(v):
    return 0 <= v <= 20

def clean_mcq_list(data, n):
    """Extract, validate and normalise MCQ list from AI response."""
    # Unwrap dict wrapper if needed
    if isinstance(data, dict):
        for key in data:
            if isinstance(data[key], list):
                data = data[key]
                break

    if not isinstance(data, list):
        return []

    cleaned = []
    for q in data[:n]:
        if not isinstance(q, dict):
            continue

        question = q.get("question", "").strip()
        options  = q.get("options", [])
        answer   = str(q.get("answer", "")).strip()

        if not question or len(options) < 2:
            continue

        # Strip leading labels like "A)", "A.", "(A)" from each option
        clean_opts = []
        for opt in options:
            opt = str(opt).strip()
            opt = re.sub(r'^[A-Da-d][).\s]+', '', opt).strip()
            clean_opts.append(opt)

        # If answer is a single letter like "A"/"B"/"C"/"D", map it to the option text
        letter_map = {"a": 0, "b": 1, "c": 2, "d": 3}
        if answer.lower() in letter_map:
            idx = letter_map[answer.lower()]
            answer = clean_opts[idx] if idx < len(clean_opts) else clean_opts[0]
        else:
            # Strip label prefix from answer too
            answer = re.sub(r'^[A-Da-d][).\s]+', '', answer).strip()

        cleaned.append({
            "question": question,
            "options":  clean_opts,
            "answer":   answer
        })

    return cleaned


def is_correct(user_ans, correct_ans):
    """Robust answer comparison — handles partial matches and case differences."""
    u = str(user_ans).strip().lower()
    c = str(correct_ans).strip().lower()
    # Exact match
    if u == c:
        return True
    # One contains the other (handles minor prefix/suffix differences)
    if u in c or c in u:
        return True
    return False


def get_mcqs(subject, n=7, type_label="diagnostic", topic=""):
    focus  = f"specifically on the topic: '{topic}'" if topic else f"covering the {type_label} syllabus"
    year   = st.session_state.user_year
    branch = st.session_state.user_branch

    prompt = f"""You are a senior professor at a top engineering university setting an official examination paper.

Subject: {subject}
Branch: {branch}
Year: {year}
Focus: {focus}

Generate exactly {n} university-level engineering MCQs.

STRICT RULES:
1. Questions must be at university engineering exam difficulty — not school level.
2. Each question must have exactly 4 options.
3. Every option must be a FULL meaningful technical phrase, value, or formula — NEVER just "A", "B", "C", "D".
4. All 4 options must be technically plausible — no obviously wrong distractors.
5. The "answer" field must be the EXACT word-for-word text of the correct option.
6. Mix styles: numerical/formula-based, conceptual, application-based, code/algorithm-based (if relevant), diagram-description.
7. Use proper engineering terminology, SI units, standard notation.
8. Do NOT repeat questions.

Example GOOD question:
{{
  "question": "In a BJT amplifier, if the collector current Ic = 10 mA and base current Ib = 100 µA, what is the DC current gain (β)?",
  "options": ["100", "0.01", "1000", "10"],
  "answer": "100"
}}

Example BAD question (NEVER do this):
{{
  "question": "What is Ohm's law?",
  "options": ["A", "B", "C", "D"],
  "answer": "A"
}}

Return ONLY a JSON object:
{{"questions": [
  {{"question": "...", "options": ["full text 1", "full text 2", "full text 3", "full text 4"], "answer": "exact correct option text"}},
  ...
]}}"""

    try:
        MODELS_TO_TRY = ["llama-3.3-70b-versatile", "llama3-70b-8192", "mixtral-8x7b-32768"]
        r = None
        for _model in MODELS_TO_TRY:
            try:
                r = client.chat.completions.create(
                    model=_model,
                    messages=[
                        {
                            "role": "system",
                            "content": (
                                f"You are a strict university engineering professor for {branch}, {year}. "
                                f"You ONLY output valid JSON. Questions must be at degree-level difficulty. "
                                f"Every option must be a complete technical phrase, never a single letter or bare number."
                            )
                        },
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.4,
                    response_format={"type": "json_object"}
                )
                break  # success — stop trying models
            except Exception:
                continue
        if r is None:
            raise Exception("All models failed. Please check your API key.")
        data = json.loads(r.choices[0].message.content)
        return clean_mcq_list(data, n)
    except Exception as e:
        st.error(f"MCQ generation failed: {e}")
        return []


def generate_3_sets():
    sets = []
    for i in range(3):
        with st.spinner(f"Generating diagnostic set {i+1}/3 …"):
            sets.append(get_mcqs(
                st.session_state.weakest_subject, n=7,
                type_label=f"diagnostic set {i+1}"
            ))
    return sets


def generate_30_day_objectives(subject):
    year   = st.session_state.user_year
    branch = st.session_state.user_branch
    prompt = (
        f"List exactly 30 unique university-level engineering sub-topics from "
        f"'{subject}' for {branch} {year} students. "
        f"Each topic should be specific and exam-relevant. "
        f"One topic per line, topic name only — no numbering or bullets."
    )
    try:
        messages = [{"role": "user", "content": prompt}]
        r_raw = safe_chat(messages, temperature=0.4, max_tokens=1500)
        if r_raw is None: raise Exception("AI service unavailable. Check API key.")
        class _R: pass
        r = _R()
        class _C: pass
        r.choices = [_C()]
        r.choices[0].message = _C()
        r.choices[0].message.content = r_raw
        lines = r.choices[0].message.content.strip().split('\n')
        topics = [re.sub(r'^(Day\s\d+:|\d+\.|\d+\)|\-|\*)', '', l).strip()
                  for l in lines if len(l.strip()) > 3]
        while len(topics) < 30:
            topics.append(f"Advanced {subject} Revision")
        return topics[:30]
    except Exception:
        return [f"{subject} Topic {i+1}" for i in range(30)]


def ai_feedback(student, subject, pre, post, pct):
    year   = st.session_state.user_year
    branch = st.session_state.user_branch
    prompt = (
        f"University student '{student}' ({branch}, {year}) scored {pre}/21 in the "
        f"pre-test and {post}/21 in the post-test for '{subject}'. "
        f"Final percentage: {pct:.1f}%. "
        f"Give 3 sentences of personalised university-level academic feedback "
        f"and 2 specific actionable study tips for an engineering student."
    )
    try:
        messages = [{"role": "user", "content": prompt}]
        r_raw = safe_chat(messages, temperature=0.4, max_tokens=1500)
        if r_raw is None: raise Exception("AI service unavailable. Check API key.")
        class _R: pass
        r = _R()
        class _C: pass
        r.choices = [_C()]
        r.choices[0].message = _C()
        r.choices[0].message.content = r_raw
        return r.choices[0].message.content.strip()
    except Exception:
        return "Unable to generate feedback right now."

def compute_risk_curve():
    pre = st.session_state.pre_score / 21.0
    curve = []
    for day in range(1, 31):
        imp = (day / 30.0) * 0.4
        daily_perf = st.session_state.daily_scores.get(day, 0) / 5.0 if day in st.session_state.daily_scores else 0
        mastery = min(pre + imp + daily_perf * 0.1, 1.0)
        curve.append(max(0, round((1 - mastery) * 100, 1)))
    return curve


def save_to_csv(row_dict):
    path = "performance_history.csv"
    file_exists = os.path.isfile(path)

    # If file already exists, align columns to avoid field-count mismatch
    if file_exists:
        try:
            existing_df = pd.read_csv(path, on_bad_lines="skip")
            existing_cols = list(existing_df.columns)
            # Merge: union of existing + new columns
            new_cols = [c for c in row_dict.keys() if c not in existing_cols]
            all_cols = existing_cols + new_cols
        except Exception:
            all_cols = list(row_dict.keys())
    else:
        all_cols = list(row_dict.keys())

    # Fill missing fields with empty string
    aligned_row = {col: row_dict.get(col, "") for col in all_cols}

    # Re-write entire file if columns changed, else append
    if file_exists:
        try:
            existing_df = pd.read_csv(path, on_bad_lines="skip")
            for col in all_cols:
                if col not in existing_df.columns:
                    existing_df[col] = ""
            existing_df = existing_df[all_cols]
            new_row_df  = pd.DataFrame([aligned_row], columns=all_cols)
            combined    = pd.concat([existing_df, new_row_df], ignore_index=True)
            combined.to_csv(path, index=False)
        except Exception:
            # Fallback: just append — better than crashing
            with open(path, "a", newline="") as f:
                writer = csv.DictWriter(f, fieldnames=all_cols, extrasaction="ignore")
                writer.writerow(aligned_row)
    else:
        with open(path, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=all_cols)
            writer.writeheader()
            writer.writerow(aligned_row)

def check_badges(day_idx, score):
    badges = st.session_state.badges
    if score == 5 and "⭐ Perfect Day" not in badges:
        badges.append("⭐ Perfect Day")
    if day_idx == 7 and "🔥 One Week Warrior" not in badges:
        badges.append("🔥 One Week Warrior")
    if day_idx == 30 and "🏆 30-Day Champion" not in badges:
        badges.append("🏆 30-Day Champion")
    # Streak badge
    if st.session_state.streak >= 5 and "💪 5-Day Streak" not in badges:
        badges.append("💪 5-Day Streak")
    st.session_state.badges = badges

# ─────────────────────────────────────────────
# 6. PDF REPORT GENERATOR
# ─────────────────────────────────────────────

def generate_pdf_report():
    buf = BytesIO()
    doc = SimpleDocTemplate(buf, pagesize=A4,
                            rightMargin=40, leftMargin=40,
                            topMargin=40, bottomMargin=40)
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style  = ParagraphStyle("title",  parent=styles["Title"],
                                  fontSize=22, textColor=colors.HexColor("#7c3aed"),
                                  spaceAfter=4, alignment=TA_CENTER)
    sub_style    = ParagraphStyle("sub",    parent=styles["Normal"],
                                  fontSize=11, textColor=colors.grey,
                                  alignment=TA_CENTER, spaceAfter=16)
    heading_style= ParagraphStyle("h2",     parent=styles["Heading2"],
                                  fontSize=13, textColor=colors.HexColor("#4f46e5"),
                                  spaceBefore=14, spaceAfter=6)
    body_style   = ParagraphStyle("body",   parent=styles["Normal"],
                                  fontSize=10, leading=14,
                                  textColor=colors.HexColor("#1e293b"))

    story = []

    # ── Header
    story.append(Paragraph("🎓 AI Academic Mentor — Student Report", title_style))
    story.append(Paragraph(f"Generated: {datetime.now().strftime('%d %b %Y  %H:%M')}", sub_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#7c3aed")))
    story.append(Spacer(1, 12))

    # ── Student Info table
    story.append(Paragraph("Student Details", heading_style))
    info_data = [
        ["Name",         st.session_state.student_name or "—",
         "University",   st.session_state.university_name or "—"],
        ["Roll No.",     st.session_state.roll_no or "—",
         "Attendance",   f"{st.session_state.attendance}%"],
        ["Branch",       st.session_state.user_branch,
         "Year",         st.session_state.user_year],
        ["Activities",   st.session_state.activities or "—",
         "Weak Subject", st.session_state.weakest_subject or "—"],
    ]
    info_table = Table(info_data, colWidths=[80, 130, 80, 130])
    info_table.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,-1), colors.HexColor("#f5f3ff")),
        ("FONTNAME",   (0,0), (0,-1), "Helvetica-Bold"),
        ("FONTNAME",   (2,0), (2,-1), "Helvetica-Bold"),
        ("FONTSIZE",   (0,0), (-1,-1), 9),
        ("ROWBACKGROUNDS", (0,0), (-1,-1), [colors.HexColor("#ede9fe"), colors.HexColor("#f5f3ff")]),
        ("GRID",       (0,0), (-1,-1), 0.5, colors.HexColor("#c4b5fd")),
        ("PADDING",    (0,0), (-1,-1), 6),
    ]))
    story.append(info_table)
    story.append(Spacer(1, 12))

    # ── Marks table
    story.append(Paragraph("Internal Assessment Performance", heading_style))
    marks_header = [["Subject", "IA1 (0–30)", "IA2 (0–30)", "Avg", "Improvement %"]]
    marks_rows   = []
    for s, v in st.session_state.subjects_data.items():
        avg = (v["IA1"] + v["IA2"]) / 2
        imp = improvement_pct(v["IA1"], v["IA2"])
        marks_rows.append([s, v["IA1"], v["IA2"], f"{avg:.1f}", f"{imp:+.1f}%"])
    marks_table = Table(marks_header + marks_rows,
                        colWidths=[120, 80, 80, 70, 100])
    marks_table.setStyle(TableStyle([
        ("BACKGROUND",  (0,0), (-1,0), colors.HexColor("#7c3aed")),
        ("TEXTCOLOR",   (0,0), (-1,0), colors.white),
        ("FONTNAME",    (0,0), (-1,0), "Helvetica-Bold"),
        ("ROWBACKGROUNDS", (0,1), (-1,-1),
         [colors.HexColor("#faf5ff"), colors.white]),
        ("GRID",        (0,0), (-1,-1), 0.5, colors.HexColor("#c4b5fd")),
        ("ALIGN",       (1,0), (-1,-1), "CENTER"),
        ("FONTSIZE",    (0,0), (-1,-1), 9),
        ("PADDING",     (0,0), (-1,-1), 6),
    ]))
    story.append(marks_table)
    story.append(Spacer(1, 12))

    # ── Test scores
    story.append(Paragraph("Diagnostic vs Final Assessment", heading_style))
    pre  = st.session_state.pre_score
    post = st.session_state.post_score
    pct  = (post / 21 * 100) if post else 0
    verdict = "PASS ✅" if pct >= 60 else ("BORDERLINE ⚠️" if pct >= 40 else "FAIL ❌")
    risk, _ = risk_label(pct)
    score_data = [
        ["Metric",              "Value"],
        ["Pre-Test Score",      f"{pre} / 21"],
        ["Post-Test Score",     f"{post} / 21"],
        ["Final Percentage",    f"{pct:.1f}%"],
        ["Pass/Fail Prediction",verdict],
        ["Risk Level",          risk],
    ]
    score_table = Table(score_data, colWidths=[200, 200])
    score_table.setStyle(TableStyle([
        ("BACKGROUND",  (0,0), (-1,0), colors.HexColor("#4f46e5")),
        ("TEXTCOLOR",   (0,0), (-1,0), colors.white),
        ("FONTNAME",    (0,0), (-1,0), "Helvetica-Bold"),
        ("ROWBACKGROUNDS", (0,1), (-1,-1),
         [colors.HexColor("#eef2ff"), colors.white]),
        ("GRID",        (0,0), (-1,-1), 0.5, colors.HexColor("#a5b4fc")),
        ("ALIGN",       (1,0), (-1,-1), "CENTER"),
        ("FONTSIZE",    (0,0), (-1,-1), 10),
        ("PADDING",     (0,0), (-1,-1), 7),
    ]))
    story.append(score_table)
    story.append(Spacer(1, 12))

    # ── Daily progress
    if st.session_state.daily_scores:
        story.append(Paragraph("30-Day Daily Practice Scores", heading_style))
        rows = [["Day", "Topic", "Score /5"]]
        for day, sc in sorted(st.session_state.daily_scores.items()):
            topic = ""
            if st.session_state.daily_plan_objectives and day <= 30:
                topic = st.session_state.daily_plan_objectives[day - 1]
            rows.append([str(day), topic or "—", f"{sc}/5"])
        daily_t = Table(rows, colWidths=[40, 310, 70])
        daily_t.setStyle(TableStyle([
            ("BACKGROUND",  (0,0), (-1,0), colors.HexColor("#0f766e")),
            ("TEXTCOLOR",   (0,0), (-1,0), colors.white),
            ("FONTNAME",    (0,0), (-1,0), "Helvetica-Bold"),
            ("ROWBACKGROUNDS", (0,1), (-1,-1),
             [colors.HexColor("#f0fdf4"), colors.white]),
            ("GRID",        (0,0), (-1,-1), 0.4, colors.HexColor("#99f6e4")),
            ("FONTSIZE",    (0,0), (-1,-1), 9),
            ("PADDING",     (0,0), (-1,-1), 5),
        ]))
        story.append(daily_t)
        story.append(Spacer(1, 12))

    # ── AI Feedback
    if post > 0:
        story.append(Paragraph("AI Personalised Feedback", heading_style))
        feedback = ai_feedback(
            st.session_state.student_name or "Student",
            st.session_state.weakest_subject,
            pre, post, pct
        )
        story.append(Paragraph(feedback, body_style))
        story.append(Spacer(1, 12))

    # ── Badges
    if st.session_state.badges:
        story.append(Paragraph("Achievements Earned", heading_style))
        story.append(Paragraph("  ".join(st.session_state.badges), body_style))
        story.append(Spacer(1, 12))

    # ── Footer
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#7c3aed")))
    story.append(Spacer(1, 6))
    story.append(Paragraph("MENTORA AI  |  Powered by Groq LLaMA 3.3 70B",
                            ParagraphStyle("footer", parent=styles["Normal"],
                                           fontSize=8, textColor=colors.grey,
                                           alignment=TA_CENTER)))
    doc.build(story)
    buf.seek(0)
    return buf


# ─────────────────────────────────────────────
# 7B. CODING CONTENT DATABASE
# ─────────────────────────────────────────────
CODING_CONTENT = {
    "C Programming": {
        "icon": "🔵", "color": "#2563eb",
        "chapters": {
            "1. Introduction to C": {
                "theory": "**C** was developed by Dennis Ritchie in 1972.\n\n**Structure:**\n```c\n#include <stdio.h>\nint main() {\n    printf(\"Hello!\");\n    return 0;\n}\n```\n\n**Key Points:**\n- `#include` includes library\n- `main()` is entry point\n- `printf()` prints output\n- Compiled language, very fast",
                "example": "```c\n#include <stdio.h>\nint main() {\n    printf(\"Hello, MENTORA AI!\\n\");\n    printf(\"Welcome to C Programming\\n\");\n    return 0;\n}\n```\n**Output:**\n```\nHello, MENTORA AI!\nWelcome to C Programming\n```",
                "mcq_topic": "C programming basics structure syntax printf"
            },
            "2. Variables & Data Types": {
                "theory": "**Data Types:**\n- `int` (4 bytes) — integers\n- `float` (4 bytes) — decimals\n- `double` (8 bytes) — precise decimals\n- `char` (1 byte) — single character\n\n**Format Specifiers:**\n- `%d` integer, `%f` float, `%c` char, `%s` string",
                "example": "```c\n#include <stdio.h>\nint main() {\n    int age = 21;\n    float cgpa = 8.5;\n    char grade = 'A';\n    printf(\"Age: %d\\n\", age);\n    printf(\"CGPA: %.2f\\n\", cgpa);\n    printf(\"Grade: %c\\n\", grade);\n    return 0;\n}\n```",
                "mcq_topic": "C variables data types int float char"
            },
            "3. Operators": {
                "theory": "**Types:** Arithmetic `+ - * / %`, Relational `== != > <`, Logical `&& || !`, Assignment `= += -=`, Increment `++ --`, Bitwise `& | ^`",
                "example": "```c\n#include <stdio.h>\nint main() {\n    int a=10, b=3;\n    printf(\"Add:%d Sub:%d Mul:%d\\n\", a+b, a-b, a*b);\n    printf(\"Div:%d Mod:%d\\n\", a/b, a%b);\n    a++; printf(\"After a++: %d\\n\", a);\n    return 0;\n}\n```",
                "mcq_topic": "C operators arithmetic relational logical"
            },
            "4. Control Flow": {
                "theory": "**if-else:**\n```c\nif(x>0) printf(\"Positive\");\nelse if(x<0) printf(\"Negative\");\nelse printf(\"Zero\");\n```\n**switch:**\n```c\nswitch(n){case 1: ...; break; default: ...;}\n```\n**Ternary:** `result = (a>b) ? a : b;`",
                "example": "```c\n#include <stdio.h>\nint main() {\n    int m=75;\n    if(m>=90) printf(\"Grade O\\n\");\n    else if(m>=80) printf(\"Grade A+\\n\");\n    else if(m>=70) printf(\"Grade A\\n\");\n    else printf(\"Below A\\n\");\n    printf(\"%s\\n\", m>=40?\"PASS\":\"FAIL\");\n    return 0;\n}\n```",
                "mcq_topic": "C if else switch control flow"
            },
            "5. Loops": {
                "theory": "**for:** `for(i=0; i<n; i++)`\n**while:** `while(condition){}`\n**do-while:** `do{} while(condition);`\n**break** — exit loop, **continue** — skip iteration",
                "example": "```c\n#include <stdio.h>\nint main() {\n    for(int i=1;i<=5;i++) printf(\"%d \",i);\n    printf(\"\\n\");\n    int sum=0,n=1;\n    while(n<=10){ sum+=n; n++; }\n    printf(\"Sum 1-10: %d\\n\", sum);\n    return 0;\n}\n```",
                "mcq_topic": "C for while do-while loops"
            },
            "6. Arrays": {
                "theory": "```c\nint arr[5] = {10,20,30,40,50};\nint matrix[3][3] = {{1,2,3},{4,5,6},{7,8,9}};\n```\n- Index starts at 0\n- Stored in contiguous memory\n- `arr[i]` — access element i",
                "example": "```c\n#include <stdio.h>\nint main() {\n    int arr[]={5,3,8,1,9};\n    int n=5, max=arr[0], sum=0;\n    for(int i=0;i<n;i++){\n        sum+=arr[i];\n        if(arr[i]>max) max=arr[i];\n    }\n    printf(\"Max:%d Sum:%d\\n\",max,sum);\n    return 0;\n}\n```",
                "mcq_topic": "C arrays 1D 2D indexing"
            },
            "7. Functions": {
                "theory": "```c\nreturn_type name(params) {\n    return value;\n}\n```\n**Call by Value** — copy passed, original unchanged\n**Call by Reference** — pointer passed, original changes\n**Recursive** — function calls itself",
                "example": "```c\n#include <stdio.h>\nint factorial(int n){\n    if(n<=1) return 1;\n    return n*factorial(n-1);\n}\nvoid swap(int *a,int *b){\n    int t=*a; *a=*b; *b=t;\n}\nint main(){\n    printf(\"5!=%d\\n\",factorial(5));\n    int x=10,y=20; swap(&x,&y);\n    printf(\"x=%d y=%d\\n\",x,y);\n}\n```",
                "mcq_topic": "C functions recursion call by value reference"
            },
            "8. Pointers": {
                "theory": "**Pointer** stores memory address.\n```c\nint *ptr = &var;  // store address\n*ptr              // dereference\nptr++             // pointer arithmetic\n```\n`&` — address-of, `*` — dereference\n`NULL` pointer — safe initialisation",
                "example": "```c\n#include <stdio.h>\nint main(){\n    int num=42;\n    int *ptr=&num;\n    printf(\"Value: %d\\n\",*ptr);\n    *ptr=100;\n    printf(\"Changed: %d\\n\",num);\n    int arr[]={10,20,30};\n    int *p=arr;\n    for(int i=0;i<3;i++) printf(\"%d \",*(p+i));\n    return 0;\n}\n```",
                "mcq_topic": "C pointers address dereference pointer arithmetic"
            },
            "9. Strings": {
                "theory": "Strings are char arrays ending with `\\0`\n```c\nchar s[] = \"MENTORA\";\n```\n**Functions:** `strlen`, `strcpy`, `strcat`, `strcmp`, `strupr`, `strlwr`",
                "example": "```c\n#include <stdio.h>\n#include <string.h>\nint main(){\n    char s1[]=\"MENTORA\",s2[]=\" AI\",s3[20];\n    printf(\"Len:%lu\\n\",strlen(s1));\n    strcpy(s3,s1); strcat(s3,s2);\n    printf(\"%s\\n\",s3);\n    printf(\"Equal:%d\\n\",strcmp(s1,s1));\n    return 0;\n}\n```",
                "mcq_topic": "C strings strlen strcpy strcat strcmp"
            },
            "10. Structures & File I/O": {
                "theory": "```c\nstruct Student{ int roll; char name[50]; float cgpa; };\nstruct Student s = {101, \"Alex\", 8.5};\n```\n**File:** `fopen`, `fprintf`, `fscanf`, `fclose`\nModes: `\"r\"` read, `\"w\"` write, `\"a\"` append",
                "example": "```c\n#include <stdio.h>\nstruct Student{int roll;char name[50];float cgpa;};\nint main(){\n    struct Student s={101,\"Aryan\",9.1};\n    printf(\"%d %s %.1f\\n\",s.roll,s.name,s.cgpa);\n    FILE *fp=fopen(\"out.txt\",\"w\");\n    fprintf(fp,\"%s %.1f\",s.name,s.cgpa);\n    fclose(fp);\n    printf(\"Saved!\\n\");\n}\n```",
                "mcq_topic": "C structures file handling fopen fclose"
            },
        }
    },
    "C++ Programming": {
        "icon": "🟣", "color": "#7c3aed",
        "chapters": {
            "1. OOP Concepts": {
                "theory": "**4 Pillars:** Encapsulation, Inheritance, Polymorphism, Abstraction\n\n```cpp\nclass Student{\nprivate:\n    string name; float cgpa;\npublic:\n    Student(string n,float c):name(n),cgpa(c){}\n    void display(){ cout<<name<<\" \"<<cgpa; }\n};\n```",
                "example": "```cpp\n#include<iostream>\nusing namespace std;\nclass Rectangle{\n    float l,w;\npublic:\n    Rectangle(float a,float b):l(a),w(b){}\n    float area(){return l*w;}\n    float peri(){return 2*(l+w);}\n};\nint main(){\n    Rectangle r(10,4);\n    cout<<\"Area:\"<<r.area()<<\" Peri:\"<<r.peri();\n}\n```",
                "mcq_topic": "C++ OOP classes objects encapsulation"
            },
            "2. Inheritance": {
                "theory": "**Types:** Single, Multiple, Multilevel, Hierarchical\n```cpp\nclass Animal{ public: void eat(){} };\nclass Dog:public Animal{ public: void bark(){} };\n```\nAccess: `public`, `private`, `protected`",
                "example": "```cpp\n#include<iostream>\nusing namespace std;\nclass Shape{ public: string color; Shape(string c):color(c){} };\nclass Circle:public Shape{\n    float r;\npublic:\n    Circle(string c,float r):Shape(c),r(r){}\n    void show(){ cout<<color<<\" circle area:\"<<3.14*r*r; }\n};\nint main(){ Circle c(\"Red\",5); c.show(); }\n```",
                "mcq_topic": "C++ inheritance types single multiple"
            },
            "3. Polymorphism": {
                "theory": "**Compile-time:** Function overloading, Operator overloading\n**Runtime:** Virtual functions, Function overriding\n```cpp\nvirtual void show()=0;  // pure virtual\n```",
                "example": "```cpp\n#include<iostream>\nusing namespace std;\nclass Animal{public: virtual void sound(){cout<<\"...\\n\";}};\nclass Dog:public Animal{public: void sound() override{cout<<\"Woof!\\n\";}};\nclass Cat:public Animal{public: void sound() override{cout<<\"Meow!\\n\";}};\nint main(){\n    Animal *a;\n    Dog d; Cat c;\n    a=&d; a->sound();\n    a=&c; a->sound();\n}\n```",
                "mcq_topic": "C++ polymorphism virtual override"
            },
            "4. STL Containers": {
                "theory": "**Containers:** `vector`, `list`, `map`, `set`, `stack`, `queue`\n```cpp\nvector<int> v={1,2,3};\nv.push_back(4);\nsort(v.begin(),v.end());\nmap<string,int> m; m[\"key\"]=10;\n```",
                "example": "```cpp\n#include<iostream>\n#include<vector>\n#include<algorithm>\n#include<map>\nusing namespace std;\nint main(){\n    vector<int> v={5,2,8,1,9};\n    sort(v.begin(),v.end());\n    for(int x:v) cout<<x<<\" \";\n    map<string,int> marks;\n    marks[\"DBMS\"]=85; marks[\"OS\"]=90;\n    for(auto &p:marks) cout<<p.first<<\":\"<<p.second<<\" \";\n}\n```",
                "mcq_topic": "C++ STL vector map sort algorithms"
            },
            "5. Templates & Generics": {
                "theory": "**Function Template:**\n```cpp\ntemplate<typename T>\nT maxVal(T a, T b){ return (a>b)?a:b; }\n```\n**Class Template:**\n```cpp\ntemplate<typename T>\nclass Stack{ vector<T> v; public: void push(T x){v.push_back(x);} };\n```",
                "example": "```cpp\n#include<iostream>\n#include<vector>\nusing namespace std;\ntemplate<typename T>\nT sumArr(T arr[],int n){\n    T s=0;\n    for(int i=0;i<n;i++) s+=arr[i];\n    return s;\n}\nint main(){\n    int a[]={1,2,3,4,5};\n    double b[]={1.1,2.2,3.3};\n    cout<<sumArr(a,5)<<endl;\n    cout<<sumArr(b,3)<<endl;\n}\n```",
                "mcq_topic": "C++ templates generic programming"
            },
            "6. Exception Handling": {
                "theory": "```cpp\ntry{\n    if(x==0) throw runtime_error(\"Division by zero\");\n    cout<<10/x;\n}catch(runtime_error &e){\n    cout<<\"Error: \"<<e.what();\n}catch(...){\n    cout<<\"Unknown error\";\n}finally{ // not in C++, use RAII }\n```",
                "example": "```cpp\n#include<iostream>\n#include<stdexcept>\nusing namespace std;\ndouble divide(double a,double b){\n    if(b==0) throw invalid_argument(\"Divisor cannot be zero\");\n    return a/b;\n}\nint main(){\n    try{\n        cout<<divide(10,2)<<endl;\n        cout<<divide(5,0)<<endl;\n    }catch(invalid_argument &e){\n        cout<<\"Caught: \"<<e.what()<<endl;\n    }\n}\n```",
                "mcq_topic": "C++ exception handling try catch throw"
            },
            "7. File Handling & Streams": {
                "theory": "```cpp\n#include<fstream>\nofstream out(\"file.txt\");  // write\nifstream in(\"file.txt\");   // read\nfstream f(\"file.txt\", ios::in|ios::out);\n```\n**Modes:** `ios::in`, `ios::out`, `ios::app`, `ios::binary`",
                "example": "```cpp\n#include<iostream>\n#include<fstream>\n#include<string>\nusing namespace std;\nint main(){\n    ofstream out(\"students.txt\");\n    out<<\"Aryan 9.1\\nSara 8.5\\n\";\n    out.close();\n    ifstream in(\"students.txt\");\n    string line;\n    while(getline(in,line)) cout<<line<<endl;\n    in.close();\n}\n```",
                "mcq_topic": "C++ file handling fstream ifstream ofstream"
            },
            "8. Smart Pointers & Memory": {
                "theory": "**Unique Pointer** — sole ownership\n**Shared Pointer** — reference counted\n**Weak Pointer** — non-owning reference\n```cpp\n#include<memory>\nunique_ptr<int> p = make_unique<int>(42);\nshared_ptr<int> sp = make_shared<int>(10);\n```\nPrevent memory leaks — auto delete when out of scope.",
                "example": "```cpp\n#include<iostream>\n#include<memory>\nusing namespace std;\nclass Node{ public: int val; Node(int v):val(v){ cout<<\"Created \"<<v<<endl; } ~Node(){ cout<<\"Destroyed \"<<val<<endl; } };\nint main(){\n    unique_ptr<Node> p1 = make_unique<Node>(1);\n    shared_ptr<Node> sp1 = make_shared<Node>(2);\n    shared_ptr<Node> sp2 = sp1;\n    cout<<\"Count: \"<<sp1.use_count()<<endl;\n}\n```",
                "mcq_topic": "C++ smart pointers unique_ptr shared_ptr memory management"
            },
        }
    },
    "Python": {
        "icon": "🟡", "color": "#d97706",
        "chapters": {
            "1. Basics": {
                "theory": "**Python** — high-level, interpreted, dynamically typed.\n\n```python\nname = \"MENTORA\"  # str\nage = 21          # int\ncgpa = 9.1        # float\nflag = True       # bool\nprint(f\"Hello {name}, CGPA={cgpa}\")\n```",
                "example": "```python\nname = input(\"Name: \")\ncgpa = 9.1\nprint(f\"Hello {name}!\")\nprint(f\"CGPA: {cgpa:.2f}\")\na, b, c = 10, 20, 30\nprint(a + b + c)  # 60\nprint(type(cgpa)) # <class 'float'>\n```",
                "mcq_topic": "Python basics variables data types input output"
            },
            "2. Lists Tuples Sets Dicts": {
                "theory": "**List** — ordered, mutable: `[1,2,3]`\n**Tuple** — ordered, immutable: `(1,2,3)`\n**Set** — unique: `{1,2,3}`\n**Dict** — key-value: `{'a':1}`\n\nList comprehension: `[x*2 for x in lst if x>0]`",
                "example": "```python\nstudents = [\n    {\"name\":\"Aryan\",\"cgpa\":9.1},\n    {\"name\":\"Sara\", \"cgpa\":8.5},\n]\ntoppers = [s[\"name\"] for s in students if s[\"cgpa\"]>=9]\nprint(\"Toppers:\",toppers)\nstudents.sort(key=lambda x:x[\"cgpa\"],reverse=True)\nfor s in students: print(f\"{s['name']}:{s['cgpa']}\")\n```",
                "mcq_topic": "Python list tuple set dictionary comprehension"
            },
            "3. Functions & Lambda": {
                "theory": "```python\ndef func(params, default=value, *args, **kwargs):\n    return result\n\nlambda x: x**2   # anonymous function\nmap(func, lst)   # apply func to all\nfilter(func,lst) # filter by condition\n```",
                "example": "```python\ndef cgpa(marks, credits):\n    return sum(m*c for m,c in zip(marks,credits))/sum(credits)\n\nprint(f\"{cgpa([85,90,78],[4,3,3]):.2f}\")\n\nsquare = lambda x: x*x\nnums = [1,2,3,4,5]\nprint(list(map(square, nums)))\nprint(list(filter(lambda x:x>2, nums)))\n```",
                "mcq_topic": "Python functions lambda map filter"
            },
            "4. OOP": {
                "theory": "```python\nclass ClassName:\n    def __init__(self, params):\n        self.attr = params\n    def method(self):\n        return self.attr\n\nclass Child(Parent):\n    def __init__(self): super().__init__()\n```\nDunder: `__str__`, `__len__`, `__add__`",
                "example": "```python\nclass BankAccount:\n    def __init__(self, owner, bal=0):\n        self.owner = owner\n        self.__bal = bal\n    def deposit(self, amt): self.__bal += amt\n    def withdraw(self, amt):\n        if amt>self.__bal: print(\"Insufficient!\")\n        else: self.__bal -= amt\n    def __str__(self): return f\"{self.owner}:Rs{self.__bal}\"\n\nacc = BankAccount(\"Aryan\",1000)\nacc.deposit(500); acc.withdraw(200)\nprint(acc)  # Aryan:Rs1300\n```",
                "mcq_topic": "Python OOP classes objects inheritance"
            },
            "6. Modules, Packages & Virtual Env": {
                "theory": "```python\nimport os, sys, math, random\nfrom datetime import datetime\nimport json, csv, re\n\n# Virtual environment\n# python -m venv env\n# source env/bin/activate  (Linux/Mac)\n# env\\Scripts\\activate     (Windows)\n# pip install requests pandas numpy\n```\n**pip:** `pip install`, `pip freeze > requirements.txt`, `pip install -r requirements.txt`",
                "example": "```python\nimport json, os, random\nfrom datetime import datetime\n\n# Save student data to JSON\nstudents = [\n    {\"name\": \"Aryan\", \"cgpa\": 9.1, \"branch\": \"CS\"},\n    {\"name\": \"Sara\",  \"cgpa\": 8.5, \"branch\": \"EC\"},\n]\nwith open(\"students.json\", \"w\") as f:\n    json.dump(students, f, indent=2)\n\nwith open(\"students.json\") as f:\n    data = json.load(f)\n\ntoppers = [s[\"name\"] for s in data if s[\"cgpa\"] >= 9.0]\nprint(f\"{datetime.now().date()} — Toppers: {toppers}\")\n```",
                "mcq_topic": "Python modules packages import pip virtual environment"
            },
            "7. NumPy & Pandas Basics": {
                "theory": "**NumPy:** fast array operations\n```python\nimport numpy as np\narr = np.array([1,2,3,4,5])\narr * 2          # vectorized\nnp.mean(arr)     # statistics\nnp.dot(A, B)     # matrix multiply\n```\n**Pandas:** tabular data\n```python\nimport pandas as pd\ndf = pd.read_csv('data.csv')\ndf['col'].mean()\ndf[df['cgpa'] > 8]\ndf.groupby('branch')['cgpa'].mean()\n```",
                "example": "```python\nimport numpy as np\nimport pandas as pd\n\n# NumPy\nmarks = np.array([85, 92, 78, 95, 65, 88])\nprint(f\"Mean:{marks.mean():.1f} Std:{marks.std():.1f} Max:{marks.max()}\")\nprint(f\"Above 80: {marks[marks > 80]}\")\n\n# Pandas\ndata = {'name':['Aryan','Sara','Raj'],'cgpa':[9.1,8.5,7.8],'branch':['CS','EC','ME']}\ndf = pd.DataFrame(data)\nprint(df[df['cgpa'] >= 9.0][['name','cgpa']])\nprint(df.groupby('branch')['cgpa'].mean())\n```",
                "mcq_topic": "Python NumPy Pandas arrays DataFrame groupby"
            },
            "8. Decorators, Generators & Context Managers": {
                "theory": "**Decorator** — wrap a function to add behavior\n```python\ndef timer(func):\n    def wrapper(*args, **kwargs):\n        import time\n        t = time.time()\n        result = func(*args, **kwargs)\n        print(f\"Time: {time.time()-t:.4f}s\")\n        return result\n    return wrapper\n\n@timer\ndef my_func(): ...\n```\n**Generator:** `yield` — lazy sequence\n**Context Manager:** `with` — auto cleanup",
                "example": "```python\n# Generator — memory efficient\ndef fibonacci(n):\n    a, b = 0, 1\n    for _ in range(n):\n        yield a\n        a, b = b, a+b\n\nprint(list(fibonacci(10)))\n\n# Context manager\nclass Timer:\n    import time\n    def __enter__(self):\n        self.start = __import__('time').time()\n        return self\n    def __exit__(self, *args):\n        elapsed = __import__('time').time() - self.start\n        print(f\"Elapsed: {elapsed:.4f}s\")\n\nwith Timer():\n    total = sum(fibonacci(1000))\nprint(total)\n```",
                "mcq_topic": "Python decorators generators yield context managers with"
            },
        }
    },
    "Java": {
        "icon": "🟠", "color": "#ea580c",
        "chapters": {
            "1. Basics & JVM": {
                "theory": "**Java** — platform independent, OOP, automatic GC\n```\n.java → javac → .class (bytecode) → JVM → Output\n```\n```java\npublic class Main {\n    public static void main(String[] args) {\n        System.out.println(\"Hello!\");\n    }\n}\n```",
                "example": "```java\npublic class Main {\n    public static void main(String[] args) {\n        String name = \"Aryan\";\n        int age = 21;\n        double cgpa = 9.1;\n        System.out.println(\"Name: \"+name);\n        System.out.printf(\"CGPA: %.2f%n\",cgpa);\n        int marks = (int)(cgpa*10);\n        System.out.println(\"Marks:\"+marks);\n    }\n}\n```",
                "mcq_topic": "Java basics JVM architecture main method"
            },
            "2. OOP & Inheritance": {
                "theory": "```java\nclass Animal{\n    public void speak(){System.out.println(\"...\");}\n}\nclass Dog extends Animal{\n    @Override\n    public void speak(){System.out.println(\"Woof!\");}\n}\n```\n**Interface:** `interface Drawable { void draw(); }`",
                "example": "```java\nabstract class Shape{\n    abstract double area();\n    void show(){ System.out.printf(\"Area:%.2f%n\",area()); }\n}\nclass Circle extends Shape{\n    double r; Circle(double r){this.r=r;}\n    double area(){return Math.PI*r*r;}\n}\npublic class Main{\n    public static void main(String[] a){\n        new Circle(5).show();\n    }\n}\n```",
                "mcq_topic": "Java OOP inheritance abstract interface"
            },
            "3. Collections Framework": {
                "theory": "```java\nArrayList<String> list = new ArrayList<>();\nlist.add(\"DBMS\");\nHashMap<String,Integer> map = new HashMap<>();\nmap.put(\"OS\",90);\nCollections.sort(list);\n```\nHierarchy: Collection → List, Set, Queue; Map (separate)",
                "example": "```java\nimport java.util.*;\npublic class Main{\n    public static void main(String[] a){\n        ArrayList<String> sub=new ArrayList<>();\n        sub.add(\"DBMS\"); sub.add(\"OS\"); sub.add(\"CN\");\n        Collections.sort(sub);\n        System.out.println(sub);\n        HashMap<String,Integer> m=new HashMap<>();\n        m.put(\"DBMS\",85); m.put(\"OS\",92);\n        m.forEach((k,v)->System.out.println(k+\":\"+v));\n    }\n}\n```",
                "mcq_topic": "Java ArrayList HashMap Collections sort"
            },
            "4. Exception Handling": {
                "theory": "```java\ntry{\n    int x = 10/0;\n}catch(ArithmeticException e){\n    System.out.println(\"Error: \"+e.getMessage());\n}catch(Exception e){\n    e.printStackTrace();\n}finally{\n    System.out.println(\"Always runs\");\n}\n```\n**Custom Exception:** `class MyEx extends Exception{}`",
                "example": "```java\nimport java.io.*;\npublic class Main{\n    static int divide(int a,int b) throws ArithmeticException{\n        if(b==0) throw new ArithmeticException(\"Zero divisor\");\n        return a/b;\n    }\n    public static void main(String[] args){\n        try{\n            System.out.println(divide(10,2));\n            System.out.println(divide(5,0));\n        }catch(ArithmeticException e){\n            System.out.println(\"Caught: \"+e.getMessage());\n        }finally{\n            System.out.println(\"Done\");\n        }\n    }\n}\n```",
                "mcq_topic": "Java exception handling try catch finally throws"
            },
            "5. Multithreading": {
                "theory": "**Thread creation:**\n1. Extend `Thread` class\n2. Implement `Runnable` interface\n\n```java\nclass MyThread extends Thread{\n    public void run(){ System.out.println(\"Running\"); }\n}\nnew MyThread().start();\n```\n**Synchronization:** `synchronized` keyword prevents race conditions",
                "example": "```java\nclass Counter{\n    private int count=0;\n    synchronized void increment(){ count++; }\n    int get(){ return count; }\n}\npublic class Main{\n    public static void main(String[] a) throws InterruptedException{\n        Counter c=new Counter();\n        Thread t1=new Thread(()->{ for(int i=0;i<1000;i++) c.increment(); });\n        Thread t2=new Thread(()->{ for(int i=0;i<1000;i++) c.increment(); });\n        t1.start(); t2.start();\n        t1.join(); t2.join();\n        System.out.println(c.get()); // 2000\n    }\n}\n```",
                "mcq_topic": "Java multithreading Thread Runnable synchronized"
            },
            "6. Java 8 — Streams & Lambda": {
                "theory": "```java\n// Lambda\nlist.forEach(x -> System.out.println(x));\n// Stream pipeline\nlist.stream()\n    .filter(x -> x > 5)\n    .map(x -> x * 2)\n    .collect(Collectors.toList());\n// Optional\nOptional<String> opt = Optional.of(\"MENTORA\");\nopt.ifPresent(System.out::println);\n```",
                "example": "```java\nimport java.util.*;\nimport java.util.stream.*;\npublic class Main{\n    public static void main(String[] a){\n        List<Integer> marks=Arrays.asList(85,92,78,95,65,88);\n        double avg=marks.stream().mapToInt(Integer::intValue).average().orElse(0);\n        List<Integer> pass=marks.stream().filter(m->m>=80).sorted().collect(Collectors.toList());\n        System.out.printf(\"Avg: %.1f%n\",avg);\n        System.out.println(\"Passed: \"+pass);\n    }\n}\n```",
                "mcq_topic": "Java 8 streams lambda filter map collect"
            },
            "7. JDBC & File I/O": {
                "theory": "**File I/O:**\n```java\nBufferedReader br = new BufferedReader(new FileReader(\"f.txt\"));\nBufferedWriter bw = new BufferedWriter(new FileWriter(\"f.txt\"));\n```\n**JDBC Steps:** Load driver → getConnection → createStatement → executeQuery → ResultSet → close",
                "example": "```java\nimport java.io.*;\nimport java.nio.file.*;\npublic class Main{\n    public static void main(String[] a) throws IOException{\n        // Write\n        List<String> lines=Arrays.asList(\"Aryan,CS,9.1\",\"Sara,EC,8.5\");\n        Files.write(Paths.get(\"students.txt\"),lines);\n        // Read\n        Files.lines(Paths.get(\"students.txt\"))\n             .map(l->l.split(\",\"))\n             .forEach(p->System.out.println(p[0]+\": CGPA \"+p[2]));\n    }\n}\n```",
                "mcq_topic": "Java file I/O JDBC BufferedReader FileWriter"
            },
        }
    },
    "DSA (Python)": {
        "icon": "🟢", "color": "#16a34a",
        "chapters": {
            "1. Arrays & Searching": {
                "theory": "**Linear Search:** O(n) — scan each element\n**Binary Search:** O(log n) — only on sorted array\n```python\ndef binary_search(arr, t):\n    l,h=0,len(arr)-1\n    while l<=h:\n        m=(l+h)//2\n        if arr[m]==t: return m\n        elif arr[m]<t: l=m+1\n        else: h=m-1\n    return -1\n```",
                "example": "```python\ndef binary_search(arr, t):\n    l,h,steps=0,len(arr)-1,0\n    while l<=h:\n        steps+=1; m=(l+h)//2\n        if arr[m]==t: return m,steps\n        elif arr[m]<t: l=m+1\n        else: h=m-1\n    return -1,steps\n\narr=list(range(1,101))\nidx,s=binary_search(arr,73)\nprint(f\"Found at {idx} in {s} steps\")\n# Only ~7 steps vs 73 for linear!\n```",
                "mcq_topic": "DSA linear search binary search complexity"
            },
            "2. Sorting": {
                "theory": "| Algorithm | Average | Worst | Stable |\n|-----------|---------|-------|--------|\n| Bubble | O(n²) | O(n²) | ✅ |\n| Merge | O(n logn) | O(n logn) | ✅ |\n| Quick | O(n logn) | O(n²) | ❌ |\n| Heap | O(n logn) | O(n logn) | ❌ |",
                "example": "```python\ndef merge_sort(arr):\n    if len(arr)<=1: return arr\n    m=len(arr)//2\n    l=merge_sort(arr[:m]); r=merge_sort(arr[m:])\n    res,i,j=[],0,0\n    while i<len(l) and j<len(r):\n        if l[i]<=r[j]: res.append(l[i]);i+=1\n        else: res.append(r[j]);j+=1\n    return res+l[i:]+r[j:]\n\nprint(merge_sort([38,27,43,3,9,82,10]))\n# [3,9,10,27,38,43,82]\n```",
                "mcq_topic": "DSA sorting bubble merge quick complexity"
            },
            "3. Linked List": {
                "theory": "**Singly Linked List** — each node has data + next pointer\n\n| Operation | Array | Linked List |\n|-----------|-------|-------------|\n| Access | O(1) | O(n) |\n| Insert head | O(n) | O(1) |\n| Delete head | O(n) | O(1) |",
                "example": "```python\nclass Node:\n    def __init__(self,d): self.data=d; self.next=None\nclass LL:\n    def __init__(self): self.head=None\n    def insert(self,d):\n        n=Node(d); n.next=self.head; self.head=n\n    def show(self):\n        c=self.head\n        while c: print(c.data,end=\" -> \"); c=c.next\n        print(\"None\")\nll=LL()\nfor v in [1,2,3,4,5]: ll.insert(v)\nll.show()  # 5->4->3->2->1->None\n```",
                "mcq_topic": "DSA linked list singly node insertion"
            },
            "4. Stack & Queue": {
                "theory": "**Stack** — LIFO: `append()` push, `pop()` pop\n**Queue** — FIFO: `append()` enqueue, `popleft()` dequeue\n\n**Stack uses:** Undo/Redo, balanced brackets, function calls\n**Queue uses:** BFS, CPU scheduling, print spooling",
                "example": "```python\n# Balanced brackets using stack\ndef balanced(expr):\n    stk=[]; pairs={')':'(',']':'[','}':'{'}\n    for c in expr:\n        if c in '([{': stk.append(c)\n        elif c in ')]}' :\n            if not stk or stk[-1]!=pairs[c]: return False\n            stk.pop()\n    return not stk\nprint(balanced(\"({[]})\"))  # True\nprint(balanced(\"({[})\"))   # False\n```",
                "mcq_topic": "DSA stack queue LIFO FIFO"
            },
            "5. Trees & Graphs": {
                "theory": "**BST:** Left < Root < Right\n**Traversals:** Inorder(LRR), Preorder(RLL), Postorder(LLR)\n\n**Graph:** Adjacency List O(V+E)\n- BFS — O(V+E) shortest unweighted path\n- DFS — O(V+E) cycle detection",
                "example": "```python\nclass BST:\n    def __init__(self,v): self.v=v; self.l=self.r=None\n    def insert(self,v):\n        if v<self.v:\n            if self.l: self.l.insert(v)\n            else: self.l=BST(v)\n        else:\n            if self.r: self.r.insert(v)\n            else: self.r=BST(v)\n    def inorder(self):\n        return (self.l.inorder() if self.l else [])+[self.v]+(self.r.inorder() if self.r else [])\nroot=BST(50)\nfor v in [30,70,20,40,60,80]: root.insert(v)\nprint(root.inorder())  # sorted!\n```",
                "mcq_topic": "DSA BST tree traversal graph BFS DFS"
            },
            "6. Dynamic Programming": {
                "theory": "**DP** = Recursion + Memoization\n**Two approaches:** Top-down (memoization), Bottom-up (tabulation)\n**Key problems:** Fibonacci, 0/1 Knapsack, LCS, LIS, Coin Change\n\n**Overlapping subproblems + Optimal substructure** → use DP",
                "example": "```python\n# 0/1 Knapsack — O(n*W)\ndef knapsack(weights, values, W):\n    n = len(weights)\n    dp = [[0]*(W+1) for _ in range(n+1)]\n    for i in range(1, n+1):\n        for w in range(W+1):\n            dp[i][w] = dp[i-1][w]\n            if weights[i-1] <= w:\n                dp[i][w] = max(dp[i][w],\n                    values[i-1] + dp[i-1][w-weights[i-1]])\n    return dp[n][W]\n\nprint(knapsack([2,3,4,5],[3,4,5,6], 8))  # 10\n```",
                "mcq_topic": "DSA dynamic programming memoization tabulation knapsack"
            },
            "7. Heap & Priority Queue": {
                "theory": "**Min-Heap:** parent ≤ children (root = minimum)\n**Max-Heap:** parent ≥ children (root = maximum)\n\n**Operations:** Insert O(log n), Extract-min/max O(log n), Heapify O(n)\n\n**Uses:** Priority queue, Dijkstra, Prim's, K largest elements, Heap sort",
                "example": "```python\nimport heapq\n\n# Min-heap (default in Python)\nheap = []\nfor val in [5, 3, 8, 1, 9, 2]:\n    heapq.heappush(heap, val)\nprint([heapq.heappop(heap) for _ in range(3)])  # [1,2,3]\n\n# K largest elements\ndef k_largest(nums, k):\n    return heapq.nlargest(k, nums)\n\nnums = [3, 2, 1, 5, 6, 4]\nprint(k_largest(nums, 3))  # [6, 5, 4]\n```",
                "mcq_topic": "DSA heap priority queue min-heap max-heap heapify"
            },
            "8. Hashing & Hash Maps": {
                "theory": "**Hash Function** maps key → index in O(1) average\n**Collision Resolution:**\n- Chaining (linked list at index)\n- Open Addressing (linear probing, quadratic)\n\n**Load Factor** = n/m; resize when > 0.75\n**Python dict** = hash map; average O(1) get/set/delete",
                "example": "```python\n# Two Sum — O(n) using hash map\ndef two_sum(nums, target):\n    seen = {}  # value -> index\n    for i, n in enumerate(nums):\n        complement = target - n\n        if complement in seen:\n            return [seen[complement], i]\n        seen[n] = i\n    return []\n\nprint(two_sum([2,7,11,15], 9))   # [0, 1]\nprint(two_sum([3,2,4], 6))       # [1, 2]\n\n# Frequency counter\nfrom collections import Counter\nwords = ['cat','dog','cat','bird','dog','cat']\nprint(Counter(words).most_common(2))  # [('cat',3),('dog',2)]\n```",
                "mcq_topic": "DSA hashing hash map collision resolution load factor"
            },
        }
    },
    "SQL": {
        "icon": "🔴", "color": "#dc2626",
        "chapters": {
            "1. DDL Commands": {
                "theory": "**SQL Types:** DDL, DML, DQL, DCL, TCL\n\n```sql\nCREATE TABLE Students(\n    roll INT PRIMARY KEY,\n    name VARCHAR(50) NOT NULL,\n    cgpa DECIMAL(3,2),\n    branch VARCHAR(30)\n);\nALTER TABLE Students ADD email VARCHAR(50);\nDROP TABLE Students;\n```",
                "example": "```sql\nCREATE DATABASE MentoraAI;\nUSE MentoraAI;\nCREATE TABLE Students(\n    roll INT PRIMARY KEY AUTO_INCREMENT,\n    name VARCHAR(50) NOT NULL,\n    branch VARCHAR(30),\n    cgpa DECIMAL(3,2) CHECK(cgpa BETWEEN 0 AND 10)\n);\nINSERT INTO Students(name,branch,cgpa)\nVALUES('Aryan','CS',9.10),('Sara','EC',8.50);\nSELECT * FROM Students;\n```",
                "mcq_topic": "SQL DDL CREATE ALTER DROP constraints"
            },
            "2. SELECT & DML": {
                "theory": "```sql\nSELECT col FROM table\nWHERE condition\nGROUP BY col HAVING condition\nORDER BY col DESC LIMIT n;\n```\n**Aggregates:** `COUNT SUM AVG MAX MIN`\n**Operators:** `BETWEEN IN LIKE IS NULL`",
                "example": "```sql\nSELECT name,cgpa FROM Students WHERE cgpa>=9.0;\nSELECT branch, COUNT(*) AS total, AVG(cgpa) AS avg_cgpa\nFROM Students\nGROUP BY branch HAVING AVG(cgpa)>8\nORDER BY avg_cgpa DESC;\nSELECT * FROM Students WHERE name LIKE 'A%';\nSELECT * FROM Students\nORDER BY cgpa DESC LIMIT 3;\n```",
                "mcq_topic": "SQL SELECT WHERE GROUP BY aggregate functions"
            },
            "3. JOINs": {
                "theory": "**INNER JOIN** — matching rows both tables\n**LEFT JOIN** — all left + matching right\n**RIGHT JOIN** — all right + matching left\n**FULL JOIN** — all rows both\n\n```sql\nSELECT a.col, b.col\nFROM A INNER JOIN B ON A.key=B.key;\n```",
                "example": "```sql\n-- Students with department name\nSELECT s.name, s.cgpa, d.dept_name\nFROM Students s\nINNER JOIN Departments d ON s.dept_id=d.dept_id;\n\n-- LEFT JOIN: show all students\nSELECT s.name,\n       COALESCE(d.dept_name,'No Dept') AS dept\nFROM Students s\nLEFT JOIN Departments d ON s.dept_id=d.dept_id;\n```",
                "mcq_topic": "SQL INNER LEFT RIGHT JOIN types"
            },
            "4. Subqueries & Views": {
                "theory": "**Subquery** — query inside query\n```sql\nSELECT name FROM Students\nWHERE cgpa > (SELECT AVG(cgpa) FROM Students);\n```\n**View** — virtual table\n```sql\nCREATE VIEW TopStudents AS\nSELECT name, cgpa FROM Students WHERE cgpa >= 9.0;\nSELECT * FROM TopStudents;\n```\n**Correlated subquery** — references outer query",
                "example": "```sql\n-- Subquery: students above average CGPA\nSELECT name, cgpa\nFROM Students\nWHERE cgpa > (SELECT AVG(cgpa) FROM Students)\nORDER BY cgpa DESC;\n\n-- EXISTS subquery\nSELECT name FROM Students s\nWHERE EXISTS (\n    SELECT 1 FROM Enrollments e\n    WHERE e.student_id = s.roll\n);\n\n-- View\nCREATE VIEW BranchSummary AS\nSELECT branch, COUNT(*) as count, ROUND(AVG(cgpa),2) as avg_cgpa\nFROM Students GROUP BY branch;\n```",
                "mcq_topic": "SQL subqueries views EXISTS correlated"
            },
            "5. Stored Procedures & Triggers": {
                "theory": "**Stored Procedure:**\n```sql\nDELIMITER //\nCREATE PROCEDURE GetToppers(IN min_cgpa FLOAT)\nBEGIN\n    SELECT * FROM Students WHERE cgpa >= min_cgpa;\nEND //\nCALL GetToppers(9.0);\n```\n**Trigger:** Auto-executes on INSERT/UPDATE/DELETE",
                "example": "```sql\n-- Stored Procedure with OUT param\nDELIMITER //\nCREATE PROCEDURE GetBranchAvg(\n    IN branch_name VARCHAR(30),\n    OUT avg_result FLOAT)\nBEGIN\n    SELECT AVG(cgpa) INTO avg_result\n    FROM Students WHERE branch=branch_name;\nEND //\nCALL GetBranchAvg('CS', @result);\nSELECT @result;\n\n-- Trigger: log updates\nCREATE TRIGGER after_cgpa_update\nAFTER UPDATE ON Students\nFOR EACH ROW\nINSERT INTO AuditLog(student_id, old_cgpa, new_cgpa, changed_at)\nVALUES(OLD.roll, OLD.cgpa, NEW.cgpa, NOW());\n```",
                "mcq_topic": "SQL stored procedures triggers DELIMITER"
            },
            "6. Indexing & Normalization": {
                "theory": "**Index** — speeds up SELECT, slows INSERT/UPDATE\n```sql\nCREATE INDEX idx_cgpa ON Students(cgpa);\nCREATE UNIQUE INDEX idx_email ON Students(email);\n```\n**Normalization:**\n- **1NF** — atomic values, no repeating groups\n- **2NF** — 1NF + no partial dependency\n- **3NF** — 2NF + no transitive dependency\n- **BCNF** — every determinant is a candidate key",
                "example": "```sql\n-- Check query plan with index\nEXPLAIN SELECT * FROM Students WHERE cgpa > 8.5;\n\n-- Composite index\nCREATE INDEX idx_branch_cgpa ON Students(branch, cgpa);\n\n-- Normalization example: decompose\n-- Unnormalized: Orders(order_id, customer_name, customer_city, product, qty)\n-- 3NF: Customers(cust_id, name, city)\n--      Orders(order_id, cust_id, product_id, qty)\n--      Products(product_id, name, price)\n```",
                "mcq_topic": "SQL indexing normalization 1NF 2NF 3NF BCNF"
            },
        }
    },
    "JavaScript": {
        "icon": "🔵", "color": "#0284c7",
        "chapters": {
            "1. Basics & Functions": {
                "theory": "```javascript\nlet name = \"MENTORA\";  // block scoped\nconst PI = 3.14;        // constant\nvar x = 10;             // function scoped\n\n// Arrow function\nconst square = x => x*x;\nconst add = (a,b) => a+b;\n```\n**Types:** number, string, boolean, null, undefined, object",
                "example": "```javascript\nconst marks = [85,92,78,95,88];\nconst avg = marks.reduce((a,b)=>a+b,0)/marks.length;\nconst passed = marks.filter(m=>m>=80);\nconst grades = marks.map(m=>m>=90?'A':'B');\nconsole.log(`Avg:${avg.toFixed(1)}`);\nconsole.log('Passed:',passed);\nconsole.log('Grades:',grades);\nconst [first,...rest] = marks;\nconsole.log(first, rest);\n```",
                "mcq_topic": "JavaScript variables functions arrow const let"
            },
            "2. Async & Promises": {
                "theory": "**Callback** → **Promise** → **Async/Await**\n```javascript\nasync function getData(url) {\n    try {\n        const res = await fetch(url);\n        const data = await res.json();\n        return data;\n    } catch(err) {\n        console.error(err);\n    }\n}\n```",
                "example": "```javascript\nasync function fetchStudent(id) {\n    try {\n        const res = await fetch(`/api/students/${id}`);\n        if(!res.ok) throw new Error(res.status);\n        const student = await res.json();\n        console.log(`${student.name}: ${student.cgpa}`);\n        return student;\n    } catch(e) {\n        console.error('Error:',e.message);\n    }\n}\n// Promise.all — parallel requests\nPromise.all([fetch('/api/a'), fetch('/api/b')])\n    .then(responses => Promise.all(responses.map(r=>r.json())))\n    .then(([a,b]) => console.log(a,b));\n```",
                "mcq_topic": "JavaScript async await promises fetch API"
            },
            "3. DOM Manipulation": {
                "theory": "```javascript\n// Select elements\nconst el = document.getElementById('id');\nconst els = document.querySelectorAll('.class');\n// Modify\nel.textContent = 'New text';\nel.style.color = 'red';\nel.classList.add('active');\n// Create/append\nconst div = document.createElement('div');\ndocument.body.appendChild(div);\n// Events\nel.addEventListener('click', handler);\n```",
                "example": "```javascript\n// Dynamic todo list\nfunction addTask(text) {\n    const li = document.createElement('li');\n    li.textContent = text;\n    const btn = document.createElement('button');\n    btn.textContent = 'Delete';\n    btn.onclick = () => li.remove();\n    li.appendChild(btn);\n    document.getElementById('list').appendChild(li);\n}\ndocument.getElementById('add').addEventListener('click', () => {\n    const val = document.getElementById('input').value;\n    if(val.trim()) addTask(val);\n});\n```",
                "mcq_topic": "JavaScript DOM manipulation events querySelector"
            },
            "4. ES6+ Features": {
                "theory": "**Destructuring:**\n```javascript\nconst {name, age} = student;\nconst [first, ...rest] = arr;\n```\n**Spread/Rest:**\n```javascript\nconst merged = {...obj1, ...obj2};\nfunction sum(...nums){ return nums.reduce((a,b)=>a+b,0); }\n```\n**Template Literals, Optional Chaining, Nullish Coalescing:**\n```javascript\nconst val = obj?.prop?.nested ?? 'default';\n```",
                "example": "```javascript\n// Destructuring + default values\nconst { name='Unknown', cgpa=0, branch='CS' } = student;\n// Object spread (immutable update)\nconst updated = { ...student, cgpa: 9.5 };\n// Array methods chaining\nconst topStudents = students\n    .filter(s => s.cgpa >= 9.0)\n    .sort((a,b) => b.cgpa - a.cgpa)\n    .slice(0, 3)\n    .map(({name, cgpa}) => `${name}: ${cgpa}`);\nconsole.log(topStudents);\n```",
                "mcq_topic": "JavaScript ES6 destructuring spread rest optional chaining"
            },
            "5. OOP in JavaScript": {
                "theory": "```javascript\nclass Animal {\n    constructor(name) { this.name = name; }\n    speak() { return `${this.name} makes a sound`; }\n}\nclass Dog extends Animal {\n    speak() { return `${this.name} barks!`; }\n}\n```\n**Prototype chain:** All objects inherit from `Object.prototype`",
                "example": "```javascript\nclass BankAccount {\n    #balance = 0;  // private field\n    constructor(owner, initial=0) {\n        this.owner = owner;\n        this.#balance = initial;\n    }\n    deposit(amt) { this.#balance += amt; return this; }\n    withdraw(amt) {\n        if(amt > this.#balance) throw new Error('Insufficient funds');\n        this.#balance -= amt; return this;\n    }\n    get balance() { return this.#balance; }\n}\nconst acc = new BankAccount('Aryan', 1000);\nacc.deposit(500).withdraw(200);\nconsole.log(acc.balance); // 1300\n```",
                "mcq_topic": "JavaScript classes OOP prototype inheritance"
            },
            "6. Node.js & Modules": {
                "theory": "**CommonJS (Node):**\n```javascript\nconst fs = require('fs');\nmodule.exports = { func };\n```\n**ES Modules:**\n```javascript\nimport { func } from './module.js';\nexport const PI = 3.14;\n```\n**Event Loop:** Single-threaded, non-blocking I/O via libuv\n**npm:** `npm init`, `npm install express`, `package.json`",
                "example": "```javascript\n// Simple Express server\nconst express = require('express');\nconst app = express();\napp.use(express.json());\nconst students = [];\napp.get('/students', (req, res) => res.json(students));\napp.post('/students', (req, res) => {\n    students.push(req.body);\n    res.status(201).json(req.body);\n});\napp.listen(3000, () => console.log('Server running on port 3000'));\n```",
                "mcq_topic": "JavaScript Node.js Express modules npm event loop"
            },
        }
    },
    "R Programming": {
        "icon": "🟦", "color": "#1d6fa5",
        "chapters": {
            "1. R Basics & Data Types": {
                "theory": "**R** is a language for statistical computing and graphics.\n\n**Data Types:**\n```r\nx <- 42L          # integer\ny <- 3.14         # numeric\nname <- \"MENTORA\" # character\nflag <- TRUE      # logical\ncx <- 2+3i        # complex\n```\n**Key functions:** `class()`, `typeof()`, `is.numeric()`, `as.character()`\n\n**Vectors** (R's most basic structure):\n```r\nmarks <- c(85, 92, 78, 95, 88)\nmarks[1]          # 85 (1-indexed!)\nmarks[marks > 80] # filter\n```",
                "example": "```r\n# Student data example\nnames  <- c(\"Aryan\",\"Sara\",\"Rahul\")\ncgpa   <- c(9.1, 8.5, 7.8)\nbranch <- c(\"CS\",\"EC\",\"ME\")\n\ncat(\"Students:\", length(names), \"\\n\")\ncat(\"Avg CGPA:\", mean(cgpa), \"\\n\")\ncat(\"Max CGPA:\", max(cgpa), \"\\n\")\ncat(\"Toppers:\", names[cgpa >= 9.0], \"\\n\")\n```",
                "mcq_topic": "R programming basics data types vectors assignment operator"
            },
            "2. Data Structures in R": {
                "theory": "**Matrix:**\n```r\nm <- matrix(1:9, nrow=3, ncol=3)\n```\n**Data Frame** (most used for data analysis):\n```r\ndf <- data.frame(\n  name=c(\"A\",\"B\",\"C\"),\n  score=c(85,90,78),\n  pass=c(T,T,T)\n)\ndf$score       # column access\ndf[1,]         # row access\n```\n**List** (mixed types):\n```r\nstudent <- list(name=\"Aryan\", cgpa=9.1, subjects=c(\"OS\",\"DS\"))\nstudent$name   # access by name\n```\n**Factor** (categorical):\n```r\ngrades <- factor(c(\"A\",\"B\",\"A\",\"C\"))\nlevels(grades)\n```",
                "example": "```r\n# Working with a data frame\ndf <- data.frame(\n  subject = c(\"DBMS\",\"OS\",\"CN\",\"DS\"),\n  marks   = c(88, 75, 92, 85),\n  credits = c(4, 4, 3, 4)\n)\ncat(\"Pass count:\", sum(df$marks >= 40), \"\\n\")\ncat(\"Avg Marks:\", mean(df$marks), \"\\n\")\ncat(\"Best:\",      df$subject[which.max(df$marks)], \"\\n\")\n# Add a new column\ndf$grade <- ifelse(df$marks >= 90, \"A\", ifelse(df$marks >= 75, \"B\", \"C\"))\nprint(df)\n```",
                "mcq_topic": "R matrix data frame list factor structure"
            },
            "3. Control Flow & Functions": {
                "theory": "**Conditionals:**\n```r\nif (cgpa >= 9.0) {\n  cat(\"Distinction\")\n} else if (cgpa >= 7.5) {\n  cat(\"First Class\")\n} else {\n  cat(\"Pass\")\n}\n```\n**Loops:**\n```r\nfor (i in 1:5) { cat(i, \"\") }\nwhile (x > 0) { x <- x - 1 }\n```\n**Functions:**\n```r\ncalc_gpa <- function(marks, credits) {\n  sum(marks * credits) / sum(credits)\n}\nresult <- calc_gpa(c(85,90), c(4,3))\n```\n**apply family:** `sapply()`, `lapply()`, `apply()`",
                "example": "```r\n# Grade calculator function\nget_grade <- function(marks) {\n  sapply(marks, function(m) {\n    if (m >= 90) \"O\"\n    else if (m >= 80) \"A+\"\n    else if (m >= 70) \"A\"\n    else if (m >= 60) \"B+\"\n    else if (m >= 50) \"B\"\n    else \"F\"\n  })\n}\nmarks <- c(95, 83, 72, 61, 45)\ngrades <- get_grade(marks)\ncat(\"Grades:\", grades, \"\\n\")\ncat(\"Pass rate:\", mean(marks >= 50)*100, \"%\\n\")\n```",
                "mcq_topic": "R functions control flow if else for loop apply sapply"
            },
            "4. Data Manipulation with dplyr": {
                "theory": "**dplyr** is the go-to package for data manipulation.\n```r\nlibrary(dplyr)\n```\n**Key verbs:**\n- `filter()` — select rows\n- `select()` — select columns\n- `mutate()` — add/transform columns\n- `summarise()` — aggregate\n- `arrange()` — sort\n- `group_by()` — group for aggregation\n\n**Pipe operator `%>%`** (or `|>` in R 4.1+):\n```r\ndf %>% filter(score > 80) %>% arrange(desc(score))\n```",
                "example": "```r\nlibrary(dplyr)\nstudents <- data.frame(\n  name   = c(\"Aryan\",\"Sara\",\"Rahul\",\"Priya\",\"Dev\"),\n  branch = c(\"CS\",\"EC\",\"CS\",\"IT\",\"EC\"),\n  cgpa   = c(9.1, 8.5, 7.8, 9.3, 8.1)\n)\n# Branch-wise summary\nstudents %>%\n  group_by(branch) %>%\n  summarise(\n    count    = n(),\n    avg_cgpa = mean(cgpa),\n    toppers  = sum(cgpa >= 9.0)\n  ) %>%\n  arrange(desc(avg_cgpa))\n```",
                "mcq_topic": "R dplyr filter select mutate summarise pipe operator"
            },
            "5. Data Visualisation with ggplot2": {
                "theory": "**ggplot2** uses a layered *Grammar of Graphics*.\n```r\nlibrary(ggplot2)\nggplot(data=df, aes(x=var1, y=var2)) +\n  geom_point() +\n  geom_line() +\n  labs(title=\"My Plot\", x=\"X axis\", y=\"Y axis\") +\n  theme_minimal()\n```\n**Common geoms:**\n- `geom_bar()` — bar chart\n- `geom_histogram()` — distribution\n- `geom_boxplot()` — box plot\n- `geom_point()` — scatter plot\n- `geom_line()` — line chart\n\n**`aes()`** maps data columns to visual properties (x, y, color, size).",
                "example": "```r\nlibrary(ggplot2)\ndf <- data.frame(\n  subject = c(\"DS\",\"DBMS\",\"OS\",\"CN\",\"Algo\"),\n  marks   = c(88,75,92,85,79)\n)\nggplot(df, aes(x=reorder(subject,-marks), y=marks, fill=subject)) +\n  geom_bar(stat=\"identity\", width=0.6) +\n  geom_hline(yintercept=80, linetype=\"dashed\", color=\"red\") +\n  labs(title=\"Subject-wise Marks\",\n       x=\"Subject\", y=\"Marks\") +\n  theme_minimal() +\n  theme(legend.position=\"none\")\n```",
                "mcq_topic": "R ggplot2 visualisation geom aes layers grammar of graphics"
            },
            "6. Statistics & Data Analysis": {
                "theory": "**Descriptive Statistics:**\n```r\nmean(x); median(x); sd(x); var(x)\nquantile(x, 0.25)   # Q1\nsummary(x)          # full summary\n```\n**Hypothesis Testing:**\n```r\nt.test(x, mu=70)          # one-sample t-test\nt.test(x, y)              # two-sample\ncor.test(x, y)            # correlation\nchisq.test(table(a, b))   # chi-square\n```\n**Linear Regression:**\n```r\nmodel <- lm(cgpa ~ attendance + study_hours, data=df)\nsummary(model)\npredict(model, newdata=data.frame(attendance=80, study_hours=5))\n```",
                "example": "```r\nset.seed(42)\nmarks_A <- c(85,88,92,79,95,87,91,83)\nmarks_B <- c(78,82,75,88,80,77,85,79)\n\ncat(\"Group A mean:\", mean(marks_A), \"\\n\")\ncat(\"Group B mean:\", mean(marks_B), \"\\n\")\ncat(\"Group A SD:  \", sd(marks_A), \"\\n\")\n\n# t-test to compare groups\nresult <- t.test(marks_A, marks_B)\ncat(\"p-value:\", result$p.value, \"\\n\")\nif(result$p.value < 0.05) {\n  cat(\"Significant difference between groups!\\n\")\n} else {\n  cat(\"No significant difference.\\n\")\n}\n```",
                "mcq_topic": "R statistics t-test hypothesis testing regression correlation"
            },
            "7. File I/O & String Handling": {
                "theory": "**Read/Write CSV:**\n```r\ndf <- read.csv(\"data.csv\", stringsAsFactors=FALSE)\nwrite.csv(df, \"output.csv\", row.names=FALSE)\n```\n**Read Excel:** `readxl::read_excel(\"file.xlsx\")`\n\n**String functions:**\n```r\nnchar(\"MENTORA\")           # 7\ntoupper(\"hello\")           # \"HELLO\"\nsubstr(\"Hello\",1,3)        # \"Hel\"\npaste(\"A\",\"B\",sep=\"-\")    # \"A-B\"\ngsub(\"o\",\"0\",\"hello\")     # \"hell0\"\ngrepl(\"CS\",branches)       # logical vector\n```\n**stringr** package:\n```r\nlibrary(stringr)\nstr_detect(\"MENTORA AI\", \"AI\")   # TRUE\nstr_replace(\"Hello\", \"l\", \"L\")  # \"HeLlo\"\n```",
                "example": "```r\n# Parse and clean student names\nraw <- c(\" aryan sharma \",\"SARA  ALI\",\"rahul.mehta\")\nclean <- trimws(raw)             # remove spaces\nclean <- toupper(clean)          # uppercase\nclean <- gsub(\"\\\\.\",\" \",clean)  # replace dots\ncat(\"Cleaned:\", clean, \"\\n\")\n\n# Count characters per name\ncharcount <- nchar(clean)\ncat(\"Lengths:\", charcount, \"\\n\")\ncat(\"Longest name:\", clean[which.max(charcount)], \"\\n\")\n```",
                "mcq_topic": "R file IO CSV read write string manipulation gsub paste"
            },
            "8. R for Machine Learning": {
                "theory": "**caret** package — unified ML interface:\n```r\nlibrary(caret)\n# Train/test split\nset.seed(42)\nidx <- createDataPartition(df$target, p=0.8, list=FALSE)\ntrain <- df[idx,]; test <- df[-idx,]\n# Train model\nmodel <- train(target~., data=train, method=\"rf\")\n# Predict\npreds <- predict(model, test)\nconfusionMatrix(preds, test$target)\n```\n**Popular algorithms in R:**\n- `lm()` / `glm()` — linear/logistic regression\n- `rpart` — decision trees\n- `randomForest` — random forest\n- `e1071` — SVM, Naive Bayes\n- `xgboost` — gradient boosting",
                "example": "```r\n# Simple logistic regression example\nset.seed(42)\nn <- 100\nstudy_hours  <- rnorm(n, mean=5, sd=2)\nattendance   <- rnorm(n, mean=75, sd=10)\npass <- as.factor(ifelse(study_hours*0.4 + attendance*0.06 + rnorm(n,0,1) > 7, 1, 0))\ndf <- data.frame(study_hours, attendance, pass)\n\nmodel <- glm(pass ~ study_hours + attendance,\n             data=df, family=binomial)\nsummary(model)$coefficients\n# Prediction for new student\nnew_student <- data.frame(study_hours=6, attendance=80)\nprob <- predict(model, new_student, type=\"response\")\ncat(\"Pass probability:\", round(prob,3), \"\\n\")\n```",
                "mcq_topic": "R machine learning caret logistic regression random forest classification"
            },
        }
    },
}

# ─────────────────────────────────────────────
# USERS for login
# ─────────────────────────────────────────────
USERS = {"admin": "mentora123", "student": "student123", "demo": "demo123"}

def show_login():

    # ── Feature pills
    st.markdown("""
    <div class="features-strip">
        <span class="feature-pill">📊 Academic Tracker</span>
        <span class="feature-pill">💻 Coding Practice</span>
        <span class="feature-pill">🤖 AI Powered</span>
        <span class="feature-pill">🎓 CGPA Estimator</span>
        <span class="feature-pill">📄 PDF Reports</span>
    </div>
    <br>
    """, unsafe_allow_html=True)

    # ── Login card
    _, mid, _ = st.columns([1, 2, 1])
    with mid:
        st.markdown("""
        <div class="login-card">
            <div class="login-card-title">🔐 Welcome Back</div>
            <div class="login-card-sub">Sign in to continue your learning journey</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

        uname = st.text_input("👤 Username", placeholder="Enter your username", key="li_user")
        pwd   = st.text_input("🔒 Password", type="password", placeholder="Enter your password", key="li_pass")

        st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)

        if st.button("🚀 Sign In", key="login_btn", use_container_width=True):
            if uname.strip() == "" or pwd.strip() == "":
                st.warning("⚠️ Please enter both username and password.")
            elif uname in USERS and USERS[uname] == pwd:
                st.session_state.logged_in = True
                st.session_state.login_username = uname
                st.success(f"✅ Welcome, {uname.title()}!")
                st.rerun()
            else:
                st.error("❌ Invalid username or password. Please try again.")

        st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)

        if st.button("👁️ Quick Demo Login", key="demo_btn", use_container_width=True):
            st.session_state.logged_in = True
            st.session_state.login_username = "demo"
            st.rerun()

        st.markdown("""
        <div class="demo-box">
            <b>🔑 Demo Credentials</b><br>
            Username: <code>demo</code> &nbsp;/&nbsp; Password: <code>demo123</code><br>
            Admin: <code>admin</code> &nbsp;/&nbsp; Password: <code>mentora123</code>
        </div>
        """, unsafe_allow_html=True)

def _card_mini(col, icon, title, desc, color, mode):
    """Compact card for Group 2 & 3 features on home screen."""
    with col:
        st.markdown(f"""
        <div style="background:linear-gradient(145deg,#{color}ee,#{color}cc);
        border-radius:18px;padding:20px 14px 16px;text-align:center;
        box-shadow:0 8px 24px rgba(0,0,0,0.15);border:1px solid rgba(255,255,255,0.2);
        min-height:160px;">
        <span style="font-size:2.4rem;display:block;margin-bottom:8px;">{icon}</span>
        <div style="font-size:1rem;font-weight:700;color:#fff;margin-bottom:5px;">{title}</div>
        <div style="font-size:0.75rem;color:rgba(255,255,255,0.88);line-height:1.5;">{desc}</div>
        </div>""", unsafe_allow_html=True)
        st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)
        if st.button(f"Open →", key=f"btn_{mode}", use_container_width=True):
            st.session_state.app_mode = mode
            st.rerun()

def show_home():

    # ── Section heading
    st.markdown("""
    <div style="text-align:center; margin: 0 0 20px 0;">
        <h3 style="font-family:Poppins,sans-serif; color:#4c1d95; font-size:1.1rem;
        font-weight:600; margin:0; letter-spacing:1px;">
        ✦ &nbsp; CHOOSE YOUR LEARNING PATH &nbsp; ✦</h3>
    </div>
    """, unsafe_allow_html=True)

    _, mid, _ = st.columns([0.3, 3, 0.3])
    with mid:
        # ── Row 1: 3 cards
        col1, col2, col3 = st.columns(3, gap="large")

        with col1:
            st.markdown("""
            <div class="path-card-purple">
                <span class="card-icon">📊</span>
                <div class="card-title">Academic Tracker</div>
                <div class="card-features card-features-purple">
                    🎯 Auto Weak Subject Detection<br>
                    📝 IA1 &amp; IA2 Marks Analysis<br>
                    🗓️ 30-Day Personalised Study Plan<br>
                    🎓 CGPA Estimator<br>
                    🤖 AI Feedback &amp; PDF Report
                </div>
                <span class="card-badge">LLaMA 3.3 70B</span>
                <span class="card-badge">10 Branches</span>
            </div>
            """, unsafe_allow_html=True)
            st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)
            if st.button("📊 Open Academic Tracker →", key="btn_tracker", use_container_width=True):
                st.session_state.app_mode = "tracker"; st.rerun()

        with col2:
            st.markdown("""
            <div class="path-card-cyan">
                <span class="card-icon">💻</span>
                <div class="card-title">Coding Practice</div>
                <div class="card-features card-features-cyan">
                    🔵 C Programming — 10 Chapters<br>
                    🟣 C++ with OOP — 4 Chapters<br>
                    🟡 Python — 5 Chapters<br>
                    🟠 Java — 3 Chapters<br>
                    🟢 DSA, SQL &amp; JavaScript
                </div>
                <span class="card-badge">Theory</span>
                <span class="card-badge">Examples</span>
                <span class="card-badge">AI MCQs</span>
            </div>
            """, unsafe_allow_html=True)
            st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)
            if st.button("💻 Open Coding Practice →", key="btn_coding", use_container_width=True):
                st.session_state.app_mode = "coding"; st.rerun()

        with col3:
            st.markdown("""
            <div style="background:linear-gradient(145deg,#059669,#047857,#065f46);
            border-radius:24px;padding:30px 20px 24px 20px;text-align:center;
            box-shadow:0 12px 40px rgba(5,150,105,0.35);border:1px solid rgba(255,255,255,0.2);">
                <span style="font-size:3.4rem;margin-bottom:12px;display:block;">🗓️</span>
                <div style="font-size:1.2rem;font-weight:700;color:#ffffff;margin:0 0 10px 0;">Daily Schedule</div>
                <div style="font-size:0.78rem;line-height:1.8;margin:0 0 14px 0;color:#ffffff;">
                    📋 Create daily timetable<br>⏰ Set time slots<br>
                    ✅ Track task completion<br>📅 View any day's plan
                </div>
                <span style="background:rgba(255,255,255,0.22);border-radius:20px;padding:3px 10px;font-size:0.72rem;color:#fff;margin:2px;display:inline-block;">Tasks</span>
                <span style="background:rgba(255,255,255,0.22);border-radius:20px;padding:3px 10px;font-size:0.72rem;color:#fff;margin:2px;display:inline-block;">Timetable</span>
            </div>
            """, unsafe_allow_html=True)
            st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)
            if st.button("🗓️ Open Daily Schedule →", key="btn_schedule", use_container_width=True):
                st.session_state.app_mode = "schedule"; st.rerun()

        st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)

        # ── Row 2: 2 cards centred
        _, c4, c5, _ = st.columns([0.5, 2, 2, 0.5], gap="large")

        with c4:
            st.markdown("""
            <div style="background:linear-gradient(145deg,#dc2626,#b91c1c,#991b1b);
            border-radius:24px;padding:30px 20px 24px 20px;text-align:center;
            box-shadow:0 12px 40px rgba(220,38,38,0.35);border:1px solid rgba(255,255,255,0.2);">
                <span style="font-size:3.4rem;margin-bottom:12px;display:block;">📝</span>
                <div style="font-size:1.2rem;font-weight:700;color:#ffffff;margin:0 0 10px 0;">Subject Test</div>
                <div style="font-size:0.78rem;line-height:1.8;margin:0 0 14px 0;color:#ffffff;">
                    🏫 All Engineering Branches<br>📚 Any Subject you choose<br>
                    🔢 Custom MCQ count<br>⏱️ Timed Practice Test<br>
                    📊 Score &amp; Review
                </div>
                <span style="background:rgba(255,255,255,0.22);border-radius:20px;padding:3px 10px;font-size:0.72rem;color:#fff;margin:2px;display:inline-block;">AI Generated</span>
                <span style="background:rgba(255,255,255,0.22);border-radius:20px;padding:3px 10px;font-size:0.72rem;color:#fff;margin:2px;display:inline-block;">All Branches</span>
            </div>
            """, unsafe_allow_html=True)
            st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)
            if st.button("📝 Open Subject Test →", key="btn_subtest", use_container_width=True):
                st.session_state.app_mode = "subtest"; st.rerun()

        with c5:
            st.markdown("""
            <div style="background:linear-gradient(145deg,#d97706,#b45309,#92400e);
            border-radius:24px;padding:30px 20px 24px 20px;text-align:center;
            box-shadow:0 12px 40px rgba(217,119,6,0.35);border:1px solid rgba(255,255,255,0.2);">
                <span style="font-size:3.4rem;margin-bottom:12px;display:block;">🎯</span>
                <div style="font-size:1.2rem;font-weight:700;color:#ffffff;margin:0 0 10px 0;">GATE Preparation</div>
                <div style="font-size:0.78rem;line-height:1.8;margin:0 0 14px 0;color:#ffffff;">
                    📅 90-Day Fixed Timetable<br>🤖 AI Exam Date Planner<br>
                    📆 Weekly Topic Schedule<br>⏰ Daily Study Hours Plan<br>
                    🏅 All GATE Branches
                </div>
                <span style="background:rgba(255,255,255,0.22);border-radius:20px;padding:3px 10px;font-size:0.72rem;color:#fff;margin:2px;display:inline-block;">GATE 2026</span>
                <span style="background:rgba(255,255,255,0.22);border-radius:20px;padding:3px 10px;font-size:0.72rem;color:#fff;margin:2px;display:inline-block;">AI Planner</span>
            </div>
            """, unsafe_allow_html=True)
            st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)
            if st.button("🎯 Open GATE Prep →", key="btn_gate", use_container_width=True):
                st.session_state.app_mode = "gate"; st.rerun()

    # ── Row 3 heading: Group 2
    st.markdown("""
    <div style="text-align:center;margin:28px 0 10px;">
    <h3 style="font-family:Poppins,sans-serif;color:#4c1d95;font-size:0.95rem;
    font-weight:600;margin:0;letter-spacing:1px;">
    🎓 &nbsp; CAREER &amp; PERFORMANCE &nbsp; 🎓</h3></div>
    """, unsafe_allow_html=True)

    _, mid2, _ = st.columns([0.3, 3, 0.3])
    with mid2:
        g2c1, g2c2, g2c3, g2c4 = st.columns(4, gap="medium")
        _card_mini(g2c1, "🎯", "Mock Interview", "AI technical & HR rounds","#6d28d9","interview")
        _card_mini(g2c2, "📝", "Notes Organiser", "Create · Tag · AI Summary","#0e7490","notes")
        _card_mini(g2c3, "📈", "CGPA Calculator", "Semester grades · Predictor","#047857","cgpa")
        _card_mini(g2c4, "🏆", "Leaderboard", "Class ranking · Peer scores","#b91c1c","leaderboard")

    # ── Row 4 heading: Group 3
    st.markdown("""
    <div style="text-align:center;margin:24px 0 10px;">
    <h3 style="font-family:Poppins,sans-serif;color:#4c1d95;font-size:0.95rem;
    font-weight:600;margin:0;letter-spacing:1px;">
    📋 &nbsp; EXAM TOOLS &nbsp; 📋</h3></div>
    """, unsafe_allow_html=True)

    _, mid3, _ = st.columns([0.3, 3, 0.3])
    with mid3:
        g3c1, g3c2, g3c3, g3c4 = st.columns(4, gap="medium")
        _card_mini(g3c1, "📅", "Exam Countdown", "Days left · AI prep tips","#4f46e5","countdown")
        _card_mini(g3c2, "🗂️", "PYQ Bank", "Previous year papers + solutions","#0891b2","pyq")
        _card_mini(g3c3, "💊", "Syllabus Tracker", "Tick topics · Track coverage","#059669","syllabus")
        _card_mini(g3c4, "🔔", "Smart Reminders", "AI daily study reminders","#b45309","reminders")

    # ── Footer
    st.markdown("""
    <div style="text-align:center; margin-top:24px; padding:14px;
    background: linear-gradient(90deg,#f5f3ff,#e0f2fe,#f5f3ff);
    border-radius:14px; border:1px solid #ddd6fe;">
        <span style="font-size:0.8rem; color:#7c3aed; letter-spacing:1px;">
        🚀 &nbsp; Powered by <b>Groq LLaMA 3.3 70B</b> &nbsp;·&nbsp;
        Built with <b>Python &amp; Streamlit</b> &nbsp;·&nbsp; <b>MENTORA AI</b> © 2025
        </span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)
    _, lc, _ = st.columns([3, 1, 3])
    if lc.button("🚪 Logout", key="logout_home", use_container_width=True):
        st.session_state.logged_in = False
        st.session_state.app_mode = None
        st.rerun()

def show_coding():
    # Nav bar
    ncol1, _, ncol3 = st.columns([1, 4, 1])
    if st.session_state.coding_chapter:
        if ncol1.button("← Chapters", key="bk_chap"):
            st.session_state.coding_chapter = None
            st.session_state.code_mcqs = []
            st.session_state.code_mcq_score = None
            st.rerun()
        if ncol3.button("🏠 Home", key="home_coding_top"):
            st.session_state.app_mode = None
            st.session_state.coding_lang = None
            st.session_state.coding_chapter = None
            st.rerun()
    elif st.session_state.coding_lang:
        if ncol1.button("← Languages", key="bk_lang"):
            st.session_state.coding_lang = None
            st.session_state.coding_chapter = None
            st.rerun()
        if ncol3.button("🏠 Home", key="home_coding_lang"):
            st.session_state.app_mode = None
            st.session_state.coding_lang = None
            st.rerun()
    else:
        if ncol1.button("🏠 Home", key="bk_home2"):
            st.session_state.app_mode = None; st.rerun()

    # LEVEL 1 — Language grid
    if not st.session_state.coding_lang:
        st.markdown("""<h2 style="text-align:center;font-family:Poppins,sans-serif;color:#4c1d95;margin:4px 0 4px 0;">
        💻 Coding Practice</h2>
        <p style="text-align:center;color:#6b7280;font-family:Poppins,sans-serif;margin:0 0 20px 0;">
        Select a programming language</p>""", unsafe_allow_html=True)
        cols = st.columns(4)
        for i, (lang, info) in enumerate(CODING_CONTENT.items()):
            with cols[i % 4]:
                st.markdown(f"""<div style="background:linear-gradient(135deg,{info['color']}18,{info['color']}08);
                border:2px solid {info['color']}44;border-radius:14px;padding:18px 10px;
                text-align:center;margin-bottom:4px;min-height:120px;">
                <div style="font-size:2.4rem;">{info['icon']}</div>
                <h4 style="color:{info['color']};font-family:Poppins,sans-serif;margin:6px 0 3px 0;font-size:0.88rem;">
                {lang}</h4>
                <p style="color:#9ca3af;font-size:0.73rem;margin:0;">{len(info['chapters'])} chapters</p>
                </div>""", unsafe_allow_html=True)
                if st.button(f"Open", key=f"lang_{i}", use_container_width=True):
                    st.session_state.coding_lang = lang; st.rerun()

    # LEVEL 2 — Chapter list
    elif not st.session_state.coding_chapter:
        lang = st.session_state.coding_lang
        info = CODING_CONTENT[lang]
        st.markdown(f"""<div style="background:linear-gradient(90deg,{info['color']},{info['color']}88);
        border-radius:14px;padding:14px 22px;margin-bottom:18px;">
        <h2 style="color:#fff;font-family:Poppins,sans-serif;margin:0;">{info['icon']} {lang} — Chapters</h2>
        </div>""", unsafe_allow_html=True)
        for idx, (chap, _) in enumerate(info["chapters"].items()):
            c1, c2 = st.columns([5, 1])
            c1.markdown(f"""<div style="background:#fff;border:1.5px solid {info['color']}44;
            border-left:5px solid {info['color']};border-radius:10px;
            padding:12px 16px;margin-bottom:4px;">
            <b style="color:#1e1e2e;font-family:Poppins,sans-serif;">{chap}</b></div>""",
            unsafe_allow_html=True)
            if c2.button("Open →", key=f"ch_{idx}", use_container_width=True):
                st.session_state.coding_chapter = chap
                st.session_state.code_mcqs = []; st.session_state.code_mcq_score = None; st.rerun()
            st.markdown("<div style='height:1px'></div>", unsafe_allow_html=True)

    # LEVEL 3 — Chapter content
    else:
        lang    = st.session_state.coding_lang
        chap    = st.session_state.coding_chapter
        info    = CODING_CONTENT[lang]
        content = info["chapters"][chap]
        st.markdown(f"""<div style="background:linear-gradient(90deg,{info['color']},{info['color']}88);
        border-radius:12px;padding:12px 20px;margin-bottom:14px;">
        <h3 style="color:#fff;font-family:Poppins,sans-serif;margin:0;">{info['icon']} {chap}</h3>
        </div>""", unsafe_allow_html=True)

        t1, t2, t3 = st.tabs(["📖 Theory", "💡 Example", "🧠 MCQ Practice"])

        with t1:
            st.markdown(content["theory"])
        with t2:
            st.markdown("### 💡 Code Example")
            st.markdown(content["example"])
        with t3:
            st.markdown("### 🧠 AI MCQ Practice")
            st.caption(f"Topic: {content['mcq_topic']}")
            if not st.session_state.code_mcqs:
                if st.button("🎲 Generate 5 MCQs", key="gen_code_mcq", use_container_width=True):
                    with st.spinner("Generating MCQs …"):
                        mcqs = get_mcqs(chap, n=5, type_label="coding", topic=content["mcq_topic"])
                        st.session_state.code_mcqs = mcqs; st.session_state.code_mcq_score = None; st.rerun()
            elif st.session_state.code_mcq_score is None:
                with st.form("code_form"):
                    ans = {}
                    for i, q in enumerate(st.session_state.code_mcqs):
                        st.markdown(f"**Q{i+1}. {q['question']}**")
                        ans[i] = st.radio(f"Q{i+1}", q["options"], key=f"cq{i}", label_visibility="collapsed")
                        st.divider()
                    if st.form_submit_button("✅ Submit", use_container_width=True):
                        sc = sum(1 for i,q in enumerate(st.session_state.code_mcqs) if is_correct(ans[i],q["answer"]))
                        st.session_state.code_mcq_score = sc; st.rerun()
            else:
                sc = st.session_state.code_mcq_score; tot = len(st.session_state.code_mcqs)
                pct = sc/tot*100
                col = "#16a34a" if pct>=80 else "#d97706" if pct>=60 else "#dc2626"
                em  = "🏆" if pct>=80 else "📈" if pct>=60 else "📚"
                st.markdown(f"""<div style="background:{col}18;border:2px solid {col}44;
                border-radius:14px;padding:18px;text-align:center;margin-bottom:14px;">
                <div style="font-size:2.2rem;">{em}</div>
                <h2 style="color:{col};font-family:Poppins,sans-serif;margin:6px 0;">
                {sc}/{tot} Correct ({pct:.0f}%)</h2>
                <p style="color:#6b7280;margin:0;">{'Excellent!' if pct>=80 else 'Good effort! Review theory.' if pct>=60 else 'Keep practising!'}</p>
                </div>""", unsafe_allow_html=True)
                st.markdown("""<div style='background:#f5f3ff;border:1.5px solid #c4b5fd;
                border-radius:12px;padding:10px 16px;margin:8px 0 4px 0;'>
                <b style='color:#4c1d95;font-family:Poppins,sans-serif;'>📋 Correct Answers</b>
                </div>""", unsafe_allow_html=True)
                for i, q in enumerate(st.session_state.code_mcqs):
                    st.markdown(f"**Q{i+1}.** {q['question']}")
                    st.success(f"✅ **{q['answer']}**")
                    st.divider()
                if st.button("🔄 Try Again", key="retry_code", use_container_width=True):
                    st.session_state.code_mcqs = []; st.session_state.code_mcq_score = None; st.rerun()

def show_schedule():
    # ── Top nav
    n1, _, n3 = st.columns([1, 4, 1])
    if n1.button("🏠 Home", key="sched_home"):
        st.session_state.app_mode = None; st.rerun()
    if n3.button("🚪 Logout", key="sched_logout"):
        st.session_state.logged_in = False
        st.session_state.app_mode = None; st.rerun()

    # ── Header
    st.markdown("""
    <div style="background:linear-gradient(90deg,#059669,#047857,#0891b2);
    border-radius:14px;padding:16px 24px;margin-bottom:20px;
    box-shadow:0 6px 24px rgba(5,150,105,0.3);">
    <h2 style="color:#fff;font-family:Poppins,sans-serif;margin:0;font-size:1.4rem;">
    🗓️ Daily Schedule Manager</h2>
    <p style="color:#a7f3d0;font-family:Poppins,sans-serif;margin:4px 0 0 0;font-size:0.83rem;">
    Create your timetable · Add tasks · Track your day</p>
    </div>
    """, unsafe_allow_html=True)

    # ── Date selector
    dc1, dc2 = st.columns([1, 2])
    with dc1:
        selected_date = st.date_input("📅 Select Date", value=datetime.today(), key="sched_date_pick")
    date_str = str(selected_date)
    st.session_state.schedule_date = date_str

    # Init date key
    if date_str not in st.session_state.schedule_tasks:
        st.session_state.schedule_tasks[date_str] = []

    tasks = st.session_state.schedule_tasks[date_str]

    # ── Summary stats
    total = len(tasks)
    done  = sum(1 for t in tasks if t.get("done"))
    pct   = int(done / total * 100) if total > 0 else 0

    s1, s2, s3, s4 = st.columns(4)
    s1.markdown(f"""<div style="background:#fff;border:2px solid #059669;border-radius:14px;
    padding:14px;text-align:center;box-shadow:0 4px 12px rgba(5,150,105,0.1);">
    <h2 style="color:#059669;font-family:Poppins,sans-serif;margin:0;">{total}</h2>
    <p style="color:#6b7280;margin:4px 0 0 0;font-size:0.8rem;">Total Tasks</p></div>""",
    unsafe_allow_html=True)
    s2.markdown(f"""<div style="background:#fff;border:2px solid #2563eb;border-radius:14px;
    padding:14px;text-align:center;box-shadow:0 4px 12px rgba(37,99,235,0.1);">
    <h2 style="color:#2563eb;font-family:Poppins,sans-serif;margin:0;">{done}</h2>
    <p style="color:#6b7280;margin:4px 0 0 0;font-size:0.8rem;">Completed</p></div>""",
    unsafe_allow_html=True)
    s3.markdown(f"""<div style="background:#fff;border:2px solid #d97706;border-radius:14px;
    padding:14px;text-align:center;box-shadow:0 4px 12px rgba(217,119,6,0.1);">
    <h2 style="color:#d97706;font-family:Poppins,sans-serif;margin:0;">{total - done}</h2>
    <p style="color:#6b7280;margin:4px 0 0 0;font-size:0.8rem;">Remaining</p></div>""",
    unsafe_allow_html=True)
    s4.markdown(f"""<div style="background:#fff;border:2px solid #7c3aed;border-radius:14px;
    padding:14px;text-align:center;box-shadow:0 4px 12px rgba(124,58,237,0.1);">
    <h2 style="color:#7c3aed;font-family:Poppins,sans-serif;margin:0;">{pct}%</h2>
    <p style="color:#6b7280;margin:4px 0 0 0;font-size:0.8rem;">Done</p></div>""",
    unsafe_allow_html=True)

    # Progress bar
    if total > 0:
        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
        st.progress(pct / 100)
        st.caption(f"✅ {done} of {total} tasks completed for {selected_date.strftime('%A, %d %B %Y')}")

    st.divider()

    # ── Add New Task
    st.markdown("""<div style="background:#f0fdf4;border:2px solid #bbf7d0;border-radius:14px;
    padding:16px 20px;margin-bottom:16px;">
    <h4 style="color:#065f46;font-family:Poppins,sans-serif;margin:0 0 12px 0;">
    ➕ Add New Task</h4></div>""", unsafe_allow_html=True)

    ac1, ac2, ac3 = st.columns([2, 1, 1])
    with ac1:
        task_name = st.text_input("📝 Task / Subject", placeholder="e.g. Study DBMS Chapter 3", key="new_task_name")
    with ac2:
        time_slot = st.selectbox("⏰ Time Slot", [
            "6:00 AM – 7:00 AM",
            "7:00 AM – 8:00 AM",
            "8:00 AM – 9:00 AM",
            "9:00 AM – 10:00 AM",
            "10:00 AM – 11:00 AM",
            "11:00 AM – 12:00 PM",
            "12:00 PM – 1:00 PM",
            "1:00 PM – 2:00 PM",
            "2:00 PM – 3:00 PM",
            "3:00 PM – 4:00 PM",
            "4:00 PM – 5:00 PM",
            "5:00 PM – 6:00 PM",
            "6:00 PM – 7:00 PM",
            "7:00 PM – 8:00 PM",
            "8:00 PM – 9:00 PM",
            "9:00 PM – 10:00 PM",
        ], key="new_task_time")
    with ac3:
        priority = st.selectbox("🔥 Priority", ["🔴 High", "🟡 Medium", "🟢 Low"], key="new_task_priority")

    ac4, ac5 = st.columns([3, 1])
    with ac4:
        task_note = st.text_input("📌 Notes (optional)", placeholder="e.g. Focus on SQL joins", key="new_task_note")
    with ac5:
        st.markdown("<div style='height:28px'></div>", unsafe_allow_html=True)
        if st.button("➕ Add Task", key="add_task_btn", use_container_width=True):
            if task_name.strip():
                st.session_state.schedule_tasks[date_str].append({
                    "task":     task_name.strip(),
                    "time":     time_slot,
                    "priority": priority,
                    "note":     task_note.strip(),
                    "done":     False,
                    "id":       datetime.now().strftime("%H%M%S%f")
                })
                st.success(f"✅ Task '{task_name}' added!")
                st.rerun()
            else:
                st.warning("⚠️ Please enter a task name.")

    st.divider()

    # ── Task List
    if not tasks:
        st.markdown("""<div style="text-align:center;padding:40px;background:#f9fafb;
        border:2px dashed #d1d5db;border-radius:16px;">
        <div style="font-size:3rem;">📋</div>
        <h3 style="color:#9ca3af;font-family:Poppins,sans-serif;">No tasks yet!</h3>
        <p style="color:#d1d5db;font-family:Poppins,sans-serif;font-size:0.85rem;">
        Add your first task above to start planning your day 🚀</p>
        </div>""", unsafe_allow_html=True)
    else:
        st.markdown(f"""<h4 style="font-family:Poppins,sans-serif;color:#065f46;margin:0 0 12px 0;">
        📋 Tasks for {selected_date.strftime('%A, %d %B %Y')}</h4>""", unsafe_allow_html=True)

        # Sort by time slot
        sorted_tasks = sorted(enumerate(tasks), key=lambda x: x[1]["time"])

        for orig_idx, task in sorted_tasks:
            done    = task.get("done", False)
            pri     = task.get("priority", "🟡 Medium")
            pri_col = "#dc2626" if "High" in pri else "#d97706" if "Medium" in pri else "#16a34a"
            bg      = "#f0fdf4" if done else "#ffffff"
            border  = "#bbf7d0" if done else "#e5e7eb"
            opacity = "0.6" if done else "1"

            tc1, tc2 = st.columns([6, 1])
            with tc1:
                st.markdown(f"""
                <div style="background:{bg};border:1.5px solid {border};border-radius:14px;
                padding:14px 18px;margin-bottom:6px;opacity:{opacity};
                border-left:5px solid {pri_col};">
                    <div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;">
                        <div>
                            <span style="font-family:Poppins,sans-serif;font-weight:700;
                            color:#1e1e2e;font-size:0.95rem;
                            {'text-decoration:line-through;color:#9ca3af;' if done else ''}">
                            {'✅ ' if done else '⬜ '}{task['task']}</span>
                            <span style="margin-left:10px;background:{pri_col}22;color:{pri_col};
                            border-radius:8px;padding:2px 10px;font-size:0.72rem;
                            font-family:Poppins,sans-serif;font-weight:600;">{pri}</span>
                        </div>
                        <span style="font-family:Poppins,sans-serif;font-size:0.8rem;
                        color:#7c3aed;font-weight:600;">⏰ {task['time']}</span>
                    </div>
                    {f'<p style="color:#6b7280;font-size:0.78rem;font-family:Poppins,sans-serif;margin:6px 0 0 0;">📌 {task["note"]}</p>' if task.get("note") else ''}
                </div>
                """, unsafe_allow_html=True)

            with tc2:
                st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)
                done_label = "↩️ Undo" if done else "✅ Done"
                if st.button(done_label, key=f"done_{date_str}_{orig_idx}", use_container_width=True):
                    st.session_state.schedule_tasks[date_str][orig_idx]["done"] = not done
                    st.rerun()
                if st.button("🗑️ Del", key=f"del_{date_str}_{orig_idx}", use_container_width=True):
                    st.session_state.schedule_tasks[date_str].pop(orig_idx)
                    st.rerun()

        # ── Clear all button
        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
        _, clrcol, _ = st.columns([3, 1, 3])
        if clrcol.button("🗑️ Clear All Tasks", key="clear_all_tasks", use_container_width=True):
            st.session_state.schedule_tasks[date_str] = []
            st.rerun()



# ─────────────────────────────────────────────
# SUBJECT TEST
# ─────────────────────────────────────────────
BRANCH_SUBJECTS = {
    "Computer Engineering":       ["Data Structures","DBMS","Operating Systems","Computer Networks","Theory of Computation","Compiler Design","Software Engineering","Computer Architecture","Algorithms","Digital Logic"],
    "Information Technology":     ["Web Development","Network Security","Cloud Computing","Data Mining","Information Systems","Software Testing","IoT","Big Data","Cyber Security","Human Computer Interaction"],
    "Electronics & Communication":["Signals & Systems","Analog Circuits","Digital Electronics","Communication Systems","Microprocessors","VLSI Design","Electromagnetic Theory","Control Systems","Antenna Theory","DSP"],
    "Electrical Engineering":     ["Circuit Theory","Power Systems","Electrical Machines","Control Systems","Power Electronics","Measurement & Instrumentation","High Voltage Engg","Utilization of Electrical Energy","Switchgear","Electric Drives"],
    "Mechanical Engineering":     ["Engineering Thermodynamics","Fluid Mechanics","Manufacturing Processes","Machine Design","Heat Transfer","Theory of Machines","Strength of Materials","Industrial Engineering","Automobile Engg","Refrigeration & AC"],
    "Civil Engineering":          ["Structural Analysis","Concrete Technology","Geotechnical Engg","Transportation Engg","Fluid Mechanics","Surveying","Environmental Engg","Steel Structures","Construction Management","Hydrology"],
    "Chemical Engineering":       ["Mass Transfer","Heat Transfer","Reaction Engineering","Fluid Mechanics","Process Control","Thermodynamics","Separation Processes","Process Economics","Polymer Technology","Biochemical Engg"],
    "Biotechnology Engineering":  ["Molecular Biology","Genetics","Biochemistry","Microbiology","Cell Biology","Immunology","Bioprocess Engg","Bioinformatics","Genetic Engg","Enzyme Technology"],
    "Artificial Intelligence & ML":["Machine Learning","Deep Learning","NLP","Computer Vision","Reinforcement Learning","Data Science","Neural Networks","AI Ethics","Knowledge Representation","Pattern Recognition"],
    "Data Science":               ["Statistics","Machine Learning","Data Visualization","Big Data Analytics","Python for DS","SQL & Databases","Feature Engineering","Time Series","Recommender Systems","Data Mining"],
}

def show_subtest():
    n1, _, n3 = st.columns([1,4,1])
    if n1.button("🏠 Home", key="st_home"): st.session_state.app_mode = None; st.rerun()
    if n3.button("🚪 Logout", key="st_logout"): st.session_state.logged_in=False; st.session_state.app_mode=None; st.rerun()

    st.markdown("""
    <div style="background:linear-gradient(90deg,#dc2626,#b91c1c,#7f1d1d);
    border-radius:14px;padding:16px 24px;margin-bottom:20px;
    box-shadow:0 6px 24px rgba(220,38,38,0.3);">
    <h2 style="color:#fff;margin:0;font-size:1.4rem;">📝 Subject Test — All Engineering Branches</h2>
    <p style="color:#fecaca;margin:4px 0 0 0;font-size:0.83rem;">Choose your branch · Select subject · Set MCQ count · Take AI test</p>
    </div>""", unsafe_allow_html=True)

    # ── Setup panel (only if no test running)
    if not st.session_state.subtest_mcqs:
        sc1, sc2, sc3, sc4 = st.columns([2,2,1,1])
        with sc1:
            branch = st.selectbox("🏫 Engineering Branch", list(BRANCH_SUBJECTS.keys()), key="st_branch")
            st.session_state.subtest_branch = branch
        with sc2:
            subj = st.selectbox("📚 Select Subject", BRANCH_SUBJECTS[branch], key="st_subj")
            st.session_state.subtest_subject = subj
        with sc3:
            num_q = st.number_input("🔢 No. of MCQs", min_value=5, max_value=50, value=10, step=5, key="st_numq")
            st.session_state.subtest_num_q = num_q
        with sc4:
            st.markdown("<div style='height:28px'></div>", unsafe_allow_html=True)
            if st.button("🚀 Start Test", key="st_start", use_container_width=True):
                with st.spinner(f"Generating {num_q} MCQs on {subj}..."):
                    mcqs = get_mcqs(subj, n=num_q, type_label="subject test", topic=subj)
                    if mcqs:
                        st.session_state.subtest_mcqs    = mcqs
                        st.session_state.subtest_score   = None
                        st.session_state.subtest_answers = {}
                        st.rerun()
                    else:
                        st.error("MCQ generation failed. Try again.")

        # ── Info cards
        st.markdown("<br>", unsafe_allow_html=True)
        ic1, ic2, ic3, ic4 = st.columns(4)
        for col, icon, title, desc in [
            (ic1,"🏫","10 Branches","All engineering branches covered"),
            (ic2,"📚","Any Subject","Pick any subject from the list"),
            (ic3,"🔢","Custom Count","5 to 50 MCQs per test"),
            (ic4,"🤖","AI Generated","Fresh questions every time"),
        ]:
            col.markdown(f"""<div style="background:#fff;border:2px solid #fecaca;border-radius:14px;
            padding:16px;text-align:center;box-shadow:0 4px 12px rgba(220,38,38,0.08);">
            <div style="font-size:2rem;">{icon}</div>
            <b style="color:#b91c1c;font-size:0.9rem;">{title}</b>
            <p style="color:#6b7280;font-size:0.75rem;margin:4px 0 0 0;">{desc}</p>
            </div>""", unsafe_allow_html=True)

    # ── Test in progress
    elif st.session_state.subtest_score is None:
        subj = st.session_state.subtest_subject
        mcqs = st.session_state.subtest_mcqs
        st.markdown(f"""<div style="background:#fff;border:2px solid #fecaca;border-radius:14px;
        padding:12px 20px;margin-bottom:14px;display:flex;justify-content:space-between;align-items:center;">
        <span style="font-weight:700;color:#b91c1c;font-size:1rem;">📝 {subj} Test</span>
        <span style="color:#6b7280;font-size:0.85rem;">🔢 {len(mcqs)} Questions</span>
        </div>""", unsafe_allow_html=True)

        with st.form("subtest_form"):
            ans_list = []
            for i, q in enumerate(mcqs):
                st.markdown(f"**Q{i+1}. {q['question']}**")
                chosen = st.radio(f"Q{i+1}", q["options"], key=f"sta_{i}", label_visibility="collapsed")
                ans_list.append(chosen)
                st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)
                st.divider()
            if st.form_submit_button("✅ Submit Test", use_container_width=True):
                score = 0
                for i, q in enumerate(mcqs):
                    if is_correct(ans_list[i], q["answer"]): score += 1
                st.session_state.subtest_score = score
                st.session_state.subtest_answers = {i: ans_list[i] for i in range(len(mcqs))}
                st.rerun()

    # ── Results
    else:
        sc    = st.session_state.subtest_score
        tot   = len(st.session_state.subtest_mcqs)
        pct   = sc / tot * 100
        col   = "#16a34a" if pct>=80 else "#d97706" if pct>=60 else "#dc2626"
        emoji = "🏆" if pct>=80 else "📈" if pct>=60 else "📚"
        grade = "Excellent!" if pct>=80 else "Good Effort!" if pct>=60 else "Need More Practice"

        st.markdown(f"""<div style="background:{col}18;border:3px solid {col};
        border-radius:20px;padding:28px;text-align:center;margin-bottom:20px;">
        <div style="font-size:3rem;">{emoji}</div>
        <h1 style="color:{col};margin:8px 0 4px 0;">{sc}/{tot} &nbsp;({pct:.1f}%)</h1>
        <h3 style="color:{col};margin:0 0 8px 0;">{grade}</h3>
        <p style="color:#6b7280;margin:0;">Subject: <b>{st.session_state.subtest_subject}</b> &nbsp;|&nbsp;
        Branch: <b>{st.session_state.subtest_branch}</b></p>
        </div>""", unsafe_allow_html=True)

        st.markdown("""<div style="background:#f5f3ff;border:1.5px solid #c4b5fd;
        border-radius:12px;padding:10px 16px;margin-bottom:8px;">
        <b style="color:#4c1d95;">📋 Answer Key</b></div>""", unsafe_allow_html=True)
        for i, q in enumerate(st.session_state.subtest_mcqs):
            ans = st.session_state.get(f"sta_{i}", "")
            correct = is_correct(ans, q["answer"])
            bg = "#f0fdf4" if correct else "#fef2f2"
            bd = "#16a34a" if correct else "#dc2626"
            st.markdown(f"""<div style="background:{bg};border-left:4px solid {bd};
            border-radius:8px;padding:10px 14px;margin-bottom:6px;">
            <b>Q{i+1}.</b> {q['question']}<br>
            <span style="color:#16a34a;">✅ Correct: {q['answer']}</span>
            {'<br><span style="color:#dc2626;">❌ Your answer: '+ans+'</span>' if not correct and ans else ''}
            </div>""", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        rc1, rc2 = st.columns(2)
        if rc1.button("🔄 New Test (Same Subject)", key="st_retry", use_container_width=True):
            st.session_state.subtest_mcqs  = []
            st.session_state.subtest_score = None
            st.rerun()
        if rc2.button("🆕 Change Subject", key="st_new", use_container_width=True):
            st.session_state.subtest_mcqs    = []
            st.session_state.subtest_score   = None
            st.session_state.subtest_subject = ""
            st.rerun()


# ─────────────────────────────────────────────
# GATE PREPARATION
# ─────────────────────────────────────────────
GATE_SUBJECTS = {
    "CSE": ["Engineering Mathematics","Digital Logic","Computer Organization","Programming & DS","Algorithms","Theory of Computation","Compiler Design","Operating Systems","Databases","Computer Networks"],
    "ECE": ["Engineering Mathematics","Networks","Electronic Devices","Analog Circuits","Digital Circuits","Signals & Systems","Control Systems","Communications","Electromagnetics","Engineering Mathematics"],
    "EE":  ["Engineering Mathematics","Electric Circuits","Electromagnetic Fields","Signals & Systems","Electrical Machines","Power Systems","Control Systems","Power Electronics","Analog Electronics","Digital Electronics"],
    "ME":  ["Engineering Mathematics","Applied Mechanics","Strength of Materials","Theory of Machines","Vibrations","Machine Design","Fluid Mechanics","Heat Transfer","Thermodynamics","Manufacturing"],
    "CE":  ["Engineering Mathematics","Structural Mechanics","Concrete Structures","Steel Structures","Geotechnical Engg","Fluid Mechanics","Hydrology","Transportation Engg","Environmental Engg","Surveying"],
    "IN":  ["Engineering Mathematics","Electrical Circuits","Signals & Systems","Control Systems","Analog Electronics","Digital Electronics","Measurements","Sensors & Transducers","Communication","Biomedical Instrumentation"],
    "CH":  ["Engineering Mathematics","Process Calculations","Thermodynamics","Fluid Mechanics","Heat Transfer","Mass Transfer","Chemical Reaction Engg","Instrumentation","Plant Design","Polymer Technology"],
    "BT":  ["Engineering Mathematics","Microbiology","Biochemistry","Molecular Biology","Bioprocess Engg","Downstream Processing","Immunology","Cell Biology","Bioinformatics","Recombinant DNA Technology"],
}

GATE_DAILY_HOURS = {
    "Morning Study":   "6:00 AM – 8:00 AM",
    "Concept Learning":"9:00 AM – 12:00 PM",
    "Practice Problems":"2:00 PM – 5:00 PM",
    "Revision":        "7:00 PM – 9:00 PM",
    "Mock Test/PYQ":   "9:00 PM – 10:30 PM",
}

def build_90day_timetable(branch):
    subjects = GATE_SUBJECTS.get(branch, GATE_SUBJECTS["CSE"])
    timetable = {}
    days_per_subject = 90 // len(subjects)
    day = 1
    for subj in subjects:
        for _ in range(days_per_subject):
            if day > 90: break
            timetable[day] = subj
            day += 1
    while day <= 90:
        timetable[day] = "Full Revision & Mock Tests"
        day += 1
    return timetable

def show_gate():
    n1, _, n3 = st.columns([1,4,1])
    if n1.button("🏠 Home", key="gate_home"): st.session_state.app_mode = None; st.rerun()
    if n3.button("🚪 Logout", key="gate_logout"): st.session_state.logged_in=False; st.session_state.app_mode=None; st.rerun()

    st.markdown("""
    <div style="background:linear-gradient(90deg,#d97706,#b45309,#78350f);
    border-radius:14px;padding:16px 24px;margin-bottom:20px;
    box-shadow:0 6px 24px rgba(217,119,6,0.3);">
    <h2 style="color:#fff;margin:0;font-size:1.4rem;">🎯 GATE Preparation Planner</h2>
    <p style="color:#fde68a;margin:4px 0 0 0;font-size:0.83rem;">90-Day Plan · AI Planner · Weekly Schedule · Daily Hours</p>
    </div>""", unsafe_allow_html=True)

    # ── Branch + Exam Date selector
    gc1, gc2 = st.columns([2, 2])
    with gc1:
        gate_branch = st.selectbox("🎓 GATE Branch", list(GATE_SUBJECTS.keys()), key="gate_branch_sel",
            format_func=lambda x: f"{x} — {'Computer Science' if x=='CSE' else 'Electronics' if x=='ECE' else 'Electrical' if x=='EE' else 'Mechanical' if x=='ME' else 'Civil' if x=='CE' else 'Instrumentation' if x=='IN' else 'Chemical' if x=='CH' else 'Biotechnology'}")
        st.session_state.gate_branch = gate_branch
    with gc2:
        exam_date = st.date_input("📅 GATE Exam Date", value=dt_date(2026, 2, 1), key="gate_exam_date_sel")
        days_left = (exam_date - dt_date.today()).days
        if days_left > 0:
            st.success(f"⏳ {days_left} days left for GATE!")
        elif days_left == 0:
            st.warning("🎯 GATE is TODAY! Best of luck!")
        else:
            st.error(f"⚠️ GATE date was {abs(days_left)} days ago")

    st.divider()

    # ── 4 Tabs
    tab1, tab2, tab3, tab4 = st.tabs(["📅 90-Day Timetable","🤖 AI Exam Planner","📆 Weekly Schedule","⏰ Daily Study Hours"])

    # ── TAB 1: 90-Day Fixed Timetable
    with tab1:
        st.markdown(f"### 📅 90-Day GATE {gate_branch} Timetable")
        timetable = build_90day_timetable(gate_branch)
        subjects  = GATE_SUBJECTS[gate_branch]
        colors    = ["#7c3aed","#0891b2","#059669","#dc2626","#d97706","#4f46e5","#db2777","#65a30d","#0e7490","#9333ea"]
        subj_color = {s: colors[i % len(colors)] for i, s in enumerate(subjects + ["Full Revision & Mock Tests"])}

        # Show as weekly blocks
        for week in range(1, 14):
            start_day = (week-1)*7 + 1
            end_day   = min(week*7, 90)
            wdays     = {d: timetable[d] for d in range(start_day, end_day+1) if d in timetable}
            st.markdown(f"**📌 Week {week} (Day {start_day}–{end_day})**")
            wcols = st.columns(7)
            for i, (d, subj) in enumerate(wdays.items()):
                col   = subj_color.get(subj, "#6b7280")
                wcols[i % 7].markdown(f"""<div style="background:{col};border-radius:8px;
                padding:6px 4px;text-align:center;margin-bottom:4px;min-height:60px;">
                <div style="color:#fff;font-size:0.65rem;font-weight:700;">Day {d}</div>
                <div style="color:#fff;font-size:0.58rem;line-height:1.3;word-break:break-word;white-space:normal;">{subj}</div>
                </div>""", unsafe_allow_html=True)
            st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)

        # Subject legend
        st.divider()
        st.markdown("**🎨 Subject Legend:**")
        leg_cols = st.columns(5)
        for i, subj in enumerate(subjects):
            col = subj_color.get(subj, "#6b7280")
            leg_cols[i%5].markdown(f"""<div style="background:{col};border-radius:8px;
            padding:5px 8px;text-align:center;margin-bottom:4px;">
            <span style="color:#fff;font-size:0.72rem;font-weight:600;">{subj}</span>
            </div>""", unsafe_allow_html=True)

    # ── TAB 2: AI Exam Date Planner
    with tab2:
        st.markdown("### 🤖 AI-Generated Exam Date Study Plan")
        if days_left <= 0:
            st.warning("⚠️ Please set a future GATE exam date to generate an AI plan.")
        else:
            ai_plan_key = f"gate_ai_{gate_branch}_{days_left}"
            already_generated = st.session_state.gate_timetable.get("ai_key") == ai_plan_key

            if not already_generated:
                if st.button("🤖 Generate AI Study Plan", key="gate_ai_btn", use_container_width=True):
                    with st.spinner("AI is creating your personalised GATE study plan..."):
                        try:
                            prompt = (
                                f"Create a detailed GATE {gate_branch} study plan for a student with exactly {days_left} days left. "
                                f"GATE subjects: {', '.join(GATE_SUBJECTS[gate_branch])}. "
                                f"Divide the days into phases: Foundation, Deep Study, Practice, Revision, Mock Tests. "
                                f"For each phase give: phase name, duration in days, subjects to cover, daily hours, key tips. "
                                f"Format as clear sections. Be specific and actionable."
                            )
                            messages = [{"role": "system", "content": "You are an expert GATE exam coach."}, {"role": "user", "content": prompt}]
                            r_raw = safe_chat(messages, temperature=0.4, max_tokens=1500)
                            if r_raw is None: raise Exception("AI service unavailable. Check API key.")
                            class _R: pass
                            r = _R()
                            class _C: pass
                            r.choices = [_C()]
                            r.choices[0].message = _C()
                            r.choices[0].message.content = r_raw
                            plan_text = r.choices[0].message.content.strip()
                            st.session_state.gate_timetable["ai_plan"] = plan_text
                            st.session_state.gate_timetable["ai_key"]  = ai_plan_key
                            st.rerun()
                        except Exception as e:
                            st.error(f"AI plan generation failed: {e}")

            if "ai_plan" in st.session_state.gate_timetable and already_generated:
                if st.button("🔄 Regenerate Plan", key="gate_ai_regen", use_container_width=False):
                    st.session_state.gate_timetable.pop("ai_plan", None)
                    st.session_state.gate_timetable.pop("ai_key", None)
                    st.rerun()
                st.markdown(f"""<div style="background:#fffbeb;border:2px solid #fcd34d;
                border-radius:14px;padding:20px;color:#1e1e2e;line-height:1.8;">
                {st.session_state.gate_timetable['ai_plan'].replace(chr(10),'<br>')}
                </div>""", unsafe_allow_html=True)

    # ── TAB 3: Weekly Schedule
    with tab3:
        st.markdown("### 📆 Weekly Topic Schedule")
        subjects = GATE_SUBJECTS[gate_branch]
        weeks    = ["Week 1","Week 2","Week 3","Week 4","Week 5","Week 6","Week 7","Week 8","Week 9","Week 10","Week 11","Week 12"]
        days_wk  = ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"]

        for wi, week in enumerate(weeks):
            # Each week focus on 1 main subject + revision
            main_subj = subjects[wi % len(subjects)]
            rev_subj  = subjects[(wi-1) % len(subjects)] if wi > 0 else "Foundation Review"
            st.markdown(f"#### 📌 {week} — Focus: **{main_subj}**")
            day_cols = st.columns(7)
            schedule_map = {
                "Mon": f"📖 {main_subj[:20]}\nNew Concepts",
                "Tue": f"📖 {main_subj[:20]}\nDeep Study",
                "Wed": f"✏️ {main_subj[:20]}\nPractice Problems",
                "Thu": f"✏️ {main_subj[:20]}\nPYQ Practice",
                "Fri": f"🔁 {rev_subj[:20]}\nRevision",
                "Sat": f"🧪 Full Syllabus\nMock Test",
                "Sun": f"📋 Weekly\nRevision",
            }
            day_colors = {"Mon":"#7c3aed","Tue":"#4f46e5","Wed":"#0891b2","Thu":"#059669","Fri":"#d97706","Sat":"#dc2626","Sun":"#9333ea"}
            for di, day in enumerate(days_wk):
                c = day_colors[day]
                text = schedule_map[day]
                day_cols[di].markdown(f"""<div style="background:{c};border-radius:10px;
                padding:8px 5px;text-align:center;min-height:90px;">
                <div style="color:#fff;font-weight:700;font-size:0.78rem;">{day}</div>
                <div style="color:#fff;font-size:0.65rem;line-height:1.5;margin-top:4px;word-break:break-word;white-space:normal;">{text.replace(chr(10),'<br>')}</div>
                </div>""", unsafe_allow_html=True)
            st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

    # ── TAB 4: Daily Study Hours
    with tab4:
        st.markdown("### ⏰ Recommended Daily Study Hours Plan")

        # Daily hours summary
        total_hrs = 9.5
        st.markdown(f"""<div style="background:linear-gradient(135deg,#fffbeb,#fef3c7);
        border:2px solid #fcd34d;border-radius:16px;padding:18px;text-align:center;margin-bottom:20px;">
        <h2 style="color:#d97706;margin:0;">⏰ {total_hrs} Hours/Day</h2>
        <p style="color:#6b7280;margin:4px 0 0 0;font-size:0.85rem;">Recommended daily study time for GATE preparation</p>
        </div>""", unsafe_allow_html=True)

        for session, timing in GATE_DAILY_HOURS.items():
            hrs = 2.0 if "Concept" in session else 3.0 if "Practice" in session else 2.0 if "Morning" in session else 2.0 if "Revision" in session else 1.5
            col_map = {"Morning Study":"#7c3aed","Concept Learning":"#0891b2","Practice Problems":"#059669","Revision":"#d97706","Mock Test/PYQ":"#dc2626"}
            c = col_map.get(session, "#4f46e5")
            sc1, sc2, sc3 = st.columns([2,3,1])
            sc1.markdown(f"""<div style="background:{c};border-radius:10px;padding:10px 14px;">
            <b style="color:#fff;font-size:0.9rem;">{session}</b>
            </div>""", unsafe_allow_html=True)
            sc2.markdown(f"""<div style="background:#fff;border:1.5px solid {c}44;border-radius:10px;padding:10px 14px;">
            <span style="color:#1e1e2e;font-size:0.85rem;">⏰ {timing}</span>
            </div>""", unsafe_allow_html=True)
            sc3.markdown(f"""<div style="background:{c}18;border:1.5px solid {c}44;border-radius:10px;padding:10px;text-align:center;">
            <b style="color:{c};">{hrs}h</b>
            </div>""", unsafe_allow_html=True)
            st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)

        st.divider()
        st.markdown("### 📋 Important GATE Tips")
        tips = [
            ("📚","Cover PYQ (Previous Year Questions) for last 10 years — most important!"),
            ("🧮","Engineering Mathematics carries ~15% weightage in all branches"),
            ("⏱️","Attempt mock tests every Saturday — time management is key"),
            ("🎯","Focus on high-weightage topics first: DS, Algorithms, OS, DBMS, Networks for CSE"),
            ("🔁","Revise every Sunday — spaced repetition improves retention by 80%"),
            ("📖","NPTEL videos + standard textbooks > random YouTube for GATE"),
            ("💪","Aim for 200+ marks in practice; actual GATE scoring requires accuracy"),
        ]
        for icon, tip in tips:
            st.markdown(f"""<div style="background:#fffbeb;border-left:4px solid #d97706;
            border-radius:8px;padding:10px 14px;margin-bottom:6px;">
            <span style="font-size:1.1rem;">{icon}</span>
            <span style="color:#1e1e2e;font-size:0.87rem;margin-left:8px;">{tip}</span>
            </div>""", unsafe_allow_html=True)

# ── SHARED NAV BACK HELPER (must be defined before all show_ functions that use it)
def _nav_back(title, mode):
    c1, c2 = st.columns([1, 5])
    if c1.button("🏠 Home", key=f"back_{mode}"):
        st.session_state.app_mode = None
        st.rerun()


# ─────────────────────────────────────────────
# ══ GROUP 2: CAREER & PERFORMANCE FEATURES ══
# ─────────────────────────────────────────────

# ── 1. MOCK INTERVIEW PREP
def show_interview():
    _nav_back("🎯 Mock Interview Prep", "interview")

    st.markdown("""
    <div style="background:linear-gradient(90deg,#7c3aed,#4f46e5,#0ea5e9);
    border-radius:16px;padding:18px 28px;margin-bottom:22px;color:#fff;">
    <h2 style="margin:0;color:#fff!important;">🎯 Mock Interview Prep</h2>
    <p style="margin:4px 0 0;opacity:0.9;font-size:0.87rem;">AI-powered technical & HR interview simulation — branch specific</p>
    </div>""", unsafe_allow_html=True)

    branch_list = ["Computer Engineering","Information Technology","Electronics & Communication",
                   "Electrical Engineering","Mechanical Engineering","Civil Engineering",
                   "Artificial Intelligence & ML","Data Science"]

    c1, c2, c3 = st.columns([2, 1, 1])
    branch = c1.selectbox("🏫 Select Branch", branch_list,
                          index=branch_list.index(st.session_state.interview_branch)
                          if st.session_state.interview_branch in branch_list else 0,
                          key="iv_branch")
    round_type = c2.selectbox("🎙️ Round Type", ["Technical","HR","Mixed"], key="iv_round")
    difficulty = c3.selectbox("⚡ Difficulty", ["Easy","Medium","Hard"], key="iv_diff")
    st.session_state.interview_branch = branch

    if not st.session_state.interview_active:
        if st.button("🚀 Start Interview Session", use_container_width=True, key="iv_start"):
            st.session_state.interview_history = []
            st.session_state.interview_score   = None
            st.session_state.interview_active  = True
            # Generate first question
            prompt = (f"You are an interviewer for a {branch} engineering student. "
                      f"Conduct a {round_type} interview at {difficulty} level. "
                      f"Ask one interview question. Just the question, nothing else.")
            try:
                messages = [{"role": "system", "content": "You are a professional technical interviewer."}, {"role": "user", "content": prompt}]
                res_raw = safe_chat(messages, temperature=0.6, max_tokens=200)
                if res_raw is None: raise Exception("AI service unavailable. Check API key.")
                class _R: pass
                res = _R()
                class _C: pass
                res.choices = [_C()]
                res.choices[0].message = _C()
                res.choices[0].message.content = res_raw
                q = res.choices[0].message.content.strip()
                st.session_state.interview_history = [{"role":"interviewer","text":q}]
            except Exception as e:
                st.error(f"Error: {e}")
            st.rerun()
        # Show past scores
        if st.session_state.interview_score is not None:
            sc = st.session_state.interview_score
            colour = "#16a34a" if sc >= 7 else "#d97706" if sc >= 5 else "#dc2626"
            st.markdown(f"""
            <div style="background:#f0fdf4;border:2px solid #86efac;border-radius:16px;
            padding:20px;text-align:center;margin-top:16px;">
            <div style="font-size:2.5rem;font-weight:900;color:{colour};">{sc}/10</div>
            <div style="color:#4b5563;margin-top:4px;">Interview Score</div>
            </div>""", unsafe_allow_html=True)
        return

    # ── Active session
    st.markdown("---")
    for turn in st.session_state.interview_history:
        if turn["role"] == "interviewer":
            st.markdown(f"""<div style="background:#f5f3ff;border-left:4px solid #7c3aed;
            border-radius:12px;padding:12px 16px;margin:6px 0;">
            🎙️ <b style="color:#4c1d95;">Interviewer:</b>
            <span style="color:#1e1e2e;"> {turn['text']}</span></div>""", unsafe_allow_html=True)
        else:
            st.markdown(f"""<div style="background:#f0fdf4;border-left:4px solid #16a34a;
            border-radius:12px;padding:12px 16px;margin:6px 0;">
            🧑‍💼 <b style="color:#065f46;">You:</b>
            <span style="color:#1e1e2e;"> {turn['text']}</span></div>""", unsafe_allow_html=True)

    answer = st.text_area("✍️ Your Answer:", height=120, key="iv_answer_box",
                           placeholder="Type your answer here...")
    bc1, bc2, bc3 = st.columns(3)

    if bc1.button("📨 Submit Answer", key="iv_submit", use_container_width=True):
        if answer.strip():
            history = st.session_state.interview_history
            history.append({"role":"candidate","text":answer.strip()})
            # Ask AI for follow-up or evaluation
            msgs = [{"role":"system","content":
                     f"You are an interviewer for {branch} engineering. "
                     f"Round: {round_type}. Difficulty: {difficulty}. "
                     f"After each answer, briefly evaluate (1-2 sentences) then ask the next question. "
                     f"After 5 questions total, say 'Interview Complete' and give a score out of 10."}]
            for turn in history:
                role = "assistant" if turn["role"]=="interviewer" else "user"
                msgs.append({"role":role,"content":turn["text"]})
            try:
                res_raw = safe_chat(msgs, temperature=0.5, max_tokens=400)
                if res_raw is None: raise Exception("AI service unavailable. Check API key.")
                class _R: pass
                res = _R()
                class _C: pass
                res.choices = [_C()]
                res.choices[0].message = _C()
                res.choices[0].message.content = res_raw
                reply = res.choices[0].message.content.strip()
                history.append({"role":"interviewer","text":reply})
                st.session_state.interview_history = history
                # Check if done
                if "Interview Complete" in reply or "interview complete" in reply.lower():
                    import re as _re
                    m = _re.search(r'(\d+)/10', reply)
                    st.session_state.interview_score = int(m.group(1)) if m else 7
                    st.session_state.interview_active = False
            except Exception as e:
                st.error(f"Error: {e}")
            st.rerun()
        else:
            st.warning("Please type an answer first.")

    if bc2.button("⏭️ Skip Question", key="iv_skip", use_container_width=True):
        st.session_state.interview_history.append({"role":"candidate","text":"[Skipped]"})
        st.session_state.interview_history.append({"role":"interviewer","text":"No problem. Let's move on. Next question: What are your strongest technical skills?"})
        st.rerun()

    if bc3.button("🛑 End Interview", key="iv_end", use_container_width=True):
        st.session_state.interview_active = False
        st.session_state.interview_score  = 6
        st.rerun()


# ── 2. NOTES ORGANISER
def show_notes():
    _nav_back("📝 Notes Organiser", "notes")

    st.markdown("""
    <div style="background:linear-gradient(90deg,#0891b2,#0e7490,#155e75);
    border-radius:16px;padding:18px 28px;margin-bottom:22px;color:#fff;">
    <h2 style="margin:0;color:#fff!important;">📝 Notes Organiser</h2>
    <p style="margin:4px 0 0;opacity:0.9;font-size:0.87rem;">Create, tag & AI-summarise your subject notes</p>
    </div>""", unsafe_allow_html=True)

    import time as _time

    view = st.session_state.note_view

    # ── LIST VIEW
    if view == "list":
        c1, c2 = st.columns([3, 1])
        search = c1.text_input("🔍 Search notes...", key="notes_search", placeholder="Search by title or subject...")
        if c2.button("➕ New Note", key="notes_new", use_container_width=True):
            st.session_state.note_view = "edit"
            st.session_state.note_editing_id = None
            st.rerun()

        notes = st.session_state.notes
        if search:
            notes = [n for n in notes if search.lower() in n["title"].lower()
                     or search.lower() in n.get("subject","").lower()
                     or search.lower() in n.get("content","").lower()]

        if not notes:
            st.markdown("""<div style="text-align:center;padding:40px;color:#9ca3af;">
            📭 No notes yet. Click <b>➕ New Note</b> to create your first note!
            </div>""", unsafe_allow_html=True)
        else:
            cols = st.columns(3)
            for i, note in enumerate(notes):
                with cols[i % 3]:
                    tags_html = " ".join([f'<span style="background:#ede9fe;color:#7c3aed;border-radius:10px;padding:2px 8px;font-size:0.7rem;">{t}</span>' for t in note.get("tags",[])])
                    st.markdown(f"""
                    <div style="background:#fff;border:1.5px solid #ede9fe;border-radius:16px;
                    padding:16px;margin-bottom:12px;box-shadow:0 2px 8px rgba(124,58,237,0.07);">
                    <div style="font-weight:700;color:#3b0764;font-size:0.95rem;">{note['title']}</div>
                    <div style="font-size:0.75rem;color:#7c3aed;margin:4px 0;">{note.get('subject','')}</div>
                    <div style="font-size:0.8rem;color:#6b7280;margin:6px 0;line-height:1.5;
                    overflow:hidden;max-height:3.5em;">{note.get('content','')[:120]}{'...' if len(note.get('content',''))>120 else ''}</div>
                    <div style="margin-top:8px;">{tags_html}</div>
                    <div style="font-size:0.7rem;color:#9ca3af;margin-top:6px;">{note.get('created','')}</div>
                    </div>""", unsafe_allow_html=True)
                    bc1, bc2 = st.columns(2)
                    if bc1.button("✏️ Edit", key=f"note_edit_{note['id']}"):
                        st.session_state.note_view = "edit"
                        st.session_state.note_editing_id = note["id"]
                        st.rerun()
                    if bc2.button("🗑️ Delete", key=f"note_del_{note['id']}"):
                        st.session_state.notes = [n for n in st.session_state.notes if n["id"] != note["id"]]
                        st.rerun()

    # ── EDIT VIEW
    elif view == "edit":
        eid = st.session_state.note_editing_id
        existing = next((n for n in st.session_state.notes if n["id"] == eid), None) if eid else None

        st.markdown(f"### {'✏️ Edit Note' if existing else '➕ New Note'}")
        title   = st.text_input("📌 Title", value=existing["title"] if existing else "", key="note_title")
        subject = st.text_input("📚 Subject", value=existing.get("subject","") if existing else "", key="note_subj")
        tags_raw= st.text_input("🏷️ Tags (comma-separated)", value=", ".join(existing.get("tags",[])) if existing else "", key="note_tags")
        content = st.text_area("📄 Content", value=existing.get("content","") if existing else "",
                               height=250, key="note_content")

        bc1, bc2, bc3 = st.columns(3)
        if bc1.button("💾 Save Note", key="note_save", use_container_width=True):
            if title.strip():
                tags = [t.strip() for t in tags_raw.split(",") if t.strip()]
                if existing:
                    for n in st.session_state.notes:
                        if n["id"] == eid:
                            n["title"]   = title.strip()
                            n["subject"] = subject.strip()
                            n["tags"]    = tags
                            n["content"] = content.strip()
                else:
                    st.session_state.notes.append({
                        "id":      str(int(_time.time()*1000)),
                        "title":   title.strip(),
                        "subject": subject.strip(),
                        "tags":    tags,
                        "content": content.strip(),
                        "created": datetime.now().strftime("%d %b %Y, %H:%M")
                    })
                st.session_state.note_view = "list"
                st.session_state.note_editing_id = None
                st.success("✅ Note saved!")
                st.rerun()
            else:
                st.warning("Please enter a title.")

        if bc2.button("🤖 AI Summarise", key="note_summarise", use_container_width=True):
            if content.strip():
                with st.spinner("Summarising..."):
                    try:
                        messages = [{"role": "system", "content": "You are an expert academic summariser."}, {"role": "user", "content": f"Summarise these notes in 3-4 bullet points:\n\n{content.strip()}"}]
                        res_raw = safe_chat(messages, temperature=0.3, max_tokens=300)
                        if res_raw is None: raise Exception("AI service unavailable. Check API key.")
                        class _R: pass
                        res = _R()
                        class _C: pass
                        res.choices = [_C()]
                        res.choices[0].message = _C()
                        res.choices[0].message.content = res_raw
                        summary = res.choices[0].message.content.strip()
                        st.info(f"**AI Summary:**\n\n{summary}")
                    except Exception as e:
                        st.error(f"Error: {e}")
            else:
                st.warning("Add some content first.")

        if bc3.button("❌ Cancel", key="note_cancel", use_container_width=True):
            st.session_state.note_view = "list"
            st.session_state.note_editing_id = None
            st.rerun()


# ── 3. CGPA / GPA CALCULATOR
def show_cgpa():
    _nav_back("📈 CGPA / GPA Calculator", "cgpa")

    st.markdown("""
    <div style="background:linear-gradient(90deg,#059669,#047857,#065f46);
    border-radius:16px;padding:18px 28px;margin-bottom:22px;color:#fff;">
    <h2 style="margin:0;color:#fff!important;">📈 CGPA / GPA Calculator</h2>
    <p style="margin:4px 0 0;opacity:0.9;font-size:0.87rem;">Semester-wise grade entry · CGPA tracker · Grade predictor</p>
    </div>""", unsafe_allow_html=True)

    GRADE_POINTS = {"O":10,"A+":9,"A":8,"B+":7,"B":6,"C":5,"P":4,"F":0}

    num_sem = st.slider("📅 Number of Semesters Completed", 1, 8, 4, key="cgpa_nsem")

    # Build semester data
    if len(st.session_state.cgpa_semesters) != num_sem:
        st.session_state.cgpa_semesters = [
            {"subjects": [{"name":f"Subject {j+1}","credits":4,"grade":"A"} for j in range(5)]}
            for _ in range(num_sem)
        ]

    tabs = st.tabs([f"📅 Sem {i+1}" for i in range(num_sem)])
    all_credits, all_points = 0, 0

    for si, tab in enumerate(tabs):
        with tab:
            sem = st.session_state.cgpa_semesters[si]
            num_subj = st.number_input(f"Number of subjects (Sem {si+1})", 1, 10,
                                        len(sem["subjects"]), key=f"cgpa_ns_{si}")
            while len(sem["subjects"]) < num_subj:
                sem["subjects"].append({"name":f"Subject {len(sem['subjects'])+1}","credits":4,"grade":"A"})
            while len(sem["subjects"]) > num_subj:
                sem["subjects"].pop()

            sem_credits, sem_points = 0, 0
            for ji, subj in enumerate(sem["subjects"]):
                sc1, sc2, sc3 = st.columns([3,1,2])
                subj["name"]    = sc1.text_input("Subject", value=subj["name"], key=f"cgpa_sn_{si}_{ji}")
                subj["credits"] = sc2.number_input("Credits", 1, 6, subj["credits"], key=f"cgpa_cr_{si}_{ji}")
                subj["grade"]   = sc3.selectbox("Grade", list(GRADE_POINTS.keys()),
                                                 index=list(GRADE_POINTS.keys()).index(subj["grade"])
                                                 if subj["grade"] in GRADE_POINTS else 2,
                                                 key=f"cgpa_gr_{si}_{ji}")
                gp = GRADE_POINTS[subj["grade"]]
                sem_credits += subj["credits"]
                sem_points  += gp * subj["credits"]

            sgpa = round(sem_points / sem_credits, 2) if sem_credits else 0
            all_credits += sem_credits
            all_points  += sem_points

            color = "#16a34a" if sgpa >= 8 else "#d97706" if sgpa >= 6 else "#dc2626"
            st.markdown(f"""
            <div style="background:#f0fdf4;border:2px solid #86efac;border-radius:12px;
            padding:12px 20px;margin-top:12px;text-align:center;">
            <b style="color:{color};font-size:1.4rem;">SGPA: {sgpa}</b>
            <span style="color:#6b7280;font-size:0.85rem;margin-left:12px;">
            Total Credits: {sem_credits}</span></div>""", unsafe_allow_html=True)

    cgpa = round(all_points / all_credits, 2) if all_credits else 0
    color = "#16a34a" if cgpa >= 8 else "#d97706" if cgpa >= 6 else "#dc2626"
    st.markdown(f"""
    <div style="background:linear-gradient(135deg,#f0fdf4,#dcfce7);
    border:3px solid #16a34a;border-radius:20px;padding:24px;text-align:center;margin:20px 0;">
    <div style="font-size:3rem;font-weight:900;color:{color};">{cgpa}</div>
    <div style="color:#16a34a;font-size:1.1rem;font-weight:600;">Overall CGPA</div>
    <div style="color:#6b7280;font-size:0.85rem;margin-top:6px;">
    Total Credits: {all_credits} &nbsp;·&nbsp;
    {'Outstanding 🏆' if cgpa>=9 else 'Excellent 🌟' if cgpa>=8 else 'Good 👍' if cgpa>=6 else 'Needs Improvement 📚'}</div>
    </div>""", unsafe_allow_html=True)

    # Grade predictor
    st.markdown("### 🎯 Grade Predictor")
    st.caption("What CGPA will you get if you score a target grade in all remaining semesters?")
    pc1, pc2 = st.columns(2)
    remaining = pc1.number_input("Remaining semesters", 1, 8, 2, key="cgpa_rem")
    target_g  = pc2.selectbox("Target grade each semester", ["O","A+","A","B+","B"], key="cgpa_tgt")
    avg_credits_per_sem = (all_credits // num_sem) if num_sem else 20
    future_credits = remaining * avg_credits_per_sem
    future_points  = remaining * avg_credits_per_sem * GRADE_POINTS[target_g]
    predicted = round((all_points + future_points) / (all_credits + future_credits), 2) if (all_credits + future_credits) else 0
    pcolor = "#16a34a" if predicted >= 8 else "#d97706" if predicted >= 6 else "#dc2626"
    st.markdown(f"""
    <div style="background:#fffbeb;border:2px solid #fcd34d;border-radius:12px;
    padding:16px;text-align:center;">
    <b style="color:{pcolor};font-size:1.5rem;">Predicted CGPA: {predicted}</b>
    <div style="color:#6b7280;font-size:0.83rem;margin-top:4px;">
    If you score <b>{target_g}</b> in all {remaining} remaining semester(s)</div>
    </div>""", unsafe_allow_html=True)


# ── 4. LEADERBOARD
def show_leaderboard():
    _nav_back("🏆 Leaderboard", "leaderboard")

    st.markdown("""
    <div style="background:linear-gradient(90deg,#dc2626,#b91c1c,#7f1d1d);
    border-radius:16px;padding:18px 28px;margin-bottom:22px;color:#fff;">
    <h2 style="margin:0;color:#fff!important;">🏆 Leaderboard & Peer Ranking</h2>
    <p style="margin:4px 0 0;opacity:0.9;font-size:0.87rem;">Quiz scores · Study streaks · Class rankings</p>
    </div>""", unsafe_allow_html=True)

    import time as _t

    # Add score form
    # ── Custom toggle (replaces st.expander to avoid arrow_down text bug)
    if "lb_form_open" not in st.session_state:
        st.session_state.lb_form_open = len(st.session_state.lb_scores) == 0
    _tog_lbl = "🔼 Hide Score Form" if st.session_state.lb_form_open else "➕ Submit Your Score"
    st.markdown(f"""<div style="background:linear-gradient(135deg,#7c3aed,#4f46e5);
        border-radius:12px;padding:1px;margin-bottom:8px;">
        </div>""", unsafe_allow_html=True)
    if st.button(_tog_lbl, key="lb_toggle", use_container_width=True):
        st.session_state.lb_form_open = not st.session_state.lb_form_open
        st.rerun()
    if st.session_state.lb_form_open:
        st.markdown("""<div style="background:#f8f5ff;border:2px solid #c4b5fd;
            border-radius:0 0 14px 14px;padding:16px 18px 10px 18px;margin-top:-4px;">
            </div>""", unsafe_allow_html=True)
        lc1, lc2, lc3, lc4 = st.columns([2, 2, 1, 1])
        lb_name    = lc1.text_input("👤 Your Name", value=st.session_state.lb_my_name, key="lb_name_in")
        lb_subject = lc2.text_input("📚 Subject", key="lb_subj_in", placeholder="e.g. DBMS")
        lb_score   = lc3.number_input("🔢 Score (/10)", min_value=0, max_value=10, value=8, step=1, key="lb_score_in")
        if lc4.button("🚀 Submit", key="lb_submit", use_container_width=True):
            if lb_name.strip() and lb_subject.strip():
                st.session_state.lb_my_name = lb_name.strip()
                st.session_state.lb_scores.append({
                    "id": str(int(_t.time()*1000)),
                    "name": lb_name.strip(),
                    "subject": lb_subject.strip(),
                    "score": lb_score,
                    "date": datetime.now().strftime("%d %b %Y")
                })
                st.session_state.lb_form_open = False
                st.success("✅ Score submitted!")
                st.rerun()
            else:
                st.warning("Please enter name and subject.")

    scores = st.session_state.lb_scores
    if not scores:
        st.markdown("""<div style="text-align:center;padding:40px;color:#9ca3af;">
        🏆 No scores yet. Be the first to submit!</div>""", unsafe_allow_html=True)
        return

    # Sort by score desc
    sorted_scores = sorted(scores, key=lambda x: x["score"], reverse=True)

    medals = ["🥇","🥈","🥉"]
    my_name = st.session_state.lb_my_name

    st.markdown("### 🏆 All-Time Leaderboard")
    for rank, entry in enumerate(sorted_scores):
        medal = medals[rank] if rank < 3 else f"#{rank+1}"
        is_me = entry["name"].lower() == my_name.lower()
        bg = "linear-gradient(90deg,#f5f3ff,#ede9fe)" if is_me else "#ffffff"
        border = "#7c3aed" if is_me else "#ede9fe"
        bar_pct = int(entry["score"] * 10)
        bar_color = "#16a34a" if entry["score"]>=8 else "#d97706" if entry["score"]>=6 else "#dc2626"
        st.markdown(f"""
        <div style="background:{bg};border:2px solid {border};border-radius:14px;
        padding:14px 18px;margin-bottom:8px;display:flex;align-items:center;gap:16px;">
        <span style="font-size:1.5rem;min-width:36px;">{medal}</span>
        <div style="flex:1;">
            <div style="font-weight:700;color:#1e1e2e;">{entry['name']}
            {'  <span style="background:#7c3aed;color:#fff;border-radius:8px;padding:1px 8px;font-size:0.7rem;">YOU</span>' if is_me else ''}</div>
            <div style="font-size:0.78rem;color:#7c3aed;">{entry['subject']} · {entry['date']}</div>
            <div style="background:#ede9fe;border-radius:6px;height:6px;margin-top:6px;">
            <div style="width:{bar_pct}%;background:{bar_color};height:6px;border-radius:6px;"></div></div>
        </div>
        <div style="font-size:1.8rem;font-weight:900;color:{bar_color};">{entry['score']}<span style="font-size:0.8rem;color:#9ca3af;">/10</span></div>
        </div>""", unsafe_allow_html=True)

    if st.button("🗑️ Clear Leaderboard", key="lb_clear"):
        st.session_state.lb_scores = []
        st.rerun()


# ─────────────────────────────────────────────
# ══ GROUP 3: EXAM-SPECIFIC FEATURES ══
# ─────────────────────────────────────────────

# ── 5. EXAM COUNTDOWN
def show_countdown():
    _nav_back("📅 Exam Countdown", "countdown")

    st.markdown("""
    <div style="background:linear-gradient(90deg,#7c3aed,#4f46e5);
    border-radius:16px;padding:18px 28px;margin-bottom:22px;color:#fff;">
    <h2 style="margin:0;color:#fff!important;">📅 Exam Countdown Tracker</h2>
    <p style="margin:4px 0 0;opacity:0.9;font-size:0.87rem;">Track all upcoming exams · Countdown timers · Daily prep tips</p>
    </div>""", unsafe_allow_html=True)

    # Add exam
    # ── Custom toggle (replaces st.expander to avoid arrow_down text bug)
    if "exam_form_open" not in st.session_state:
        st.session_state.exam_form_open = len(st.session_state.exams) == 0
    _exam_lbl = "🔼 Hide Form" if st.session_state.exam_form_open else "➕ Add Exam"
    if st.button(_exam_lbl, key="exam_toggle", use_container_width=True):
        st.session_state.exam_form_open = not st.session_state.exam_form_open
        st.rerun()
    if st.session_state.exam_form_open:
        st.markdown("""<div style="background:#f8f5ff;border:2px solid #c4b5fd;
            border-radius:14px;padding:16px 18px 10px 18px;margin-bottom:10px;">
            </div>""", unsafe_allow_html=True)
        ec1, ec2, ec3 = st.columns([2, 2, 1])
        exam_name = ec1.text_input("📝 Exam Name", key="exam_name", placeholder="e.g. DBMS Internal 2")
        exam_date = ec2.date_input("📅 Exam Date", key="exam_date_in", min_value=dt_date.today())
        if ec3.button("➕ Add", key="exam_add", use_container_width=True):
            if exam_name.strip():
                st.session_state.exams.append({
                    "id": exam_name.strip() + str(exam_date),
                    "name": exam_name.strip(),
                    "date": str(exam_date)
                })
                st.session_state.exam_form_open = False
                st.success(f"✅ {exam_name} added!")
                st.rerun()

    if not st.session_state.exams:
        st.markdown("""<div style="text-align:center;padding:40px;color:#9ca3af;">
        📅 No exams added yet. Add your upcoming exams above!</div>""", unsafe_allow_html=True)
        return

    today = dt_date.today()
    exams_sorted = sorted(st.session_state.exams,
                          key=lambda x: dt_date.fromisoformat(x["date"]))

    cols = st.columns(min(3, len(exams_sorted)))
    for i, exam in enumerate(exams_sorted):
        exam_dt = dt_date.fromisoformat(exam["date"])
        days_left = (exam_dt - today).days
        if days_left < 0:
            label, bg, border = "✅ Passed", "#f0fdf4", "#86efac"
            days_str = f"{abs(days_left)} days ago"
        elif days_left == 0:
            label, bg, border = "🚨 TODAY!", "#fef2f2", "#fca5a5"
            days_str = "TODAY"
        elif days_left <= 3:
            label, bg, border = "⚠️ Very Soon", "#fef2f2", "#fca5a5"
            days_str = f"{days_left} day{'s' if days_left>1 else ''} left"
        elif days_left <= 7:
            label, bg, border = "⏳ This Week", "#fffbeb", "#fcd34d"
            days_str = f"{days_left} days left"
        else:
            label, bg, border = "📅 Upcoming", "#f5f3ff", "#c4b5fd"
            days_str = f"{days_left} days left"

        col_idx = i % min(3, len(exams_sorted))
        with cols[col_idx]:
            # Choose big display symbol
            if days_left < 0:
                big_display = "✓"
                big_color   = "#16a34a"
            elif days_left == 0:
                big_display = "🎓"
                big_color   = "#dc2626"
            elif days_left <= 3:
                big_display = str(days_left)
                big_color   = "#dc2626"
            elif days_left <= 7:
                big_display = str(days_left)
                big_color   = "#d97706"
            else:
                big_display = str(days_left)
                big_color   = "#7c3aed"
            st.markdown(f"""
            <div style="background:{bg};border:2px solid {border};border-radius:18px;
            padding:20px;text-align:center;margin-bottom:14px;">
            <div style="font-size:0.75rem;font-weight:600;color:#6b7280;margin-bottom:6px;">{label}</div>
            <div style="font-size:1.1rem;font-weight:700;color:#1e1e2e;">{exam['name']}</div>
            <div style="font-size:2.8rem;font-weight:900;color:{big_color};margin:8px 0;">{big_display}</div>
            <div style="font-size:0.85rem;color:#7c3aed;font-weight:600;">{days_str}</div>
            <div style="font-size:0.78rem;color:#9ca3af;margin-top:4px;">{exam_dt.strftime('%d %b %Y')}</div>
            </div>""", unsafe_allow_html=True)
            if st.button("🗑️ Remove", key=f"exam_del_{exam['id']}", use_container_width=True):
                st.session_state.exams = [e for e in st.session_state.exams if e["id"] != exam["id"]]
                st.rerun()

    # Upcoming: AI prep tip for nearest exam
    upcoming = [e for e in exams_sorted if (dt_date.fromisoformat(e["date"]) - today).days >= 0]
    if upcoming:
        nearest = upcoming[0]
        days_left = (dt_date.fromisoformat(nearest["date"]) - today).days
        st.markdown("---")
        st.markdown(f"### 🤖 AI Prep Tips for: {nearest['name']}")
        if st.button("💡 Generate Study Tips", key="exam_tips"):
            with st.spinner("Generating tips..."):
                try:
                    messages = [{"role": "system", "content": "You are an expert exam preparation coach."}, {"role": "user", "content": f"Give 5 specific daily study tips for a student with {days_left} days left before their '{nearest['name']}' exam. Be concise and actionable."}]
                    res_raw = safe_chat(messages, temperature=0.4, max_tokens=400)
                    if res_raw is None: raise Exception("AI service unavailable. Check API key.")
                    class _R: pass
                    res = _R()
                    class _C: pass
                    res.choices = [_C()]
                    res.choices[0].message = _C()
                    res.choices[0].message.content = res_raw
                    st.markdown(res.choices[0].message.content.strip())
                except Exception as e:
                    st.error(f"Error: {e}")


# ── 6. PREVIOUS YEAR PAPERS (PYQ Bank)
def show_pyq():
    _nav_back("🗂️ PYQ Bank", "pyq")

    st.markdown("""
    <div style="background:linear-gradient(90deg,#0891b2,#0e7490);
    border-radius:16px;padding:18px 28px;margin-bottom:22px;color:#fff;">
    <h2 style="margin:0;color:#fff!important;">🗂️ Previous Year Question Bank</h2>
    <p style="margin:4px 0 0;opacity:0.9;font-size:0.87rem;">Branch-wise PYQs · AI-generated solutions · Exam patterns</p>
    </div>""", unsafe_allow_html=True)

    BRANCH_SUBJS = {
        "Computer Engineering": ["Data Structures","DBMS","Operating Systems","Computer Networks","Algorithms","Compiler Design","Software Engineering","Theory of Computation","Computer Architecture","Discrete Mathematics"],
        "Information Technology": ["Web Technologies","Data Structures","DBMS","Computer Networks","Software Engineering","Cloud Computing","Cybersecurity","Mobile Applications","Data Mining","AI & ML"],
        "Electronics & Communication": ["Signals & Systems","Digital Electronics","Analog Circuits","Communication Systems","VLSI Design","Microprocessors","Control Systems","Electromagnetic Theory","DSP","Antenna Theory"],
        "Mechanical Engineering": ["Engineering Mechanics","Thermodynamics","Fluid Mechanics","Machine Design","Manufacturing Processes","Heat Transfer","Theory of Machines","Material Science","CAD/CAM","Industrial Engineering"],
        "Civil Engineering": ["Structural Analysis","Fluid Mechanics","Geotechnical Engineering","Transportation Engineering","Environmental Engineering","RCC Design","Surveying","Construction Management","Hydraulics","Soil Mechanics"],
    }

    c1, c2, c3 = st.columns([2, 2, 1])
    branches = list(BRANCH_SUBJS.keys())
    branch = c1.selectbox("🏫 Branch", branches,
                          index=branches.index(st.session_state.pyq_branch)
                          if st.session_state.pyq_branch in branches else 0,
                          key="pyq_br")
    st.session_state.pyq_branch = branch
    subjects = BRANCH_SUBJS.get(branch, [])
    subject = c2.selectbox("📚 Subject", subjects, key="pyq_subj")
    year = c3.selectbox("📅 Year", ["2025","2024","2023","2022","2021","2020"], key="pyq_yr")

    st.session_state.pyq_subject = subject
    st.session_state.pyq_year    = year

    num_q = st.slider("🔢 Number of Questions", 5, 20, 10, key="pyq_nq")

    if st.button("🤖 Generate PYQ-Style Questions", key="pyq_gen", use_container_width=True):
        with st.spinner(f"Generating {num_q} PYQ-style questions for {subject} ({year})..."):
            try:
                prompt = (f"Generate {num_q} previous year exam-style questions for the subject '{subject}' "
                          f"for {branch} engineering students (exam year: {year}). "
                          f"Mix short answer (2 marks), medium (5 marks), and long answer (10 marks) questions. "
                          f"Format: Q1. [marks] question text. Number them 1 to {num_q}.")
                messages = [{"role": "system", "content": "You are a university exam paper setter."}, {"role": "user", "content": prompt}]
                res_raw = safe_chat(messages, temperature=0.5, max_tokens=1200)
                if res_raw is None: raise Exception("AI service unavailable. Check API key.")
                class _R: pass
                res = _R()
                class _C: pass
                res.choices = [_C()]
                res.choices[0].message = _C()
                res.choices[0].message.content = res_raw
                raw = res.choices[0].message.content.strip()
                questions = [line.strip() for line in raw.split('\n') if line.strip() and line.strip()[0].isdigit()]
                st.session_state.pyq_questions = questions if questions else [raw]
                st.rerun()
            except Exception as e:
                st.error(f"Error: {e}")

    if st.session_state.pyq_questions:
        st.markdown(f"### 📋 {subject} — PYQ-Style Questions ({year})")
        for qi, q in enumerate(st.session_state.pyq_questions):
            marks_color = "#dc2626" if "10" in q[:8] else "#d97706" if "5" in q[:8] else "#059669"
            st.markdown(f"""
            <div style="background:#fff;border:1.5px solid #ede9fe;border-radius:12px;
            padding:14px 18px;margin-bottom:8px;">
            <span style="color:#7c3aed;font-weight:600;">Q{qi+1}.</span>
            <span style="color:#1e1e2e;"> {q[q.find('.')+1:].strip() if '.' in q else q}</span>
            </div>""", unsafe_allow_html=True)

            # ── Custom toggle for AI Solution (replaces st.expander)
            sol_key     = f"pyq_sol_{qi}"
            sol_tog_key = f"pyq_sol_open_{qi}"
            if sol_key not in st.session_state:
                st.session_state[sol_key] = ""
            if sol_tog_key not in st.session_state:
                st.session_state[sol_tog_key] = False
            _sol_lbl = "🔼 Hide Solution" if st.session_state[sol_tog_key] else f"💡 View AI Solution — Q{qi+1}"
            if st.button(_sol_lbl, key=f"pyq_sol_togbtn_{qi}"):
                st.session_state[sol_tog_key] = not st.session_state[sol_tog_key]
                st.rerun()
            if st.session_state[sol_tog_key]:
                st.markdown("""<div style="background:#f0fdf4;border:1px solid #86efac;
                    border-radius:12px;padding:14px 16px;margin-top:4px;">""", unsafe_allow_html=True)
                if not st.session_state[sol_key]:
                    if st.button(f"🤖 Generate Solution", key=f"pyq_sol_btn_{qi}"):
                        with st.spinner("Generating solution..."):
                            try:
                                sol_messages = [{"role": "system", "content": "You are an expert engineering professor."}, {"role": "user", "content": f"Provide a detailed solution for this exam question:\n\n{q_text}"}]
                                res2_raw = safe_chat(sol_messages, temperature=0.3, max_tokens=500)
                                if res2_raw is None: raise Exception("AI service unavailable. Check API key.")
                                class _R: pass
                                res2 = _R()
                                class _C: pass
                                res2.choices = [_C()]
                                res2.choices[0].message = _C()
                                res2.choices[0].message.content = res2_raw
                                st.session_state[sol_key] = res2.choices[0].message.content.strip()
                                st.rerun()
                            except Exception as e:
                                st.error(f"Error: {e}")
                else:
                    st.markdown(st.session_state[sol_key])
                st.markdown("</div>", unsafe_allow_html=True)


# ── 7. SYLLABUS TRACKER
def show_syllabus():
    _nav_back("💊 Syllabus Tracker", "syllabus")

    st.markdown("""
    <div style="background:linear-gradient(90deg,#059669,#047857);
    border-radius:16px;padding:18px 28px;margin-bottom:22px;color:#fff;">
    <h2 style="margin:0;color:#fff!important;">💊 Syllabus Tracker</h2>
    <p style="margin:4px 0 0;opacity:0.9;font-size:0.87rem;">Tick off topics · Track % coverage per subject</p>
    </div>""", unsafe_allow_html=True)

    SYLLABUS = {
        "Data Structures": ["Arrays & Strings","Linked Lists","Stacks & Queues","Trees (BST, AVL)","Heaps","Graphs (BFS, DFS)","Hashing","Sorting Algorithms","Searching Algorithms","Dynamic Programming"],
        "DBMS": ["ER Model","Relational Model","SQL Basics","Advanced SQL","Normalization (1NF-BCNF)","Transaction Management","Concurrency Control","Indexing & Hashing","Query Optimization","NoSQL Basics"],
        "Operating Systems": ["Process Management","CPU Scheduling","Synchronization","Deadlock","Memory Management","Virtual Memory","File Systems","I/O Management","Security","Distributed Systems"],
        "Computer Networks": ["OSI Model","TCP/IP","Data Link Layer","Network Layer","Transport Layer","Application Layer","Routing Algorithms","Congestion Control","Network Security","Wireless Networks"],
        "Algorithms": ["Asymptotic Analysis","Divide & Conquer","Greedy Algorithms","Dynamic Programming","Graph Algorithms","Backtracking","Branch & Bound","NP-Completeness","String Matching","Computational Geometry"],
        "Digital Electronics": ["Number Systems","Boolean Algebra","Logic Gates","Combinational Circuits","Sequential Circuits","Flip-Flops","Counters & Registers","ADC/DAC","Memory Devices","PLDs & FPGAs"],
        "Thermodynamics": ["Basic Concepts","First Law","Second Law","Entropy","Availability","Gas Power Cycles","Vapour Power Cycles","Refrigeration","Psychrometrics","Combustion"],
        "Structural Analysis": ["Determinate Structures","Virtual Work","Influence Lines","Arches","Cables","Indeterminate Structures","Stiffness Method","Matrix Methods","Dynamic Analysis","Plastic Analysis"],
        "Statistics & Probability": ["Descriptive Statistics","Probability Basics","Distributions (Normal,Binomial,Poisson)","Hypothesis Testing","Confidence Intervals","Correlation","Regression Analysis","Bayesian Statistics","Sampling Techniques","ANOVA"],
        "Machine Learning": ["Supervised Learning","Unsupervised Learning","Linear Regression","Logistic Regression","Decision Trees","Random Forest","SVM","K-Means Clustering","Model Evaluation","Overfitting & Regularization"],
        "Data Visualization": ["matplotlib Basics","seaborn","ggplot2","Bar & Line Charts","Scatter & Bubble Plots","Heatmaps","Box & Violin Plots","Interactive Plots (Plotly)","Dashboard Design","Storytelling with Data"],
        "Python for DS": ["NumPy Arrays","Pandas DataFrames","Data Cleaning","Handling Missing Values","Data Aggregation","Merging & Joining","String Operations","DateTime Handling","File I/O","Pipelines"],
        "SQL & Databases": ["SELECT & WHERE","JOINs","GROUP BY & HAVING","Subqueries","Window Functions","Indexes","Stored Procedures","NoSQL Basics","MongoDB Queries","Database Design"],
        "Feature Engineering": ["Feature Selection","Encoding Categorical Variables","Scaling & Normalization","PCA","Feature Extraction","Handling Imbalanced Data","Outlier Detection","Dimensionality Reduction","Text Features (TF-IDF)","Datetime Features"],
        "Big Data Analytics": ["Hadoop Ecosystem","MapReduce","Apache Spark","HDFS","Hive & Pig","Kafka Basics","Data Warehousing","ETL Pipelines","Cloud Platforms (AWS/GCP)","Batch vs Stream Processing"],
        "Deep Learning": ["Neural Networks Basics","Activation Functions","Backpropagation","CNNs","RNNs & LSTMs","Transfer Learning","GANs","Transformers","Hyperparameter Tuning","Model Deployment"],
        "Time Series Analysis": ["Stationarity","Autocorrelation","ARIMA Models","Seasonal Decomposition","Exponential Smoothing","LSTM for Time Series","Anomaly Detection","Forecasting Metrics","Rolling Statistics","Cross-Validation for TS"],
        "Data Mining": ["Association Rules (Apriori)","Clustering Algorithms","Classification Techniques","Anomaly Detection","Web Mining","Text Mining","Market Basket Analysis","Pattern Recognition","Evaluation Metrics","Ethical Considerations"],
    }

    BRANCH_SUBJS = {
        "Computer Engineering":       ["Data Structures","DBMS","Operating Systems","Computer Networks","Algorithms","Compiler Design","Software Engineering","Theory of Computation","Computer Architecture","Discrete Mathematics"],
        "Information Technology":     ["Web Technologies","Data Structures","DBMS","Computer Networks","Software Engineering","Cloud Computing","Cybersecurity","Mobile Applications","Data Mining","AI & ML"],
        "Electronics & Communication":["Signals & Systems","Digital Electronics","Analog Circuits","Communication Systems","VLSI Design","Microprocessors","Control Systems","Electromagnetic Theory","DSP","Antenna Theory"],
        "Mechanical Engineering":     ["Engineering Mechanics","Thermodynamics","Fluid Mechanics","Machine Design","Manufacturing Processes","Heat Transfer","Theory of Machines","Material Science","CAD/CAM","Industrial Engineering"],
        "Civil Engineering":          ["Structural Analysis","Fluid Mechanics","Geotechnical Engineering","Transportation Engineering","Environmental Engineering","RCC Design","Surveying","Construction Management","Hydraulics","Soil Mechanics"],
        "Electrical Engineering":     ["Circuit Theory","Electrical Machines","Power Systems","Control Systems","Power Electronics","Measurements","Electromagnetics","Analog Electronics","Digital Electronics","Signals & Systems"],
        "Chemical Engineering":       ["Chemical Reaction Engineering","Mass Transfer","Heat Transfer","Fluid Mechanics","Thermodynamics","Process Control","Chemical Technology","Transport Phenomena","Instrumentation","Safety Engineering"],
        "Biotechnology":              ["Biochemistry","Molecular Biology","Cell Biology","Genetic Engineering","Microbiology","Bioprocess Engineering","Bioinformatics","Immunology","Enzymology","Bioethics"],
        "Data Science":               ["Statistics & Probability","Machine Learning","Data Visualization","Python for DS","SQL & Databases","Feature Engineering","Big Data Analytics","Deep Learning","Time Series Analysis","Data Mining"],
    }

    branches = list(BRANCH_SUBJS.keys())
    sc1, sc2 = st.columns(2)
    branch  = sc1.selectbox("🏫 Branch", branches,
                             index=branches.index(st.session_state.syllabus_branch)
                             if st.session_state.syllabus_branch in branches else 0,
                             key="syl_branch")
    st.session_state.syllabus_branch = branch
    avail_subjs = BRANCH_SUBJS.get(branch, list(SYLLABUS.keys())[:3])
    subject = sc2.selectbox("📚 Subject", avail_subjs, key="syl_subj")
    st.session_state.syllabus_subject = subject

    topics = SYLLABUS.get(subject, [])
    if subject not in st.session_state.syllabus_topics:
        st.session_state.syllabus_topics[subject] = {t: False for t in topics}

    topic_state = st.session_state.syllabus_topics[subject]
    done_count = sum(1 for v in topic_state.values() if v)
    total      = len(topics)
    pct        = int(done_count / total * 100) if total else 0

    # Progress bar
    bar_color = "#16a34a" if pct >= 70 else "#d97706" if pct >= 40 else "#dc2626"
    st.markdown(f"""
    <div style="background:#fff;border:2px solid #ede9fe;border-radius:16px;padding:16px 20px;margin-bottom:18px;">
    <div style="display:flex;justify-content:space-between;margin-bottom:8px;">
    <b style="color:#4c1d95;">{subject} — Syllabus Coverage</b>
    <span style="font-weight:700;color:{bar_color};font-size:1.1rem;">{pct}%</span>
    </div>
    <div style="background:#ede9fe;border-radius:8px;height:14px;">
    <div style="width:{pct}%;background:{bar_color};height:14px;border-radius:8px;
    transition:width 0.4s;"></div></div>
    <div style="font-size:0.78rem;color:#6b7280;margin-top:6px;">{done_count}/{total} topics completed</div>
    </div>""", unsafe_allow_html=True)

    st.markdown("#### 📋 Topics")
    cols = st.columns(2)
    for ti, topic in enumerate(topics):
        with cols[ti % 2]:
            checked = topic_state.get(topic, False)
            new_val = st.checkbox(topic, value=checked, key=f"syl_{subject}_{ti}")
            if new_val != checked:
                st.session_state.syllabus_topics[subject][topic] = new_val
                st.rerun()

    bc1, bc2 = st.columns(2)
    if bc1.button("✅ Mark All Complete", key="syl_all", use_container_width=True):
        for t in topics:
            st.session_state.syllabus_topics[subject][t] = True
        st.rerun()
    if bc2.button("🔄 Reset Progress", key="syl_reset", use_container_width=True):
        for t in topics:
            st.session_state.syllabus_topics[subject][t] = False
        st.rerun()


# ── 8. SMART REMINDERS
def show_reminders():
    _nav_back("🔔 Smart Reminders", "reminders")

    st.markdown("""
    <div style="background:linear-gradient(90deg,#d97706,#b45309);
    border-radius:16px;padding:18px 28px;margin-bottom:22px;color:#fff;">
    <h2 style="margin:0;color:#fff!important;">🔔 Smart Reminders</h2>
    <p style="margin:4px 0 0;opacity:0.9;font-size:0.87rem;">AI-suggested daily study reminders based on weak subjects & exam proximity</p>
    </div>""", unsafe_allow_html=True)

    import time as _t

    # Manual reminder
    # ── Custom toggle (replaces st.expander to avoid arrow_down text bug)
    if "rem_form_open" not in st.session_state:
        st.session_state.rem_form_open = False
    _rem_lbl = "🔼 Hide Form" if st.session_state.rem_form_open else "➕ Add Custom Reminder"
    if st.button(_rem_lbl, key="rem_toggle", use_container_width=True):
        st.session_state.rem_form_open = not st.session_state.rem_form_open
        st.rerun()
    if st.session_state.rem_form_open:
        st.markdown("""<div style="background:#f8f5ff;border:2px solid #c4b5fd;
            border-radius:14px;padding:16px 18px 10px 18px;margin-bottom:10px;">
            </div>""", unsafe_allow_html=True)
        rc1, rc2, rc3 = st.columns([3, 2, 1])
        r_text    = rc1.text_input("📌 Reminder", key="rem_text", placeholder="e.g. Revise OS Deadlock chapter")
        r_date    = rc2.date_input("📅 Date", key="rem_date", min_value=dt_date.today())
        if rc3.button("➕ Add", key="rem_add", use_container_width=True):
            if r_text.strip():
                st.session_state.reminders.append({
                    "id": str(int(_t.time()*1000)),
                    "text": r_text.strip(),
                    "date": str(r_date),
                    "done": False,
                    "type": "manual"
                })
                st.session_state.rem_form_open = False
                st.success("✅ Reminder added!")
                st.rerun()

    # AI-generated reminders
    st.markdown("### 🤖 Generate AI Study Reminders")
    gc1, gc2 = st.columns(2)
    weak_subj  = gc1.text_input("📚 Weak Subject(s)", key="rem_weak",
                                  placeholder="e.g. OS, DBMS", value=st.session_state.get("weakest_subject",""))
    days_ahead = gc2.slider("📅 Generate for next N days", 3, 14, 7, key="rem_days")

    if st.button("🤖 Generate Smart Reminders", key="rem_gen", use_container_width=True):
        with st.spinner("Generating personalised reminders..."):
            try:
                prompt = (f"Generate {days_ahead} daily study reminders for an engineering student. "
                          f"Weak subjects: {weak_subj if weak_subj else 'general subjects'}. "
                          f"Make each reminder specific, actionable (e.g. 'Solve 5 OS scheduling problems'). "
                          f"One reminder per day. Format: Day 1: [reminder text]")
                messages = [{"role": "system", "content": "You are a helpful academic study coach."}, {"role": "user", "content": prompt}]
                res_raw = safe_chat(messages, temperature=0.5, max_tokens=500)
                if res_raw is None: raise Exception("AI service unavailable. Check API key.")
                class _R: pass
                res = _R()
                class _C: pass
                res.choices = [_C()]
                res.choices[0].message = _C()
                res.choices[0].message.content = res_raw
                raw = res.choices[0].message.content.strip()
                lines = [l.strip() for l in raw.split('\n') if l.strip() and ('Day' in l or l[0].isdigit())]
                from datetime import timedelta
                for di, line in enumerate(lines[:days_ahead]):
                    r_date = dt_date.today() + timedelta(days=di)
                    text = line.split(':', 1)[-1].strip() if ':' in line else line
                    st.session_state.reminders.append({
                        "id": str(int(_t.time()*1000)) + str(di),
                        "text": text,
                        "date": str(r_date),
                        "done": False,
                        "type": "ai"
                    })
                st.success(f"✅ {len(lines)} AI reminders generated!")
                st.rerun()
            except Exception as e:
                st.error(f"Error: {e}")

    if not st.session_state.reminders:
        st.markdown("""<div style="text-align:center;padding:30px;color:#9ca3af;">
        🔔 No reminders yet. Generate AI reminders or add your own!</div>""", unsafe_allow_html=True)
        return

    st.markdown("### 📋 Your Reminders")
    today = str(dt_date.today())
    sorted_rems = sorted(st.session_state.reminders, key=lambda x: x["date"])

    for rem in sorted_rems:
        is_today = rem["date"] == today
        is_past  = rem["date"] < today
        is_done  = rem["done"]
        bg     = "#f0fdf4" if is_done else "#fffbeb" if is_today else "#fff"
        border = "#86efac" if is_done else "#fcd34d" if is_today else "#ede9fe"
        icon   = "✅" if is_done else "🔔" if is_today else "📅"
        ai_tag = '<span style="background:#ede9fe;color:#7c3aed;border-radius:8px;padding:1px 6px;font-size:0.68rem;margin-left:6px;">AI</span>' if rem.get("type")=="ai" else ""
        st.markdown(f"""
        <div style="background:{bg};border:1.5px solid {border};border-radius:12px;
        padding:12px 16px;margin-bottom:6px;display:flex;align-items:center;gap:12px;
        opacity:{'0.6' if is_past and not is_today else '1'};">
        <span style="font-size:1.3rem;">{icon}</span>
        <div style="flex:1;">
        <span style="color:#1e1e2e;{'text-decoration:line-through;color:#9ca3af;' if is_done else ''}">{rem['text']}</span>{ai_tag}
        <div style="font-size:0.75rem;color:#9ca3af;margin-top:2px;">{rem['date']}{'  🔴 TODAY' if is_today else ''}</div>
        </div></div>""", unsafe_allow_html=True)

        rc1, rc2 = st.columns([1, 1])
        if not is_done:
            if rc1.button("✅ Done", key=f"rem_done_{rem['id']}", use_container_width=True):
                for r in st.session_state.reminders:
                    if r["id"] == rem["id"]: r["done"] = True
                st.rerun()
        if rc2.button("🗑️", key=f"rem_del_{rem['id']}", use_container_width=True):
            st.session_state.reminders = [r for r in st.session_state.reminders if r["id"] != rem["id"]]
            st.rerun()

    if st.button("🗑️ Clear All Done", key="rem_clear_done"):
        st.session_state.reminders = [r for r in st.session_state.reminders if not r["done"]]
        st.rerun()


# ── ROUTING
if not st.session_state.logged_in:
    show_login(); st.stop()
if st.session_state.app_mode is None:
    show_home(); st.stop()
if st.session_state.app_mode == "coding":
    show_coding(); st.stop()
if st.session_state.app_mode == "schedule":
    show_schedule(); st.stop()
if st.session_state.app_mode == "subtest":
    show_subtest(); st.stop()
if st.session_state.app_mode == "gate":
    show_gate(); st.stop()
# ── Group 2: Career & Performance
if st.session_state.app_mode == "interview":
    show_interview(); st.stop()
if st.session_state.app_mode == "notes":
    show_notes(); st.stop()
if st.session_state.app_mode == "cgpa":
    show_cgpa(); st.stop()
if st.session_state.app_mode == "leaderboard":
    show_leaderboard(); st.stop()
# ── Group 3: Exam Specific
if st.session_state.app_mode == "countdown":
    show_countdown(); st.stop()
if st.session_state.app_mode == "pyq":
    show_pyq(); st.stop()
if st.session_state.app_mode == "syllabus":
    show_syllabus(); st.stop()
if st.session_state.app_mode == "reminders":
    show_reminders(); st.stop()
# else → tracker falls through to sidebar below

# ─────────────────────────────────────────────
# 7. SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='text-align:center; padding:10px 0 5px 0;'>
        <span style='font-family:Orbitron,sans-serif; font-size:1.4rem; font-weight:900;
        background:linear-gradient(135deg,#7c3aed,#4f46e5,#06b6d4);
        -webkit-background-clip:text; -webkit-text-fill-color:transparent;
        background-clip:text; letter-spacing:2px;'>🎓 MENTORA AI</span>
        <div style='height:2px; background:linear-gradient(90deg,#7c3aed,#06b6d4);
        border-radius:2px; margin:6px 0 12px 0;'></div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("### 👤 Student Profile")

    st.session_state.student_name    = st.text_input("Full Name", st.session_state.student_name, key="sb_student_name")
    st.session_state.roll_no         = st.text_input("Roll / Enrollment No.", st.session_state.roll_no, key="sb_roll_no")
    st.session_state.university_name = st.text_input("University / College", st.session_state.university_name,
                                                      placeholder="e.g. MIT, VIT, BITS", key="sb_university")
    st.session_state.user_branch     = st.selectbox("Engineering Branch", [
        "Computer Engineering",
        "Information Technology",
        "Electronics & Communication",
        "Electrical Engineering",
        "Mechanical Engineering",
        "Civil Engineering",
        "Chemical Engineering",
        "Biotechnology Engineering",
        "Artificial Intelligence & ML",
        "Data Science",
    ], index=0, key="sb_user_branch")
    st.session_state.user_year       = st.selectbox("Year / Semester", [
        "First Year (Sem 1)",
        "First Year (Sem 2)",
        "Second Year (Sem 3)",
        "Second Year (Sem 4)",
        "Third Year (Sem 5)",
        "Third Year (Sem 6)",
        "Final Year (Sem 7)",
        "Final Year (Sem 8)",
    ], index=0, key="sb_user_year")
    st.session_state.attendance      = st.slider("Attendance %", 0, 100, st.session_state.attendance, key="sb_attendance")
    st.session_state.activities      = st.text_input("Extra-curricular / Projects",
                                                      st.session_state.activities,
                                                      placeholder="e.g. Hackathon, NSS, Sports", key="sb_activities")
    st.divider()

    # Badges
    if st.session_state.badges:
        st.markdown("### 🏅 Achievements")
        st.write("  ".join(st.session_state.badges))
        st.divider()

    # Streak
    st.markdown(f"### 🔥 Study Streak: **{st.session_state.streak} day(s)**")
    st.divider()

    # Reset
    if st.button("🏠 Back to Home", key="back_home_btn", use_container_width=True):
        st.session_state.app_mode = None; st.rerun()
    if st.button("🔄 Reset Tracker",      key="reset_btn",      use_container_width=True):
        st.session_state.clear()
        st.rerun()

    st.divider()

    # Chatbot — quick sidebar version
    st.markdown("### 💬 Quick Chat")
    st.caption("Ask a quick question below, or use the **Chat Assistant tab** in the main menu for full conversation.")
    user_msg = st.text_input("Ask anything:", key="chat_input", placeholder="e.g. Explain Ohm's Law")
    if st.button("Send", key="chat_send_btn") and user_msg:
        try:
            # Build full message history for memory
            messages = [
                {
                    "role": "system",
                    "content": (
                        f"You are an expert university professor and academic mentor. "
                        f"Student Branch: {st.session_state.user_branch}, "
                        f"Year: {st.session_state.user_year}, "
                        f"Weak Subject: {st.session_state.weakest_subject or 'Not identified yet'}. "
                        f"Answer with proper technical depth suitable for an engineering student. "
                        f"Be concise but thorough."
                    )
                }
            ]
            # Add conversation history for memory
            for chat in st.session_state.chat_history[-6:]:
                messages.append({"role": "user",      "content": chat["user"]})
                messages.append({"role": "assistant",  "content": chat["ai"]})
            messages.append({"role": "user", "content": user_msg})

            res_raw = safe_chat(messages, temperature=0.3, max_tokens=1500)
            if res_raw is None: raise Exception("AI service unavailable. Check API key.")
            class _R: pass
            res = _R()
            class _C: pass
            res.choices = [_C()]
            res.choices[0].message = _C()
            res.choices[0].message.content = res_raw
            st.session_state.chat_history.append({
                "user": user_msg,
                "ai":   res.choices[0].message.content.strip()
            })
            st.rerun()
        except Exception:
            st.error("Chat error. Try again.")

    # Show last 2 messages in sidebar
    for chat in reversed(st.session_state.chat_history[-2:]):
        st.caption(f"**You:** {chat['user']}")
        st.caption(f"**AI:** {chat['ai'][:200]}{'...' if len(chat['ai']) > 200 else ''}")

# ─────────────────────────────────────────────
# 8. PHASE: INPUT
# ─────────────────────────────────────────────
if st.session_state.phase == "input":
    st.markdown('<div class="phase-header">MENTORA AI &mdash; Academic Analysis Dashboard</div>',
                unsafe_allow_html=True)

    # ── Step 1: Add Subjects
    st.markdown("""
    <div style="background:#ffffff; border:2px solid #7c3aed; border-radius:14px;
    padding:18px 22px 10px 22px; margin-bottom:16px;
    box-shadow:0 4px 15px rgba(124,58,237,0.1);">
    <h4 style="color:#4c1d95; margin:0 0 12px 0; font-family:Poppins,sans-serif;">
    📚 Step 1 — Add Your Engineering Subjects</h4>
    </div>
    """, unsafe_allow_html=True)

    with st.container():
        st.markdown("**Enter your subjects separated by commas:**")
        sub_raw = st.text_area(
            "Subjects",
            placeholder="e.g. Data Structures, DBMS, Computer Networks, OS, Maths",
            label_visibility="collapsed",
            key="subject_input_area"
        )
        if st.button("➕ Add Subjects", key="add_subjects_btn"):
            new = [s.strip() for s in sub_raw.split(",") if s.strip()]
            if not new:
                st.warning("⚠️ Please type at least one subject name.")
            else:
                added = 0
                for s in new:
                    if s not in st.session_state.subjects_data:
                        st.session_state.subjects_data[s] = {"IA1": 0, "IA2": 0}
                        added += 1
                if added:
                    st.success(f"✅ {added} subject(s) added!")
                else:
                    st.info("These subjects are already added.")
                st.rerun()

    if st.session_state.subjects_data:
        st.divider()
        col_input, col_viz = st.columns([1, 1], gap="large")

        with col_input:
            st.subheader("✏️ Step 2 — Enter Internal Assessment Marks")

            # Column headers
            h1, h2, h3, h4 = st.columns([2, 1, 1, 0.5])
            h1.markdown("**Subject**")
            h2.markdown("**IA1** *(0–30)*")
            h3.markdown("**IA2** *(0–30)*")
            h4.markdown("**Del**")
            st.divider()

            validation_ok = True
            for sub in list(st.session_state.subjects_data.keys()):
                c1, c2, c3, c4 = st.columns([2, 1, 1, 0.5])
                c1.markdown(f"**{sub}**")

                ia1 = c2.number_input(
                    f"IA1 {sub}", min_value=0, max_value=30, step=1,
                    value=int(st.session_state.subjects_data[sub].get("IA1", 0)),
                    key=f"ut1_{sub}",
                    label_visibility="collapsed"
                )
                ia2 = c3.number_input(
                    f"IA2 {sub}", min_value=0, max_value=30, step=1,
                    value=int(st.session_state.subjects_data[sub].get("IA2", 0)),
                    key=f"ut2_{sub}",
                    label_visibility="collapsed"
                )

                # Delete subject button
                if c4.button("🗑️", key=f"del_{sub}", help=f"Remove {sub}"):
                    del st.session_state.subjects_data[sub]
                    st.rerun()

                if not (0 <= ia1 <= 30 and 0 <= ia2 <= 30):
                    st.error(f"❌ {sub}: Marks must be between 0 and 30.")
                    validation_ok = False

                st.session_state.subjects_data[sub]["IA1"] = ia1
                st.session_state.subjects_data[sub]["IA2"] = ia2

            st.write("")

            # Attendance warning
            if st.session_state.attendance < 75:
                st.warning("⚠️ Attendance below 75% — may affect exam eligibility!")

            # Summary before proceeding
            if st.session_state.subjects_data and validation_ok:
                avgs = {s: (v["IA1"]+v["IA2"])/2
                        for s, v in st.session_state.subjects_data.items()}
                weakest = min(avgs, key=avgs.get)
                st.info(f"🔍 Detected weak subject: **{weakest}** — the plan will focus here.")

            if st.button("🚀 Analyse & Start Plan",
                         disabled=not validation_ok,
                         key="start_plan_btn"):
                if not st.session_state.subjects_data:
                    st.error("Please add at least one subject first!")
                else:
                    avgs = {s: (v["IA1"]+v["IA2"])/2
                            for s, v in st.session_state.subjects_data.items()}
                    st.session_state.weakest_subject = min(avgs, key=avgs.get)

                    # Save to CSV
                    row = {
                        "Date":         datetime.now().strftime("%Y-%m-%d %H:%M"),
                        "Name":         st.session_state.student_name,
                        "Roll":         st.session_state.roll_no,
                        "Year":         st.session_state.user_year,
                        "Attendance":   st.session_state.attendance,
                        "Activities":   st.session_state.activities,
                        "Weak Subject": st.session_state.weakest_subject,
                    }
                    for s, v in st.session_state.subjects_data.items():
                        row[f"{s}_UT1"] = v["IA1"]
                        row[f"{s}_UT2"] = v["IA2"]
                    save_to_csv(row)

                    st.session_state.phase = "pre_quiz"
                    st.rerun()
        with col_viz:
            st.subheader("📈 Live Performance Preview")
            chart_list = []
            for s, v in st.session_state.subjects_data.items():
                chart_list.append({"Subject": s, "Exam": "IA1", "Score": v["IA1"]})
                chart_list.append({"Subject": s, "Exam": "IA2", "Score": v["IA2"]})
            try:
                df = pd.DataFrame(chart_list)
                if not df.empty:
                    st.bar_chart(df, x="Subject", y="Score", color="Exam", stack=False)
            except Exception:
                for item in chart_list:
                    st.write(f"**{item['Subject']}** {item['Exam']}: {item['Score']}/30")
                st.caption("Marks out of 20 — updates live as you type.")

            # Improvement indicators
            st.subheader("📉 Improvement Overview")
            for s, v in st.session_state.subjects_data.items():
                imp = improvement_pct(v["IA1"], v["IA2"])
                color = "🟢" if imp >= 0 else "🔴"
                avg   = (v["IA1"]+v["IA2"])/2
                rl, badge = risk_label(avg / 20 * 100)
                st.markdown(
                    f"{color} **{s}**: Avg {avg:.1f}  |  "
                    f"Improvement **{imp:+.1f}%**  |  "
                    f"Risk: <span class='{badge}'>{rl}</span>",
                    unsafe_allow_html=True
                )
    else:
        st.info("Start by adding subjects above ☝️")

# ─────────────────────────────────────────────
# 9. PHASE: PRE-QUIZ (3 sets × 7 MCQs)
# ─────────────────────────────────────────────
elif st.session_state.phase == "pre_quiz":
    st.markdown(
        f'<div class="phase-header">📝 Phase 1 — Diagnostic Pre-Test | {st.session_state.weakest_subject}</div>',
        unsafe_allow_html=True)
    st.caption("3 sets of 7 MCQs each · Total = 21 marks")

    # Generate all 3 sets if not done yet
    if not st.session_state.pre_quiz_sets:
        st.session_state.pre_quiz_sets = generate_3_sets()
        st.session_state.pre_set_scores = []
        st.session_state.pre_set_index  = 0
        st.rerun()

    idx = st.session_state.pre_set_index

    if idx < 3:
        qs = st.session_state.pre_quiz_sets[idx]
        if not qs:
            st.error("Could not load questions. Please reset and retry.")
        else:
            st.subheader(f"Set {idx+1} of 3")
            progress = st.progress((idx) / 3)
            with st.form(f"pre_set_{idx}"):
                answers = []
                for i, q in enumerate(qs):
                    st.write(f"**Q{i+1}:** {q['question']}")
                    answers.append(
                        st.radio(f"Q{i+1}", q["options"], key=f"pq_{idx}_{i}",
                                 label_visibility="collapsed")
                    )
                if st.form_submit_button(f"Submit Set {idx+1}"):
                    score = sum(
                        1 for i, q in enumerate(qs)
                        if is_correct(answers[i], q["answer"])
                    )
                    st.session_state.pre_set_scores.append(score)
                    st.session_state.pre_set_index += 1
                    if st.session_state.pre_set_index == 3:
                        st.session_state.pre_score = sum(st.session_state.pre_set_scores)
                        st.session_state.phase = "results"
                    st.rerun()
    else:
        # Shouldn't reach here, but just in case
        st.session_state.pre_score = sum(st.session_state.pre_set_scores)
        st.session_state.phase = "results"
        st.rerun()

# ─────────────────────────────────────────────
# 10. PHASE: RESULTS / MAIN MENU
# ─────────────────────────────────────────────
elif st.session_state.phase == "results":
    name = st.session_state.student_name or "Student"
    subj = st.session_state.weakest_subject
    pre  = st.session_state.pre_score
    post = st.session_state.post_score

    st.markdown(
        f'<div class="phase-header">🏆 Strategy Roadmap — {name}</div>',
        unsafe_allow_html=True)

    # Top metrics
    pct = (post / 21 * 100) if post > 0 else 0
    rl, badge = risk_label(pct if post else (pre/21*100))
    
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.markdown(f'<div class="metric-card"><h2>{pre}/21</h2><p>Pre-Test Score</p></div>',
                    unsafe_allow_html=True)
    with m2:
        st.markdown(f'<div class="metric-card"><h2>{post}/21</h2><p>Post-Test Score</p></div>',
                    unsafe_allow_html=True)
    with m3:
        st.markdown(f'<div class="metric-card"><h2>{st.session_state.attendance}%</h2><p>Attendance</p></div>',
                    unsafe_allow_html=True)
    with m4:
        st.markdown(
            f'<div class="metric-card"><h2><span class="{badge}">{rl}</span></h2><p>Risk Level</p></div>',
            unsafe_allow_html=True)

    st.divider()

    # ── MAIN MENU TABS
    tabs = st.tabs([
        "📊 Dashboard",
        "📈 Subject Analysis",
        "🎯 Attendance & CGPA",
        "📜 Progress History",
        "🗓️ 30-Day Plan",
        "🧠 Final Assessment",
        "💬 Chat Assistant"
    ])

    # ════════════════════════════════════════════
    # TAB 1 — DASHBOARD: Summary overview + IA chart + weak subject spotlight
    # ════════════════════════════════════════════
    with tabs[0]:
        st.subheader("📊 Overall IA Performance")
        chart_list = []
        for s, v in st.session_state.subjects_data.items():
            chart_list += [
                {"Subject": s, "Exam": "IA1", "Score": v["IA1"]},
                {"Subject": s, "Exam": "IA2", "Score": v["IA2"]},
            ]
        try:
            df = pd.DataFrame(chart_list)
            if not df.empty:
                st.bar_chart(df, x="Subject", y="Score", color="Exam", stack=False)
                st.caption("IA1 vs IA2 marks out of 30 for each subject.")
        except Exception:
            if chart_list:
                for item in chart_list:
                    st.write(f"**{item['Subject']}** — {item['Exam']}: {item['Score']}/30")

        st.divider()

        # Subject summary table
        st.subheader("📋 Subject-wise Summary Table")
        rows = []
        for s, v in st.session_state.subjects_data.items():
            avg = (v["IA1"] + v["IA2"]) / 2
            imp = improvement_pct(v["IA1"], v["IA2"])
            pct_score = round(avg / 30 * 100, 1)
            rl, _ = risk_label(pct_score)
            rows.append({
                "Subject": s,
                "IA1": v["IA1"],
                "IA2": v["IA2"],
                "Average": f"{avg:.1f}",
                "% Score": f"{pct_score}%",
                "Improvement": f"{imp:+.1f}%",
                "Risk": rl
            })
        st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)

        st.divider()

        # Weak subject spotlight
        st.subheader(f"🔦 Weak Subject Spotlight: {subj}")
        col1, col2 = st.columns(2)
        if subj in st.session_state.subjects_data:
            sv = st.session_state.subjects_data[subj]
            avg_weak = (sv["IA1"] + sv["IA2"]) / 2
            col1.metric("IA1 Score", f"{sv['IA1']}/30")
            col2.metric("IA2 Score", f"{sv['IA2']}/30")
            st.info(f"⚠️ **{subj}** has been identified as your weakest subject with an average of **{avg_weak:.1f}/30**. The 30-Day Plan and MCQ tests focus here.")

        if post > 0:
            st.divider()
            st.subheader("🏁 Pre vs Post Test Comparison")
            comp_df = pd.DataFrame({
                "Test":  ["Pre-Test", "Post-Test"],
                "Score": [pre, post]
            })
            st.bar_chart(comp_df.set_index("Test"))
            if pct >= 60:
                st.success(f"✅ PASS — Final Score: {pct:.1f}%")
            elif pct >= 40:
                st.warning(f"⚠️ BORDERLINE — Final Score: {pct:.1f}%")
            else:
                st.error(f"❌ FAIL — Final Score: {pct:.1f}%")

    # ════════════════════════════════════════════
    # TAB 2 — SUBJECT ANALYSIS: Deep per-subject breakdown
    # ════════════════════════════════════════════
    with tabs[1]:
        st.subheader("📈 Deep Subject-wise Analysis")

        # Select subject to analyse
        subject_list = list(st.session_state.subjects_data.keys())
        selected_sub = st.selectbox("Select a subject to analyse:", subject_list, key="sub_analysis_select")

        if selected_sub:
            sv = st.session_state.subjects_data[selected_sub]
            ia1, ia2 = sv["IA1"], sv["IA2"]
            avg  = (ia1 + ia2) / 2
            imp  = improvement_pct(ia1, ia2)
            pct_s = round(avg / 30 * 100, 1)
            rl, bg = risk_label(pct_s)

            # Metric row
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("IA1", f"{ia1}/30")
            c2.metric("IA2", f"{ia2}/30", delta=f"{ia2-ia1:+}")
            c3.metric("Average", f"{avg:.1f}/30")
            c4.metric("Risk Level", rl)

            st.divider()

            # Score trend for this subject
            st.subheader(f"📉 Score Trend — {selected_sub}")
            trend_df = pd.DataFrame({
                "Assessment": ["IA1", "IA2"],
                "Score": [ia1, ia2]
            }).set_index("Assessment")
            st.line_chart(trend_df)

            st.divider()

            # Performance breakdown
            st.subheader("🔍 Performance Breakdown")
            col_a, col_b = st.columns(2)
            with col_a:
                st.markdown(f"**Percentage Score:** {pct_s}%")
                st.progress(pct_s / 100)
                st.markdown(f"**Improvement from IA1→IA2:** {imp:+.1f}%")
                if imp > 0:
                    st.success("📈 Improving trend — keep it up!")
                elif imp == 0:
                    st.info("➡️ Stable — try to push higher in final exam.")
                else:
                    st.error("📉 Declining trend — needs immediate attention!")

            with col_b:
                st.markdown("**Grade Prediction (based on avg):**")
                if pct_s >= 85:
                    st.success("🏆 Predicted Grade: **O (Outstanding)**")
                elif pct_s >= 75:
                    st.success("🥇 Predicted Grade: **A+ (Excellent)**")
                elif pct_s >= 65:
                    st.info("🥈 Predicted Grade: **A (Very Good)**")
                elif pct_s >= 55:
                    st.info("🥉 Predicted Grade: **B+ (Good)**")
                elif pct_s >= 45:
                    st.warning("⚠️ Predicted Grade: **B (Average)**")
                else:
                    st.error("❌ Predicted Grade: **Fail Risk**")

                st.markdown(f"**Marks needed in End-Sem (out of 70) to pass:**")
                needed = max(0, round(40 - avg, 1))
                st.metric("Min End-Sem Marks", f"{needed}/70")

    # ════════════════════════════════════════════
    # TAB 3 — ATTENDANCE & CGPA ESTIMATOR
    # ════════════════════════════════════════════
    with tabs[2]:
        st.subheader("🎯 Attendance Analysis")

        att = st.session_state.attendance
        col1, col2, col3 = st.columns(3)
        col1.metric("Current Attendance", f"{att}%")
        col2.metric("Min Required", "75%")
        col3.metric("Status", "✅ Safe" if att >= 75 else "❌ At Risk")

        # Attendance bar
        st.progress(att / 100)

        # Attendance breakdown chart
        att_df = pd.DataFrame({
            "Status": ["Classes Attended", "Classes Missed"],
            "Percentage": [att, 100 - att]
        }).set_index("Status")
        st.bar_chart(att_df)

        if att < 75:
            st.error("🚨 CRITICAL: Attendance below 75%. You may be DETAINED from exams!")
            shortage = 75 - att
            st.markdown(f"You need to attend **{shortage:.0f}%** more classes to reach the minimum.")
        elif att < 85:
            st.warning("⚠️ Attendance is below 85%. Try to attend more classes.")
        else:
            st.success("✅ Excellent attendance! You are on the safe side.")

        st.divider()

        # CGPA Estimator
        st.subheader("🎓 CGPA Estimator")
        st.caption("Enter your expected end-semester exam marks to estimate your CGPA.")

        cgpa_rows = []
        total_credits = 0
        total_weighted = 0

        for s, v in st.session_state.subjects_data.items():
            col_s, col_cr, col_es = st.columns([2, 1, 1])
            col_s.markdown(f"**{s}**")
            credits = col_cr.number_input(f"Credits {s}", 1, 5, 3,
                                           key=f"cred_{s}", label_visibility="collapsed")
            end_sem = col_es.number_input(f"End-Sem {s} (0-70)", 0, 70, 35,
                                           key=f"endsem_{s}", label_visibility="collapsed")
            ia_avg  = (v["IA1"] + v["IA2"]) / 2
            total   = ia_avg + end_sem
            total_pct = total / 100 * 100

            # Grade points
            if total_pct >= 90:   gp = 10
            elif total_pct >= 80: gp = 9
            elif total_pct >= 70: gp = 8
            elif total_pct >= 60: gp = 7
            elif total_pct >= 50: gp = 6
            elif total_pct >= 40: gp = 5
            else:                  gp = 0

            total_credits   += credits
            total_weighted  += gp * credits
            cgpa_rows.append({
                "Subject": s, "IA Avg": f"{ia_avg:.1f}",
                "End-Sem": end_sem, "Total": f"{total:.1f}/100",
                "Grade Point": gp, "Credits": credits
            })

        if cgpa_rows:
            st.dataframe(pd.DataFrame(cgpa_rows), use_container_width=True, hide_index=True)
            estimated_cgpa = round(total_weighted / total_credits, 2) if total_credits else 0
            st.divider()
            st.metric("🎓 Estimated CGPA (this semester)", estimated_cgpa)
            if estimated_cgpa >= 8.5:
                st.success("🏆 Excellent CGPA — First Class with Distinction!")
            elif estimated_cgpa >= 7.0:
                st.info("🥇 Good CGPA — First Class!")
            elif estimated_cgpa >= 5.5:
                st.warning("🥈 Average CGPA — Second Class.")
            else:
                st.error("❌ Low CGPA — Needs serious improvement.")

    # ════════════════════════════════════════════
    # TAB 4 — PROGRESS HISTORY: Timeline + daily scores
    # ════════════════════════════════════════════
    with tabs[3]:
        st.subheader("📜 Academic Progress History")

        # Session history log
        if st.session_state.history_log:
            st.markdown("#### 🗂️ Test History (This Session)")
            hist_rows = []
            for entry in st.session_state.history_log:
                imp_h = entry["post"] - entry["pre"]
                hist_rows.append({
                    "Date":      entry["date"],
                    "Subject":   entry["subject"],
                    "Pre-Test":  f"{entry['pre']}/21",
                    "Post-Test": f"{entry['post']}/21",
                    "Change":    f"{imp_h:+}",
                    "Result":    "✅ PASS" if entry["post"]/21*100 >= 60 else "❌ FAIL"
                })
            st.dataframe(pd.DataFrame(hist_rows), use_container_width=True, hide_index=True)
        else:
            st.info("No test history yet. Complete the pre-test and post-test to see history here.")

        st.divider()

        # CSV history
        st.markdown("#### 📁 Saved Performance Records")
        if os.path.isfile("performance_history.csv"):
            try:
                hist_df = pd.read_csv("performance_history.csv", on_bad_lines="skip")
                if st.session_state.student_name and "Name" in hist_df.columns:
                    hist_df = hist_df[hist_df["Name"] == st.session_state.student_name]
                st.dataframe(hist_df.tail(10), use_container_width=True, hide_index=True)
            except Exception as e:
                st.warning(f"⚠️ Could not read performance history: {e}. "
                           f"The file may be corrupt — it will be reset on your next submission.")
                if st.button("🗑️ Reset History File", key="reset_csv_btn"):
                    os.remove("performance_history.csv")
                    st.success("History file removed. Start fresh!")
                    st.rerun()
        else:
            st.info("No saved records yet.")

        st.divider()

        # Daily practice trend
        st.markdown("#### 📈 30-Day Daily Practice Score Trend")
        if st.session_state.daily_scores:
            ds = st.session_state.daily_scores
            daily_df = pd.DataFrame({
                "Day":   list(ds.keys()),
                "Score /5": list(ds.values())
            }).set_index("Day")
            st.line_chart(daily_df)

            # Stats
            scores = list(ds.values())
            c1, c2, c3 = st.columns(3)
            c1.metric("Best Day Score",    f"{max(scores)}/5")
            c2.metric("Average Score",     f"{sum(scores)/len(scores):.1f}/5")
            c3.metric("Days Completed",    f"{len(scores)}/30")
        else:
            st.info("No daily practice scores yet. Use the 30-Day Plan tab to practice.")

        st.divider()

        # Risk curve history
        st.markdown("#### 📉 Projected Risk Reduction Over 30 Days")
        risk_df = pd.DataFrame(
            {"Risk %": compute_risk_curve()},
            index=range(1, 31)
        )
        st.line_chart(risk_df)
        st.caption("Risk % is projected to reduce as you complete daily practice.")

    # ════════════════════════════════════════════
    # TAB 5 — 30-DAY PLAN: Topic + MCQ practice
    # ════════════════════════════════════════════
    with tabs[4]:
        st.subheader(f"🗓️ 30-Day Study Plan — {subj}")
        st.caption(f"Branch: {st.session_state.user_branch} | Year: {st.session_state.user_year}")

        if not st.session_state.daily_plan_objectives:
            st.info("Generate a personalised 30-day topic plan based on your syllabus.")
            if st.button("📅 Generate 30-Day Syllabus Plan", key="gen_30day_btn"):
                with st.spinner("Fetching university curriculum topics …"):
                    st.session_state.daily_plan_objectives = generate_30_day_objectives(subj)
                    st.rerun()
        else:
            days_done = len(st.session_state.daily_scores)
            st.progress(days_done / 30, text=f"🎯 {days_done}/30 days completed")

            # Full topic table
            st.markdown("""
            <div style="background:#f5f3ff; border:1.5px solid #c4b5fd; border-radius:12px;
            padding:10px 16px; margin-bottom:8px;">
            <b style="color:#4c1d95; font-family:Poppins,sans-serif;">
            📋 Full 30-Day Topic Plan</b></div>
            """, unsafe_allow_html=True)
            with st.container():
                plan_rows = []
                for i, t in enumerate(st.session_state.daily_plan_objectives):
                    status = "✅ Done" if (i+1) in st.session_state.daily_scores else "⬜ Pending"
                    score  = st.session_state.daily_scores.get(i+1, "—")
                    plan_rows.append({"Day": i+1, "Topic": t,
                                      "Score": f"{score}/5" if score != "—" else "—",
                                      "Status": status})
                st.dataframe(pd.DataFrame(plan_rows), use_container_width=True, hide_index=True)

            st.divider()
            day_idx = st.slider("Select Day to Practice", 1, 30, key="day_slider")
            topic   = st.session_state.daily_plan_objectives[day_idx - 1]

            col_t, col_s = st.columns([3, 1])
            col_t.info(f"**Day {day_idx} Topic:** {topic}")
            if day_idx in st.session_state.daily_scores:
                col_s.success(f"✅ Done: {st.session_state.daily_scores[day_idx]}/5")

            if st.button(f"🎯 Generate MCQs for Day {day_idx}", key=f"gen_mcq_day_{day_idx}"):
                with st.spinner(f"Generating {subj} MCQs on '{topic}' …"):
                    st.session_state.current_day_mcqs = get_mcqs(subj, n=5, topic=topic)
                    st.session_state.current_day_idx  = day_idx
                st.rerun()

            if st.session_state.current_day_mcqs and st.session_state.get("current_day_idx") == day_idx:
                st.markdown(f"#### 📝 Practice MCQs — {topic}")
                with st.form(f"day_{day_idx}_form"):
                    d_ans = []
                    for i, q in enumerate(st.session_state.current_day_mcqs):
                        st.markdown(f"**Q{i+1}:** {q['question']}")
                        d_ans.append(st.radio(
                            f"Answer Q{i+1}", q["options"],
                            key=f"dq_{day_idx}_{i}",
                            label_visibility="collapsed"
                        ))
                        st.write("")
                    if st.form_submit_button("💾 Submit & Save Score"):
                        d_score = sum(
                            1 for i, q in enumerate(st.session_state.current_day_mcqs)
                            if is_correct(d_ans[i], q["answer"])
                        )
                        st.session_state.daily_scores[day_idx] = d_score
                        if day_idx == st.session_state.last_active_day + 1:
                            st.session_state.streak += 1
                        elif day_idx != st.session_state.last_active_day:
                            st.session_state.streak = 1
                        st.session_state.last_active_day = day_idx
                        check_badges(day_idx, d_score)
                        st.success(f"✅ Day {day_idx} Score: {d_score}/5")
                        st.rerun()

    # ════════════════════════════════════════════
    # TAB 6 — FINAL ASSESSMENT + AI FEEDBACK + PDF
    # ════════════════════════════════════════════
    with tabs[5]:
        st.subheader("🧠 Final Post-Test Assessment")
        st.caption("Complete your 30-day plan first, then take this final test to measure improvement.")

        if st.button("📝 Generate Final Assessment (21 MCQs)", key="gen_final_btn"):
            with st.spinner("Building your final university-level test …"):
                sets = []
                for i in range(3):
                    sets.append(get_mcqs(subj, n=7, type_label="final"))
                flat = [q for s in sets for q in s]
                st.session_state.post_quiz_data = flat
                st.session_state.post_score = 0
                st.rerun()

        if st.session_state.post_quiz_data:
            st.markdown(f"#### 📋 Final Test — {subj} ({st.session_state.user_branch})")
            with st.form("post_quiz_form"):
                p_ans = []
                for i, q in enumerate(st.session_state.post_quiz_data):
                    st.markdown(f"**Q{i+1}:** {q['question']}")
                    p_ans.append(st.radio(
                        f"Answer {i+1}", q["options"],
                        key=f"pstq_{i}",
                        label_visibility="collapsed"
                    ))
                    st.write("")
                if st.form_submit_button("✅ Submit Final Assessment"):
                    p_score = sum(
                        1 for i, q in enumerate(st.session_state.post_quiz_data)
                        if is_correct(p_ans[i], q["answer"])
                    )
                    st.session_state.post_score = p_score
                    st.session_state.history_log.append({
                        "date":    datetime.now().strftime("%d %b %Y"),
                        "pre":     st.session_state.pre_score,
                        "post":    p_score,
                        "subject": subj,
                    })
                    st.rerun()

        if st.session_state.post_score > 0:
            st.divider()
            final_pct = st.session_state.post_score / 21 * 100
            imp_val   = st.session_state.post_score - pre
            rl2, bg2  = risk_label(final_pct)

            # Results metrics
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("Pre-Test",    f"{pre}/21")
            c2.metric("Post-Test",   f"{post}/21")
            c3.metric("Improvement", f"{imp_val:+} marks")
            c4.metric("Final %",     f"{final_pct:.1f}%")

            # Verdict
            if final_pct >= 60:
                st.success("✅ PASS — Well done! Your preparation paid off.")
            elif final_pct >= 40:
                st.warning("⚠️ BORDERLINE — Close! A bit more practice needed.")
            else:
                st.error("❌ FAIL — Don't give up. Revisit the 30-day plan.")

            st.markdown(f"**Risk Level:** <span class='{bg2}'>{rl2}</span>",
                        unsafe_allow_html=True)

            st.divider()

            # AI feedback (cached)
            st.subheader("🤖 AI Personalised Feedback")
            cache_key = f"feedback_{pre}_{post}"
            if st.session_state.get("feedback_cache_key") != cache_key:
                with st.spinner("Generating personalised feedback …"):
                    fb = ai_feedback(name, subj, pre, post, final_pct)
                st.session_state.ai_feedback_text   = fb
                st.session_state.feedback_cache_key = cache_key
            st.info(st.session_state.get("ai_feedback_text", ""))

            st.divider()

            # PDF Report
            st.subheader("📄 Download Full Report")
            pdf_cache_key = f"pdf_{pre}_{post}_{name}"
            if st.session_state.get("pdf_cache_key") != pdf_cache_key:
                st.session_state.pdf_bytes     = generate_pdf_report().read()
                st.session_state.pdf_cache_key = pdf_cache_key
            st.download_button(
                label="⬇️ Download PDF Report",
                data=st.session_state.pdf_bytes,
                file_name=f"{name.replace(' ','_')}_UniversityReport.pdf",
                mime="application/pdf"
            )

    # ════════════════════════════════════════════
    # TAB 7 — FULL CHAT ASSISTANT
    # ════════════════════════════════════════════
    with tabs[6]:
        st.subheader("💬 AI Chat Assistant")
        st.caption(
            f"🎓 Your personal university professor | "
            f"Branch: **{st.session_state.user_branch}** | "
            f"Year: **{st.session_state.user_year}**"
        )

        # ── Quick prompt buttons
        st.markdown("**⚡ Quick Questions:**")
        qcol1, qcol2, qcol3, qcol4 = st.columns(4)
        quick_prompts = [
            ("📖 Weak Subject",  f"Explain the key concepts of {st.session_state.weakest_subject or 'my weakest subject'} in simple terms for a {st.session_state.user_year} {st.session_state.user_branch} student."),
            ("📝 Exam Tips",     f"Give me 5 effective exam preparation tips for a {st.session_state.user_branch} {st.session_state.user_year} university student."),
            ("🧮 Formulas",      f"List the most important formulas and equations I must know for {st.session_state.weakest_subject or 'engineering'} exam."),
            ("🗓️ 30-Day Plan",  f"Create a brief 30-day study strategy for a {st.session_state.user_branch} student to improve in {st.session_state.weakest_subject or 'their weak subject'}."),
        ]
        for qi, (col, (label, prompt)) in enumerate(zip([qcol1, qcol2, qcol3, qcol4], quick_prompts)):
            if col.button(label, key=f"qprompt_{qi}"):
                st.session_state["pending_chat_msg"] = prompt
                st.rerun()

        st.divider()

        # ── Chat display area
        if not st.session_state.chat_history:
            st.info("👋 Hi! I'm your AI Academic Mentor. Ask me anything about your subjects, exam tips, concepts, or study strategies!")
        else:
            for chat in st.session_state.chat_history:
                # User bubble
                st.markdown(
                    f"<div class='chat-user'>🧑‍💻 <b>You:</b> {chat.get('user','')}</div>",
                    unsafe_allow_html=True
                )
                # AI bubble - use st.markdown for proper rendering of code/math
                with st.container():
                    st.markdown(
                        "<div class='chat-ai'>🤖 <b>MENTORA AI:</b></div>",
                        unsafe_allow_html=True
                    )
                    st.markdown(chat.get("ai", ""))

        st.divider()

        # ── Input area
        chat_col1, chat_col2 = st.columns([5, 1])
        pending = st.session_state.get("pending_chat_msg", "")
        # Use a counter-based key so the box clears after each send
        chat_input_key = f"full_chat_input_{len(st.session_state.chat_history)}"
        new_msg = chat_col1.text_input(
            "Type your question:",
            value=pending,
            key=chat_input_key,
            placeholder="e.g. Explain the difference between TCP and UDP..."
        )
        # Clear pending after rendering
        if pending:
            st.session_state["pending_chat_msg"] = ""

        send_clicked = chat_col2.button("Send 📨", key="full_chat_send")

        if send_clicked and new_msg.strip():
            with st.spinner("AI Professor is thinking …"):
                try:
                    messages = [
                        {
                            "role": "system",
                            "content": (
                                f"You are a highly experienced university professor and academic mentor "
                                f"specialising in {st.session_state.user_branch}. "
                                f"Student profile — Name: {st.session_state.student_name or 'Student'}, "
                                f"Year: {st.session_state.user_year}, "
                                f"Weak Subject: {st.session_state.weakest_subject or 'Not identified'}. "
                                f"Give detailed, accurate, university-level answers. "
                                f"Use examples, formulas, and analogies where helpful. "
                                f"Format your response clearly with bullet points or numbered steps when appropriate."
                            )
                        }
                    ]
                    for chat in st.session_state.chat_history:
                        messages.append({"role": "user",      "content": chat["user"]})
                        messages.append({"role": "assistant",  "content": chat["ai"]})
                    messages.append({"role": "user", "content": new_msg.strip()})

                    res_raw = safe_chat(messages, temperature=0.35, max_tokens=1024)
                    if res_raw is None: raise Exception("AI service unavailable. Check API key.")
                    class _R: pass
                    res = _R()
                    class _C: pass
                    res.choices = [_C()]
                    res.choices[0].message = _C()
                    res.choices[0].message.content = res_raw
                    reply = res.choices[0].message.content.strip()
                    st.session_state.chat_history.append({
                        "user": new_msg.strip(),
                        "ai":   reply
                    })
                    st.rerun()
                except Exception as e:
                    st.error(f"Chat error: {e}")

        # ── Controls row
        ctrl1, ctrl2 = st.columns([1, 1])
        if ctrl1.button("🗑️ Clear Chat History", key="clear_chat_btn"):
            st.session_state.chat_history = []
            st.rerun()
        ctrl2.caption(f"💬 {len(st.session_state.chat_history)} message(s) in history")
    st.divider()
    if st.button("⬅️ Back to Dashboard", key="back_btn"):
        st.session_state.phase = "input"
        # Clear quiz data so fresh questions generate next time
        st.session_state.pre_quiz_sets  = []
        st.session_state.pre_set_scores = []
        st.session_state.pre_set_index  = 0
        st.session_state.quiz_data      = []
        st.session_state.post_quiz_data = []
        st.session_state.current_day_mcqs = []
        st.rerun()
