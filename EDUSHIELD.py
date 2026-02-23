import streamlit as st
import random
import statistics
import matplotlib.pyplot as plt
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
import os

st.set_page_config(page_title="AI Academic Performance System", layout="wide")

# -----------------------------
# TITLE
# -----------------------------
st.title("🎓 AI Academic Performance Intelligence System")

# -----------------------------
# STUDENT DETAILS
# -----------------------------
st.sidebar.header("Student Details")

student_name = st.sidebar.text_input("Student Name")
subject = st.sidebar.text_input("Subject Name")
exam_type = st.sidebar.selectbox("Exam Type", ["UT (0-20)", "Semester (0-100)"])

max_marks = 20 if "UT" in exam_type else 100

# -----------------------------
# BEFORE TEST SIMULATION
# -----------------------------
if st.sidebar.button("Run Analysis"):

    st.subheader("📊 Baseline Assessment")

    before_scores = [random.randint(40,80) for _ in range(3)]
    before_avg = round(statistics.mean(before_scores),2)

    st.write("Before Test Scores:", before_scores)
    st.write("Before Average:", before_avg)

    if before_avg < 60:
        st.error("Weak Subject Detected")
        weak_topic = st.text_input("Enter Weak Topic")
    else:
        weak_topic = None

    # -----------------------------
    # 30 DAY PLAN PREVIEW
    # -----------------------------
    st.subheader("📅 30 Day Personalized Plan Preview")

    for day in range(1,31):
        st.write(f"Day {day}: Study weak topic + Practice MCQs")

    if st.button("Start 30 Day Plan"):

        daily_accuracy = []
        consistency = []

        st.subheader("📈 30 Day Execution")

        for day in range(1,31):
            done = random.choice([0,1])
            consistency.append(done)

            difficulty = "Easy" if day<=10 else "Medium" if day<=20 else "Hard"
            accuracy = random.randint(50,95)
            daily_accuracy.append(accuracy)

        st.success("30 Day Plan Completed")

        # -----------------------------
        # AFTER TEST
        # -----------------------------
        st.subheader("📊 After Plan Assessment")

        after_scores = [random.randint(60,95) for _ in range(3)]
        after_avg = round(statistics.mean(after_scores),2)

        st.write("After Test Scores:", after_scores)
        st.write("After Average:", after_avg)

        # -----------------------------
        # PERFORMANCE RATING
        # -----------------------------
        if after_avg >= 85:
            rating = "A"
            risk = "Low 🟢"
        elif after_avg >= 70:
            rating = "B"
            risk = "Low 🟢"
        elif after_avg >= 50:
            rating = "C"
            risk = "Medium 🟡"
        else:
            rating = "D"
            risk = "High 🔴"

        prediction = "PASS" if after_avg >= 50 else "FAIL"

        st.subheader("🏆 Final Evaluation")
        st.write("Rating:", rating)
        st.write("Risk Level:", risk)
        st.write("Prediction:", prediction)

        # -----------------------------
        # GRAPHS
        # -----------------------------
        st.subheader("📊 Performance Graphs")

        col1, col2 = st.columns(2)

        with col1:
            fig1, ax1 = plt.subplots()
            ax1.bar(["Before","After"], [before_avg, after_avg])
            st.pyplot(fig1)

        with col2:
            fig2, ax2 = plt.subplots()
            ax2.plot(daily_accuracy)
            st.pyplot(fig2)

        # -----------------------------
        # PDF GENERATION
        # -----------------------------
        if st.button("Generate PDF Report"):

            file_name = f"{student_name}_Report.pdf"
            doc = SimpleDocTemplate(file_name)
            elements = []
            styles = getSampleStyleSheet()

            elements.append(Paragraph("AI Academic Performance Report", styles["Heading1"]))
            elements.append(Spacer(1, 0.3*inch))
            elements.append(Paragraph(f"Student: {student_name}", styles["Normal"]))
            elements.append(Paragraph(f"Subject: {subject}", styles["Normal"]))
            elements.append(Paragraph(f"Before Average: {before_avg}%", styles["Normal"]))
            elements.append(Paragraph(f"After Average: {after_avg}%", styles["Normal"]))
            elements.append(Paragraph(f"Rating: {rating}", styles["Normal"]))
            elements.append(Paragraph(f"Prediction: {prediction}", styles["Normal"]))

            doc.build(elements)

            with open(file_name, "rb") as f:
                st.download_button("Download Report", f, file_name=file_name)
