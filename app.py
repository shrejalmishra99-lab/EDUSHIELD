import streamlit as st
from groq import Groq
import pandas as pd
import json
import re
import numpy as np

# ---------- 1. CORE SETUP ----------
st.set_page_config(page_title="AI Academic Mentor", layout="wide")

if "GROQ_API_KEY" not in st.secrets:
    st.error("Please add GROQ_API_KEY to your Streamlit Secrets.")
    st.stop()

client = Groq(api_key=st.secrets["GROQ_API_KEY"])
MODEL = "llama-3.3-70b-versatile"

# ---------- 2. SESSION STATE ----------
defaults = {
    "phase": "input",
    "subjects_data": {},
    "quiz_data": [],
    "post_quiz_data": [],
    "pre_score": 0,
    "post_score": 0,
    "weakest_subject": "",
    "daily_plan_objectives": [],
    "daily_scores": {},
    "user_class": "10",
    "student_name": "",
    "roll_no": "",
    "attendance": 75,
    "chat_history": []
}

for key, val in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = val

# ---------- 3. AI LOGIC FUNCTIONS ----------

def get_clean_quiz(subject, type_label="diagnostic"):
    prompt = f"Generate 10 technical MCQs for CBSE Class {st.session_state.user_class} {subject} for a {type_label} test. Return ONLY a JSON list: [{{'question': '...', 'options': ['A','B','C','D'], 'answer': 'exact string matching one of the options' }}]"
    try:
        response = client.chat.completions.create(
            model=MODEL, messages=[{"role": "user", "content": prompt}],
            temperature=0.5, response_format={"type": "json_object"}
        )
        data = json.loads(response.choices[0].message.content)
        if isinstance(data, dict):
            for key in data:
                if isinstance(data[key], list): return data[key]
        return data
    except Exception as e:
        st.error(f"Quiz failed: {e}"); return []

def generate_30_day_objectives(subject):
    prompt = f"List exactly 30 unique sub-topics from the CBSE Class {st.session_state.user_class} {subject} syllabus. Format: Topic name only, one per line."
    try:
        response = client.chat.completions.create(model=MODEL, messages=[{"role": "user", "content": prompt}], temperature=0.4)
        lines = response.choices[0].message.content.strip().split('\n')
        topics = [re.sub(r'^(Day\s\d+:|\d+\.|\d+\))', '', line).strip() for line in lines if len(line) > 3]
        while len(topics) < 30: topics.append(f"Advanced revision of {subject}")
        return topics[:30]
    except:
        return [f"{subject} Concept {i+1}" for i in range(30)]

def generate_targeted_mcqs(subject, topic):
    prompt = f"Generate 5 technical MCQs for Class {st.session_state.user_class} {subject} on: {topic}. Return ONLY JSON list."
    try:
        response = client.chat.completions.create(model=MODEL, messages=[{"role": "user", "content": prompt}], temperature=0.4, response_format={"type": "json_object"})
        data = json.loads(response.choices[0].message.content)
        if isinstance(data, dict):
            for key in data:
                if isinstance(data[key], list): return data[key]
        return data
    except: return []

def compute_risk_curve():
    pre_score = st.session_state.pre_score / 10.0
    risk_list = []
    for day in range(1, 31):
        improvement = (day / 30.0) * 0.4
        daily_perf = st.session_state.daily_scores.get(day, 0) / 5.0 if day in st.session_state.daily_scores else 0
        expected_mastery = min(pre_score + improvement + (daily_perf * 0.1), 1.0)
        risk_list.append(max(0, round((1.0 - expected_mastery) * 100, 1)))
    return risk_list

# ---------- 4. UI SECTIONS ----------

with st.sidebar:
    st.title("👤 Student Profile")
    st.session_state.student_name = st.text_input("Student Name", st.session_state.student_name)
    st.session_state.roll_no = st.text_input("Roll Number", st.session_state.roll_no)
    st.session_state.user_class = st.selectbox("Class", ["9", "10", "11", "12"], index=1)
    st.session_state.attendance = st.slider("Attendance %", 0, 100, st.session_state.attendance)
    
    if st.button("🔄 Reset Application"):
        st.session_state.clear()
        st.rerun()
    
    st.divider()
    st.subheader("💬 Chatbot")
    user_msg = st.text_input("Ask AI:", key="chat_input")
    if st.button("Send") and user_msg:
        try:
            res = client.chat.completions.create(model=MODEL, messages=[{"role": "user", "content": user_msg}], temperature=0.3)
            st.session_state.chat_history.append({"user": user_msg, "ai": res.choices[0].message.content.strip()})
            st.rerun()
        except: st.error("Chat error")
    
    for chat in reversed(st.session_state.chat_history[-3:]):
        st.caption(f"**You:** {chat['user']}")
        st.caption(f"**AI:** {chat['ai']}")

# --- MAIN LOGIC ---

if st.session_state.phase == "input":
    st.title("📊 Academic Analysis Dashboard")
    
    # Subject Entry
    with st.expander("📝 Step 1: Add Subjects", expanded=not bool(st.session_state.subjects_data)):
        sub_raw = st.text_area("Enter subjects separated by commas (e.g., Physics, Maths, Chemistry):")
        if st.button("Add All Subjects"):
            new_list = [s.strip() for s in sub_raw.split(",") if s.strip()]
            for s in new_list:
                if s not in st.session_state.subjects_data:
                    st.session_state.subjects_data[s] = {"UT1": 0, "UT2": 0}
            st.rerun()

    if st.session_state.subjects_data:
        st.divider()
        # DYNAMIC VISUALIZATION LAYOUT
        col_input, col_viz = st.columns([1, 1])
        
        with col_input:
            st.subheader("Step 2: Marks Entry")
            for sub in list(st.session_state.subjects_data.keys()):
                with st.container():
                    c1, c2, c3 = st.columns([2, 1, 1])
                    c1.markdown(f"**{sub}**")
                    # UT1 Input
                    st.session_state.subjects_data[sub]["UT1"] = c2.number_input(
                        "UT1 (0-20)", 0, 20, st.session_state.subjects_data[sub].get("UT1", 0), key=f"ut1_{sub}"
                    )
                    # UT2 Input (Replaced Semester)
                    st.session_state.subjects_data[sub]["UT2"] = c3.number_input(
                        "UT2 (0-20)", 0, 20, st.session_state.subjects_data[sub].get("UT2", 0), key=f"ut2_{sub}"
                    )
            
            st.write("---")
            if st.button("🚀 Analyze Weakness & Start Plan"):
                # Weighting: UT1 and UT2 are equally treated for weakness analysis
                avgs = {s: (v["UT1"] + v["UT2"])/2 for s, v in st.session_state.subjects_data.items()}
                st.session_state.weakest_subject = min(avgs, key=avgs.get)
                st.session_state.phase = "quiz"
                st.rerun()

        with col_viz:
            st.subheader("Live Performance Preview")
            chart_list = []
            for s, v in st.session_state.subjects_data.items():
                chart_list.append({"Subject": s, "Exam": "UT1", "Score": v["UT1"]})
                chart_list.append({"Subject": s, "Exam": "UT2", "Score": v["UT2"]})
            
            df = pd.DataFrame(chart_list)
            if not df.empty:
                st.bar_chart(df, x="Subject", y="Score", color="Exam", stack=False)
                st.caption("Marks out of 20. Chart updates instantly as you type.")

    else:
        st.info("Start by adding subjects above.")

elif st.session_state.phase == "quiz":
    st.title(f"📝 Diagnostic: {st.session_state.weakest_subject}")
    if not st.session_state.quiz_data:
        with st.spinner("AI generating diagnostic test..."):
            st.session_state.quiz_data = get_clean_quiz(st.session_state.weakest_subject)
            st.rerun()

    with st.form("quiz_form"):
        user_answers = []
        for i, q in enumerate(st.session_state.quiz_data):
            st.write(f"**Q{i+1}:** {q['question']}")
            user_answers.append(st.radio("Options:", q['options'], key=f"q_{i}"))
        
        if st.form_submit_button("Submit Test"):
            score = sum(1 for i, q in enumerate(st.session_state.quiz_data) if str(user_answers[i]).strip().lower() == str(q['answer']).strip().lower())
            st.session_state.pre_score = score
            st.session_state.phase = "results"
            st.rerun()

elif st.session_state.phase == "results":
    st.title(f"🏆 Strategy Roadmap: {st.session_state.student_name or 'Student'}")
    
    if not st.session_state.daily_plan_objectives:
        if st.button("📅 Generate 30-Day Syllabus Plan"):
            with st.spinner("Fetching curriculum topics..."):
                st.session_state.daily_plan_objectives = generate_30_day_objectives(st.session_state.weakest_subject)
                st.rerun()
    else:
        st.subheader("🗓️ 30-Day Study Roadmap")
        day_idx = st.slider("Select Plan Day", 1, 30)
        topic = st.session_state.daily_plan_objectives[day_idx-1]
        st.info(f"**Day {day_idx} Focus:** {topic}")
        
        if st.button(f"Generate Practice for {topic}"):
            st.session_state.current_day_mcqs = generate_targeted_mcqs(st.session_state.weakest_subject, topic)
        
        if "current_day_mcqs" in st.session_state and st.session_state.current_day_mcqs:
            with st.form(f"day_{day_idx}_quiz"):
                d_answers = []
                for i, q in enumerate(st.session_state.current_day_mcqs):
                    st.write(f"**Q{i+1}:** {q['question']}")
                    d_answers.append(st.radio("Select:", q['options'], key=f"dq_{i}"))
                if st.form_submit_button("Save Progress"):
                    d_score = sum(1 for i, q in enumerate(st.session_state.current_day_mcqs) if str(d_answers[i]).strip().lower() == str(q['answer']).strip().lower())
                    st.session_state.daily_scores[day_idx] = d_score
                    st.success(f"Score Saved: {d_score}/5")

    st.divider()
    st.subheader("📉 Risk Reduction Forecast")
    st.line_chart(pd.DataFrame({"Risk %": compute_risk_curve()}))

    st.divider()
    st.subheader("🏁 Final Post-Study Assessment")
    if st.button("📝 Start Post-Test"):
        with st.spinner("Generating Final Test..."):
            st.session_state.post_quiz_data = get_clean_quiz(st.session_state.weakest_subject, "final")
            st.rerun()

    if st.session_state.post_quiz_data:
        with st.form("post_quiz_form"):
            post_answers = []
            for i, q in enumerate(st.session_state.post_quiz_data):
                st.write(f"**Q{i+1}:** {q['question']}")
                post_answers.append(st.radio("Options:", q['options'], key=f"post_q_{i}"))
            
            if st.form_submit_button("Submit Final Assessment"):
                p_score = sum(1 for i, q in enumerate(st.session_state.post_quiz_data) if str(post_answers[i]).strip().lower() == str(q['answer']).strip().lower())
                st.session_state.post_score = p_score
                st.rerun()

    if st.session_state.post_score > 0:
        st.subheader("📊 Performance Comparison")
        c1, c2, c3 = st.columns(3)
        c1.metric("Pre-Study Score", f"{st.session_state.pre_score}/10")
        c2.metric("Post-Study Score", f"{st.session_state.post_score}/10")
        improvement = st.session_state.post_score - st.session_state.pre_score
        c3.metric("Improvement", f"{improvement:+}", delta=improvement)

    if st.button("⬅ Back to Dashboard"):
        st.session_state.phase = "input"
        st.rerun()