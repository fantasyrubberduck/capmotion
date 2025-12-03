import cv2
import datetime
import subprocess
import os

camera_source = os.getenv("CAMERA_SOURCE", 0)
cap = cv2.VideoCapture(camera_source)

recording = False
ffmpeg_process = None

while True:
    ret, frame = cap.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (21, 21), 0)

    if 'first_frame' not in locals():
        first_frame = gray
        continue

    frame_delta = cv2.absdiff(first_frame, gray)
    thresh = cv2.threshold(frame_delta, 25, 255, cv2.THRESH_BINARY)[1]
    thresh = cv2.dilate(thresh, None, iterations=2)

    contours, _ = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    motion_detected = any(cv2.contourArea(c) > 5000 for c in contours)

    if motion_detected and not recording:
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"output/clip_{timestamp}.mp4"
        os.makedirs("output", exist_ok=True)

        ffmpeg_process = subprocess.Popen([
            "ffmpeg", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24",
            "-s", f"{frame.shape[1]}x{frame.shape[0]}", "-r", "20",
            "-i", "-", "-c:v", "libx264", "-preset", "fast", filename
        ], stdin=subprocess.PIPE)
        recording = True
        print(f"[INFO] Moviment detectat → inici gravació: {filename}")

    if recording:
        ffmpeg_process.stdin.write(frame.tobytes())
        if not motion_detected:
            ffmpeg_process.stdin.close()
            ffmpeg_process.wait()
            recording = False
            print("[INFO] Fi de gravació")

cap.release()
if ffmpeg_process:
    ffmpeg_process.stdin.close()
    ffmpeg_process.wait()
print("[INFO] Captura finalitzada")
