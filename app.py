import streamlit as st
import subprocess
import pandas as pd
import os
import time

st.set_page_config(page_title="Face Attendance System", layout="centered")
st.title("📸 Face Attendance Recognition System")

st.markdown("""
Welcome to the Face Attendance System!  
Click the button below to launch the camera and automatically mark students as present.
""")

# ✅ Load student names (from dataset folder or fixed list)
student_names = [os.path.splitext(f)[0] for f in os.listdir("dataset")
                 if f.lower().endswith((".jpg", ".jpeg", ".png"))]

# ✅ Initialize attendance status
attendance_status = {name: "❌ Absent" for name in student_names}

# ✅ Display initial table
status_placeholder = st.empty()
status_df = pd.DataFrame({
    "Student Name": list(attendance_status.keys()),
    "Status": list(attendance_status.values())
})
status_placeholder.table(status_df)

# ✅ Start Attendance Button
if st.button("Start Attendance"):
    st.success("Launching camera and tracking attendance...")

    # Optional: Run preprocessing if needed
    subprocess.run("python preprocess_custom.py", shell=True)

    # ✅ Launch camera script
    subprocess.Popen("python attendance.py", shell=True)

    st.info("Camera launched. Please look into the webcam. Press 'q' to close the camera window.")

    # ✅ Monitor attendance.csv and update UI
    last_marked = set()
    while True:
        if os.path.exists("attendance.csv"):
            try:
                df = pd.read_csv("attendance.csv")
                new_names = set(df["Name"].tolist())

                # Update only if new names are marked
                if new_names != last_marked:
                    for name in new_names:
                        if name in attendance_status:
                            attendance_status[name] = "✅ Present"

                    status_df = pd.DataFrame({
                        "Student Name": list(attendance_status.keys()),
                        "Status": list(attendance_status.values())
                    })
                    status_placeholder.table(status_df)
                    last_marked = new_names

            except Exception:
                pass  # File might be locked while writing

        time.sleep(2)
