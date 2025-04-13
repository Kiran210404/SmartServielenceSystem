import streamlit as st
from surveillance import detect_intrusion
import cv2

st.set_page_config(layout="wide")
st.title("🔒 Smart Surveillance System")

run_button = st.button("Start Monitoring")

if run_button:
    stframe = st.empty()
    for frame in detect_intrusion():
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        stframe.image(frame, channels="RGB")
