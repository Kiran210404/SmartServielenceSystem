import cv2
import time
import os
from datetime import datetime
from playsound import playsound
import yagmail

SAVE_DIR = "intrusions"
os.makedirs(SAVE_DIR, exist_ok=True)

yag = yagmail.SMTP("technicalseminargc12@gmail.com", "abuw nypn fsnw irwy")

def send_email_alert(image_path):
    yag.send(
        to="technicalseminargc12@gmail.com",
        subject="Intrusion Detected!",
        contents="An intrusion was detected. Screenshot attached.",
        attachments=image_path
    )

def detect_intrusion():
    cap = cv2.VideoCapture(0)
    prev_frame = None

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.equalizeHist(gray)

        if prev_frame is not None:
            diff = cv2.absdiff(gray, prev_frame)
            _, thresh = cv2.threshold(diff, 30, 255, cv2.THRESH_BINARY)
            contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            for cnt in contours:
                if cv2.contourArea(cnt) > 500:
                    x, y, w, h = cv2.boundingRect(cnt)
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
                    cv2.putText(frame, "Intrusion Detected!", (10, 30),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

                    # Save screenshot
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    img_path = os.path.join(SAVE_DIR, f"intrusion_{timestamp}.jpg")
                    cv2.imwrite(img_path, frame)

                    # Sound alert
                    playsound("alert.mp3")

                    # Send email
                    send_email_alert(img_path)

        prev_frame = gray
        yield frame  # yield each frame for streamlit to show

    cap.release()
