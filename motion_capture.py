import cv2
import datetime
import subprocess
import os
from collections import deque
import time
import logging

# Variables d’entorn configurables
camera_source = os.getenv("CAMERA_SOURCE", 0)
PRE_BUFFER_FRAMES = int(os.getenv("BUFFER_SIZE", 30))   # frames previs
STOP_DELAY = int(os.getenv("STOP_DELAY", 3))            # segons sense moviment abans d’aturar
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()      # nivell de logging (INFO per defecte)

# Configuració del logger amb nivell des de variable d’entorn
logging.basicConfig(
    level=getattr(logging, LOG_LEVEL, logging.INFO),
    format="%(asctime)s [%(levelname)s] %(message)s",
)

cap = cv2.VideoCapture(camera_source)

recording = False
ffmpeg_process = None
last_motion_time = None

frame_buffer = deque(maxlen=PRE_BUFFER_FRAMES)

while True:
    ret, frame = cap.read()
    if not ret:
        logging.error("No s'ha pogut llegir frame de la càmera.")
        break

    frame_buffer.append(frame)

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (21, 21), 0)

    if 'first_frame' not in locals():
        first_frame = gray
        continue

    frame_delta = cv2.absdiff(first_frame, gray)
    thresh = cv2.threshold(frame_delta, 25, 255, cv2.THRESH_BINARY)[1]
    thresh = cv2.dilate(thresh, None, iterations=2)

    contours, _ = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # DEBUG: mostrar àrea de cada contorn si LOG_LEVEL=DEBUG
    for c in contours:
        area = cv2.contourArea(c)
        logging.debug(f"Contorn detectat amb àrea: {area}")

    motion_detected = any(cv2.contourArea(c) > 5000 for c in contours)

    if motion_detected:
        last_motion_time = time.time()
        if not recording:
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"output/clip_{timestamp}.mp4"
            os.makedirs("output", exist_ok=True)

            ffmpeg_process = subprocess.Popen([
                "ffmpeg", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24",
                "-s", f"{frame.shape[1]}x{frame.shape[0]}", "-r", "20",
                "-i", "-", "-c:v", "libx264", "-preset", "fast", filename
            ], stdin=subprocess.PIPE)
            recording = True
            logging.info(f"Moviment detectat → inici gravació: {filename}")

            # Escriure frames del buffer per començar abans del moviment
            for buffered_frame in frame_buffer:
                ffmpeg_process.stdin.write(buffered_frame.tobytes())

    if recording:
        ffmpeg_process.stdin.write(frame.tobytes())

        # Si fa STOP_DELAY segons que no hi ha moviment → aturar
        if last_motion_time and (time.time() - last_motion_time > STOP_DELAY):
            ffmpeg_process.stdin.close()
            ffmpeg_process.wait()
            recording = False
            logging.info("Fi de gravació (sense moviment)")

cap.release()
if ffmpeg_process:
    ffmpeg_process.stdin.close()
    ffmpeg_process.wait()
logging.info("Captura finalitzada")
