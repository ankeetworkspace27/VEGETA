import pyttsx3
import threading


class Speaker:

    def __init__(self):

        self.lock = threading.Lock()

    def speak(self, text):

        if not text:
            return

        with self.lock:

            engine = None

            try:

                print(f"VEGETA TTS: {text}")

                # Create a fresh engine for every response.
                # This avoids Windows SAPI/pyttsx3 getting stuck
                # between consecutive commands.
                engine = pyttsx3.init("sapi5")

                engine.setProperty(
                    "rate",
                    175
                )

                engine.setProperty(
                    "volume",
                    1.0
                )

                engine.say(
                    str(text)
                )

                engine.runAndWait()

            except Exception as error:

                print(
                    "VEGETA TTS ERROR:"
                )

                print(error)

            finally:

                if engine is not None:

                    try:
                        engine.stop()

                    except Exception:
                        pass

                    del engine


speaker = Speaker()


def speak(text):

    speaker.speak(text)