import os
import sys
import time
import cv2

# ensure working directory is this file’s folder
os.chdir(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.abspath(os.path.join(os.getcwd(), '..')))

from camera import open_camera, capture_frame
from ocr import extract_text
from speech import speak_text

CAPTURE_FILE = "capture_trigger.txt"
STOP_FILE = "stop_ocr.txt"

# open camera once
cap = open_camera()
if not cap:
    speak_text("Unable to access the camera. Exiting.", "en")
    sys.exit(1)

speak_text("Book Reader Started. Say 'capture' to take a picture and read text", "en")

while True:
    # shutdown signal
    if os.path.exists(STOP_FILE):
        speak_text("Text reader stopped.", "en")
        os.remove(STOP_FILE)
        break

    # capture command
    if os.path.exists(CAPTURE_FILE):
        os.remove(CAPTURE_FILE)

        print("Capturing frame...")
        frame = capture_frame(cap)
        text = extract_text(frame)

        if text:
            print("Detected text:", text)
            speak_text(text, "en")
        else:
            print("No text detected.")
            speak_text("No text detected. Please adjust the camera.", "en")

    time.sleep(0.2)

# cleanup
cap.release()
cv2.destroyAllWindows()
