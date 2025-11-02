import streamlit as st
from streamlit_webrtc import webrtc_streamer
import pandas as pd
import os

st.set_page_config(page_title="Face Attendance System", layout="centered")

st.title("🧠 Face Attendance Recognition System")
st.markdown("Welcome! Click below to launch the camera and track attendance live.")

# Start button
if st.button("🚀 Start Attendance"):
    st.info("📷 Launching webcam in browser...")

    webrtc_streamer(key="face-attendance")

    st.markdown("---")
    st.subheader("📋 Attendance Log")

    if os.path.exists("attendance.csv"):
        df = pd.read_csv("attendance.csv")
        st.dataframe(df)
    else:
        st.info("No attendance data found yet.")
