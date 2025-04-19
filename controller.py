import os
import sys
import subprocess
import time
from chatbot.voice_chatbot import listen_command
from point_object_module.scripts.audio_feedback import AudioFeedback


# ─── Constants ────────────────────────────────────────────────────────────────
OCR_DIR           = "easyocr_module"
POINT_DIR         = "point_object_module"
OCR_CAPTURE_FILE  = os.path.join(OCR_DIR,   "capture_trigger.txt")
OCR_STOP_FILE     = os.path.join(OCR_DIR,   "stop_ocr.txt")
POINT_STOP_FILE   = os.path.join(".",       "stop_pointer.txt")

# ─── Globals ─────────────────────────────────────────────────────────────────
running_processes = {}
audio_feedback    = AudioFeedback()

# ─── Process Launchers ────────────────────────────────────────────────────────
def run_easyocr():
    return subprocess.Popen(
        [sys.executable, "easyocr_main.py"],
        cwd=OCR_DIR
    )

def run_point_detector():
    return subprocess.Popen(
        [sys.executable, "point_detection_main.py"],
        cwd=POINT_DIR
    )

# ─── Stop Helpers ─────────────────────────────────────────────────────────────
def stop_easyocr(silent=False):
    if "ocr" not in running_processes:
        if not silent:
            audio_feedback.speak("Text reader is not running.")
        return

    open(OCR_STOP_FILE, "w").write("stop")
    running_processes["ocr"].wait()
    del running_processes["ocr"]
    if os.path.exists(OCR_STOP_FILE):
        os.remove(OCR_STOP_FILE)

def stop_point_detector(silent=False):
    if "point" not in running_processes:
        if not silent:
            audio_feedback.speak("Object detection is not running.")
        return

    open(POINT_STOP_FILE, "w").write("stop")
    running_processes["point"].wait()
    del running_processes["point"]
    if os.path.exists(POINT_STOP_FILE):
        os.remove(POINT_STOP_FILE)

def stop_all(silent=False):
    stop_easyocr(silent)
    stop_point_detector(silent)
    if not silent:
        audio_feedback.speak("All modules stopped.")

# ─── Main Loop ────────────────────────────────────────────────────────────────
def main():
    audio_feedback.speak(
        # "Controller active. Commands are: start reader, capture, stop reader, "
        # "start pointer, stop pointer, stop all, exit."
        "Controller active"
    )

    while True:
        cmd = listen_command().lower().strip()
        print(f"Command received: '{cmd}'")

        if "start reader" in cmd or "read text" in cmd:
            # make sure detector is off
            if "point" in running_processes:
                print("Stopping object detection before starting reader.")
                audio_feedback.speak("Stopping object detection before starting reader.")
                stop_point_detector()

            if "ocr" not in running_processes:
                print("Starting Reader.")
                audio_feedback.speak("Starting Reader")
                running_processes["ocr"] = run_easyocr()
            else:
                print("Reader is already running.")
                audio_feedback.speak("Text reader is already running.")

        elif "capture" in cmd:
            if "ocr" in running_processes:
                print("Capturing image now.")
                audio_feedback.speak("Capturing image now.")
                open(OCR_CAPTURE_FILE, "w").write("go")
            else:
                audio_feedback.speak("Text reader is not running. Please start reader first.")

        elif "stop reader" in cmd or "stop ocr" in cmd:
            stop_easyocr()

        elif "start pointer" in cmd or "start object" in cmd:
            # make sure reader is off
            if "ocr" in running_processes:
                print("Stopping text reader before starting object detection.")
                audio_feedback.speak("Stopping text reader before starting object detection.")
                stop_easyocr()

            if "point" not in running_processes:
                print("Starting Pointer.")
                audio_feedback.speak("Starting Pointer")
                running_processes["point"] = run_point_detector()
            else:
                print("Object detection is already running.")
                audio_feedback.speak("Object detection is already running.")

        elif "stop pointer" in cmd or "stop object" in cmd:
            stop_point_detector()

        elif cmd in ("stop all", "stop"):
            stop_all()

        elif cmd in ("exit", "quit"):
            stop_all(silent=True)
            print("Exiting controller.")
            audio_feedback.speak("Exiting controller")
            time.sleep(3)
            break

        time.sleep(0.3)

if __name__ == "__main__":
    main()
