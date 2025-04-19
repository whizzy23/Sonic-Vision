import speech_recognition as sr

def listen_command(device_index=2, timeout=5, phrase_limit=5):
    recognizer = sr.Recognizer()

    try:
        with sr.Microphone(device_index=device_index) as source:
            print("🎤 Adjusting for ambient noise...")
            recognizer.adjust_for_ambient_noise(source, duration=1)

            print("🎧 Listening for command...")
            audio = recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_limit)

        # Try recognizing using Google Web Speech API
        try:
            command = recognizer.recognize_google(audio, language="en-US").lower().strip()
            print(f"🧠 Heard: {command}")
            return command

        except sr.UnknownValueError:
            print("❓ Didn't catch that. Try again.")
            return ""

        except sr.RequestError as e:
            print(f"❌ Could not request results from Google Speech Recognition service: {e}")
            return "API unavailable"

    except sr.WaitTimeoutError:
        print("⏳ Timeout: No speech detected.")
        return ""

    except OSError as mic_error:
        print(f"🎙️ Microphone error: {mic_error}")
        return ""

    except Exception as e:
        print(f"🚨 Unexpected error: {e}")
        return ""
