import streamlit as st
import subprocess
import pandas as pd
import os
import time

st.set_page_config(page_title="Face Attendance System", layout="centered")
st.title("📸 Face Attendance Recognition System")

st.markdown("""
Welcome to the Face Attendance System!  
Click the button below to run all preprocessing steps, launch the camera, and track attendance live.
""")

if st.button("Start Attendance"):
    st.success("Running preprocessing and launching camera...")

    # ✅ Run all preprocessing scripts
    subprocess.run("python encode_faces.py", shell=True)
    subprocess.run("python preprocess_custom.py", shell=True)
    subprocess.run("python preprocess_lrw.py", shell=True)

    # ✅ Launch camera script
    subprocess.Popen("python attendance.py", shell=True)

    st.info("Camera launched. Please look into the webcam. Press 'q' to close the camera window.")

    # ✅ Live attendance display
    placeholder = st.empty()
    last_rows = 0

    st.subheader("📋 Attendance Log")

    while True:
        if os.path.exists("attendance.csv"):
            try:
                df = pd.read_csv("attendance.csv")
                if len(df) > last_rows:
                    placeholder.dataframe(df.tail(10), width="stretch")
                    last_rows = len(df)
            except Exception:
                pass  # File might be locked while writing

        time.sleep(2)
