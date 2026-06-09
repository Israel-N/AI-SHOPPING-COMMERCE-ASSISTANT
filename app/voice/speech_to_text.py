import speech_recognition as sr

class VoiceRecognizer:

    def __init__(self):
        self.recognizer = sr.Recognizer()

    def listen(self):

        with sr.Microphone() as source:

            print("Listening...")

            self.recognizer.adjust_for_ambient_noise(
                source,
                duration=1
            )

            audio = self.recognizer.listen(source)

            try:
                text = self.recognizer.recognize_google(audio)

                print(f"Customer: {text}")

                return text

            except Exception:
                return None