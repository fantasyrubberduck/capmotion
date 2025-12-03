import os
import cv2
import numpy as np
import subprocess
import pytest

OUTPUT_DIR = "output_test"

@pytest.fixture(scope="module", autouse=True)
def setup_output_dir():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    yield
    # Neteja després del test
    for f in os.listdir(OUTPUT_DIR):
        os.remove(os.path.join(OUTPUT_DIR, f))
    os.rmdir(OUTPUT_DIR)

def generate_frame(moving=False):
    """Genera un frame sintètic amb o sense moviment."""
    frame = np.zeros((480, 640, 3), dtype=np.uint8)
    if moving:
        cv2.rectangle(frame, (100, 100), (200, 200), (255, 255, 255), -1)
    return frame

def test_motion_detection_and_recording():
    # Simulem frames sense moviment
    static_frame = generate_frame(moving=False)
    # Simulem frames amb moviment
    moving_frame = generate_frame(moving=True)

    # Obrim procés ffmpeg per gravar
    filename = os.path.join(OUTPUT_DIR, "test_clip.mp4")
    ffmpeg_process = subprocess.Popen([
        "ffmpeg", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24",
        "-s", f"{static_frame.shape[1]}x{static_frame.shape[0]}", "-r", "20",
        "-i", "-", "-c:v", "libx264", "-preset", "fast", filename
    ], stdin=subprocess.PIPE)

    # Escriu uns quants frames amb moviment
    for _ in range(30):
        ffmpeg_process.stdin.write(moving_frame.tobytes())

    ffmpeg_process.stdin.close()
    ffmpeg_process.wait()

    # Comprovem que el fitxer s'ha creat i té contingut
    assert os.path.exists(filename)
    assert os.path.getsize(filename) > 0
