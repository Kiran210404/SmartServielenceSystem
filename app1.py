# app.py

import cv2
import streamlit as st
from surviellance import detect_intrusion

st.set_page_config(layout="wide")
st.title("🔒 Smart Surveillance System")

with st.sidebar:
    st.header("🛠️ Settings")
    sensitivity = st.slider("Motion Sensitivity", min_value=100, max_value=2000, value=500, step=100)
    recipient_email = st.text_input("Alert Email", value="technicalseminargc12@gmail.com")
    show_logs = st.checkbox("Show Alert Log")

run_button = st.button("▶️ Start Monitoring")

if run_button:
    stframe = st.empty()
    st.success("Monitoring Started")
    for frame in detect_intrusion(sensitivity=sensitivity, recipient=recipient_email):
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        stframe.image(frame, channels="RGB")

if show_logs:
    st.subheader("📜 Event Log")
    try:
        with open("log.txt", "r") as log_file:
            logs = log_file.read()
            st.text_area("Logs", logs, height=300)
    except FileNotFoundError:
        st.warning("No logs found yet.")
