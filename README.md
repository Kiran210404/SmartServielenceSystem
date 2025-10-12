# 🛡️ SmartsurveillanceSystem

Welcome to **SmartsurveillanceSystem** – an intelligent, AI-powered surveillance solution designed to make monitoring smarter, faster, and more proactive!! 
Empower your security setup with real-time insights, automated alerts, and an intuitive dashboard.

---

## ✨ Features

- 🎥 **Real-Time Video Surveillance:** Monitor live camera feeds with instant access.
- 🤖 **AI Object & Intruder Detection:** Automatically spot people, objects, or suspicious activity using YOLOv8 detection.
- 🔔 **Automated Alerts:** Get notified via email when anomalies are detected.
- 📼 **Recording & Playback:** Securely record and review surveillance footage anytime.
- 🖥️ **Dashboard Interface:** Manage cameras, view alerts, and access logs from a clean dashboard (via Streamlit).
- 🗺️ **Customizable Sensitivity:** Set motion sensitivity as per your requirements.
- 📜 **Event Log:** View saved logs of detected events.
- 🎵 **Sound Alerts:** Instant sound notifications on intrusion.
---

## 🛠️ Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Kiran210404/SmartServielenceSystem.git
   cd SmartServielenceSystem
   ```

2. **Install dependencies**
   > _Make sure you have Python 3.8+ installed._

   ```bash
   pip install opencv-python streamlit playsound yagmail ultralytics
   ```

3. **Run the application**
   ```bash
   streamlit run app.py
   ```
   or
   ```bash
   streamlit run app1.py
   ```
---

## 🚦 Usage

- Open the dashboard at `http://localhost:8501` (Streamlit default port).
- Set your motion sensitivity and alert email in the sidebar.
- Click “Start Monitoring” to begin live surveillance.
- Intrusion events trigger sound alerts, email notifications, and are logged with screenshots and video clips.
- View the event log for a history of detected intrusions.


## 🧰 Tech Stack

- **Languages:** Python
- **Libraries:** OpenCV, Streamlit, Playsound, Yagmail, Ultralytics (YOLOv8)
- **AI Model:** YOLOv8 (for object detection)
- **Dashboard:** Streamlit
- **Email Alerts:** Yagmail

---
