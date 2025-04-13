# surveillance.py

import cv2
import time
import os
from datetime import datetime
import threading
from playsound import playsound
import yagmail
from ultralytics import YOLO

SAVE_DIR = "intrusions"
LOG_FILE = "log.txt"
VIDEO_DIR = "intrusion_videos"
os.makedirs(SAVE_DIR, exist_ok=True)
os.makedirs(VIDEO_DIR, exist_ok=True)

yag = yagmail.SMTP("technicalseminargc12@gmail.com", "abuw nypn fsnw irwy")

# Load YOLOv8 pretrained model
yolo_model = YOLO("yolov8n.pt")  

def send_email_alert(image_path, recipient):
    yag.send(
        to=recipient,
        subject="Intrusion Detected!",
        contents="An intrusion was detected. Screenshot attached.",
        attachments=image_path
    )

def log_event(message):
    with open(LOG_FILE, "a") as f:
        f.write(f"{datetime.now()} - {message}\n")

def detect_intrusion(sensitivity=500, recipient="technicalseminargc12@gmail.com"):
    cap = cv2.VideoCapture(0)
    prev_frame = None
    last_alert_time = 0
    cooldown_seconds = 10
    video_writer = None
    recording = False

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.equalizeHist(gray)
        gray = cv2.GaussianBlur(gray, (5, 5), 0)

        motion_detected = False
        yolo_detected = False

        if prev_frame is not None:
            diff = cv2.absdiff(gray, prev_frame)
            _, thresh = cv2.threshold(diff, 30, 255, cv2.THRESH_BINARY)
            contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            for cnt in contours:
                if cv2.contourArea(cnt) > sensitivity:
                    motion_detected = True

        # YOLO person detection
        results = yolo_model(frame, verbose=False)[0]
        for det in results.boxes.data.tolist():
            x1, y1, x2, y2, score, cls = det
            if int(cls) == 0 and score > 0.5:  # class 0 is 'person'
                yolo_detected = True
                cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
                cv2.putText(frame, f"Person: {score:.2f}", (int(x1), int(y1)-10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

        if yolo_detected and motion_detected:
            cv2.putText(frame, "Intrusion Detected!", (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

            current_time = time.time()
            if current_time - last_alert_time > cooldown_seconds:
                # Save screenshot
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                img_path = os.path.join(SAVE_DIR, f"intrusion_{timestamp}.jpg")
                cv2.imwrite(img_path, frame)

                # Log and alert
                log_event(f"Intrusion detected - {img_path}")
                threading.Thread(target=playsound, args=("alert.mp3",), daemon=True).start()
                threading.Thread(target=send_email_alert, args=(img_path, recipient), daemon=True).start()

                # Start recording
                video_path = os.path.join(VIDEO_DIR, f"intrusion_{timestamp}.mp4")
                video_writer = cv2.VideoWriter(video_path, cv2.VideoWriter_fourcc(*'XVID'), 20,
                                               (frame.shape[1], frame.shape[0]))
                recording = True
                start_time = current_time

                last_alert_time = current_time

        if recording:
            video_writer.write(frame)
            if time.time() - start_time > 10:  # Stop recording after 10 seconds
                video_writer.release()
                recording = False

        prev_frame = gray
        yield frame

    cap.release()
    if video_writer and video_writer.isOpened():
        video_writer.release()
