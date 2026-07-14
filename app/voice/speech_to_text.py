import speech_recognition as sr


class VoiceRecognizer:

    def __init__(self):
        self.recognizer = sr.Recognizer()

        # Adjust recognition sensitivity
        self.recognizer.energy_threshold = 300
        self.recognizer.dynamic_energy_threshold = True


    def listen(self):

        with sr.Microphone() as source:

            print("Listening...")

            # Reduce background noise
            self.recognizer.adjust_for_ambient_noise(
                source,
                duration=0.5
            )

            try:

                audio = self.recognizer.listen(
                    source,
                    timeout=5,
                    phrase_time_limit=10
                )


                text = self.recognizer.recognize_google(
                    audio
                )


                print(f"Customer: {text}")

                return text


            except sr.WaitTimeoutError:

                print("No speech detected")
                return None


            except sr.UnknownValueError:

                print("Could not understand audio")
                return None


            except sr.RequestError:

                print("Speech recognition service error")
                return None