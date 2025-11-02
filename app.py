import streamlit as st

st.set_page_config(page_title="Face Attendance System", layout="centered")

st.title("🧠 Face Attendance Recognition System")
st.markdown("Welcome! Click below to launch the camera and track attendance live.")

# Error-safe webcam launcher
try:
    from streamlit_webrtc import webrtc_streamer

    st.info("📷 Launching webcam in browser...")

    webrtc_streamer(key="face-attendance")

    st.success("✅ Webcam should now be visible below. If prompted, allow camera access.")

except Exception as e:
    st.error(f"❌ App crashed with error: {e}")
    st.markdown("Please check if `streamlit-webrtc` is listed in `requirements.txt` and pushed to GitHub.")
