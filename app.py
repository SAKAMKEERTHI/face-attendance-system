import streamlit as st

st.set_page_config(page_title="Face Attendance System", layout="centered")

st.title("🧠 Face Attendance Recognition System")
st.markdown("Welcome! Click below to launch the camera and track attendance live.")

try:
    # Try to import and launch webcam
    from streamlit_webrtc import webrtc_streamer

    st.info("📷 Launching webcam in browser...")
    webrtc_streamer(key="face-attendance")
    st.success("✅ Webcam should now be visible below. If prompted, allow camera access.")

except ModuleNotFoundError:
    st.error("❌ streamlit-webrtc is not installed. Please add it to requirements.txt and push to GitHub.")

except Exception as e:
    st.error(f"❌ App crashed with error: {e}")
    st.markdown("Please check your code or share the error message here so I can help fix it.")
