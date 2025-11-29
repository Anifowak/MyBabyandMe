import streamlit as st
import pandas as pd
from datetime import date
import matplotlib.pyplot as plt
import os

st.title("MyBaby&I")

st.write("""
Track your pregnancy, monitor your health metrics, and get easy-to-understand guidance. 
You can also download your data to share with your doctor.
""")

# --------------------------
# 1. User Input Form
# --------------------------
with st.form("maternal_form"):
    st.subheader("Enter Your Information")
    name = st.text_input("Your Name")
    lmp = st.date_input("Last Menstrual Period (LMP)")
    weight_kg = st.number_input("Current Weight (kg)", min_value=30.0, max_value=200.0)
    height_cm = st.number_input("Height (cm)", min_value=100.0, max_value=250.0)
    systolic_bp = st.number_input("Systolic BP (mmHg)", min_value=80, max_value=200)
    diastolic_bp = st.number_input("Diastolic BP (mmHg)", min_value=50, max_value=150)
    submitted = st.form_submit_button("Track My Pregnancy")

if submitted:
    today = date.today()
    gestation_days = (today - lmp).days
    if gestation_days < 0:
        st.error("Check LMP: Date is in the future.")
    else:
        gestation_weeks = gestation_days // 7
        gestation_remainder_days = gestation_days % 7

        # Determine trimester
        if gestation_weeks < 13:
            trimester = "First Trimester"
        elif gestation_weeks < 27:
            trimester = "Second Trimester"
        else:
            trimester = "Third Trimester"

        # BMI Calculation
        bmi = round(weight_kg / (height_cm/100)**2, 1)

        # --------------------------
        # 2. Interpret Results in Simple Terms
        # --------------------------
        def bmi_status(bmi_value):
            if bmi_value < 18.5:
                return "Underweight – try to maintain a healthy diet."
            elif 18.5 <= bmi_value < 25:
                return "Normal weight – good job maintaining a healthy BMI."
            elif 25 <= bmi_value < 30:
                return "Overweight – monitor diet and activity."
            else:
                return "Obese – consult your doctor for advice."

        def bp_status(sys, dia):
            if sys < 120 and dia < 80:
                return "Blood pressure is normal."
            elif 120 <= sys < 140 or 80 <= dia < 90:
                return "Elevated blood pressure – keep monitoring."
            else:
                return "High blood pressure – contact your doctor."

        st.subheader(f"Hello {name}, your pregnancy dashboard")
        st.write(f"Gestational Age: {gestation_weeks} weeks + {gestation_remainder_days} days")
        st.write(f"Trimester: {trimester}")

        # --------------------------
        # 3. Display Health Metrics with Explanation
        # --------------------------
        st.write(f"Weight: {weight_kg} kg, Height: {height_cm} cm")
        st.write(f"BMI: {bmi} → {bmi_status(bmi)}")
        st.write(f"Systolic BP: {systolic_bp}, Diastolic BP: {diastolic_bp} → {bp_status(systolic_bp, diastolic_bp)}")

        # --------------------------
        # 4. Visualization
        # --------------------------
        st.subheader("Your Health Metrics")
        fig, ax = plt.subplots()
        ax.bar(["BMI", "Systolic BP", "Diastolic BP"], [bmi, systolic_bp, diastolic_bp],
               color=["skyblue","salmon","lightgreen"])
        ax.set_ylim(0, max(220, systolic_bp+20))
        ax.set_ylabel("Value")
        ax.set_title("Maternal Health Metrics")
        st.pyplot(fig)

        # --------------------------
        # 5. Trimester Guidance
        # --------------------------
        st.subheader("Tips for Your Trimester")
        if trimester == "First Trimester":
            st.info("Take prenatal vitamins (folic acid), eat balanced meals, and schedule early checkups.")
        elif trimester == "Second Trimester":
            st.info("Monitor weight gain, stay active with safe exercises, and attend mid-pregnancy scans.")
        else:
            st.info("Prepare for delivery, track fetal movements, and maintain healthy nutrition.")

        # --------------------------
        # 6. Save Data Locally
        # --------------------------
        patient_data = {
            "Name": name,
            "LMP": lmp,
            "Date": today,
            "Gestation Weeks": gestation_weeks,
            "Trimester": trimester,
            "Weight_kg": weight_kg,
            "Height_cm": height_cm,
            "BMI": bmi,
            "Systolic_BP": systolic_bp,
            "Diastolic_BP": diastolic_bp
        }

        df = pd.DataFrame([patient_data])
        file_path = "maternal_health_home.csv"
        if not os.path.exists(file_path):
            df.to_csv(file_path, index=False)
        else:
            df.to_csv(file_path, mode='a', header=False, index=False)

        st.success("Your data has been saved for tracking at home!")

        # --------------------------
        # 7. Download CSV for Hospital
        # --------------------------
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Download My Data for Doctor",
            data=csv,
            file_name=f"{name.replace(' ','_')}_maternal_data.csv",
            mime="text/csv"
        )

        st.info("Take this file to your doctor to speed up your hospital visits and care.")
