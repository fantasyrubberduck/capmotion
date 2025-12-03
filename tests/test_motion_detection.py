import cv2
import numpy as np
import pytest

def detect_motion(frame1, frame2, threshold=5000):
    """Funció simplificada per detectar moviment entre dos frames."""
    gray1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
    gray1 = cv2.GaussianBlur(gray1, (21, 21), 0)

    gray2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.GaussianBlur(gray2, (21, 21), 0)

    frame_delta = cv2.absdiff(gray1, gray2)
    thresh = cv2.threshold(frame_delta, 25, 255, cv2.THRESH_BINARY)[1]
    thresh = cv2.dilate(thresh, None, iterations=2)

    contours, _ = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    return any(cv2.contourArea(c) > threshold for c in contours)

def generate_frame(moving=False):
    """Genera un frame sintètic amb o sense moviment."""
    frame = np.zeros((480, 640, 3), dtype=np.uint8)
    if moving:
        cv2.rectangle(frame, (100, 100), (200, 200), (255, 255, 255), -1)
    return frame

def test_no_motion_detected():
    f1 = generate_frame(moving=False)
    f2 = generate_frame(moving=False)
    assert detect_motion(f1, f2) is False

def test_motion_detected():
    f1 = generate_frame(moving=False)
    f2 = generate_frame(moving=True)
    assert detect_motion(f1, f2) is True
