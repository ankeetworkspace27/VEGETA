import speech_recognition as sr
import sounddevice as sd
import numpy as np
import threading
import wave
import tempfile
import os


class Listener:

    def __init__(self):

        self.recognizer = sr.Recognizer()

        self.recognizer.dynamic_energy_threshold = True
        self.recognizer.pause_threshold = 0.8

        self.recording = False
        self.audio_data = []

        self.sample_rate = 16000
        self.channels = 1

        self.lock = threading.Lock()

    # =========================================================
    # START RECORDING
    # =========================================================

    def start_recording(self):

        if self.recording:
            return

        print(
            "VEGETA: Microphone recording started."
        )

        self.recording = True

        self.audio_data = []

        try:

            self.stream = sd.InputStream(
                samplerate=self.sample_rate,
                channels=self.channels,
                dtype="int16",
                callback=self.audio_callback
            )

            self.stream.start()

        except Exception as error:

            print(
                "VEGETA MICROPHONE ERROR:"
            )

            print(error)

            self.recording = False

    # =========================================================
    # AUDIO CALLBACK
    # =========================================================

    def audio_callback(
        self,
        indata,
        frames,
        time,
        status
    ):

        if status:

            print(
                f"VEGETA AUDIO STATUS: {status}"
            )

        if self.recording:

            with self.lock:

                self.audio_data.append(
                    indata.copy()
                )

    # =========================================================
    # STOP RECORDING
    # =========================================================

    def stop_recording(self):

        if not self.recording:
            return None

        print(
            "VEGETA: Microphone recording stopped."
        )

        self.recording = False

        try:

            self.stream.stop()
            self.stream.close()

        except Exception as error:

            print(
                "VEGETA STREAM ERROR:"
            )

            print(error)

        return self.process_recording()

    # =========================================================
    # PROCESS RECORDING
    # =========================================================

    def process_recording(self):

        with self.lock:

            if not self.audio_data:

                print(
                    "VEGETA: No audio recorded."
                )

                return None

            audio = np.concatenate(
                self.audio_data,
                axis=0
            )

        # -----------------------------------------------------
        # Create temporary WAV file
        # -----------------------------------------------------

        temp_file = tempfile.NamedTemporaryFile(
            suffix=".wav",
            delete=False
        )

        temp_path = temp_file.name

        temp_file.close()

        try:

            with wave.open(
                temp_path,
                "wb"
            ) as wav_file:

                wav_file.setnchannels(
                    self.channels
                )

                wav_file.setsampwidth(2)

                wav_file.setframerate(
                    self.sample_rate
                )

                wav_file.writeframes(
                    audio.tobytes()
                )

            # -------------------------------------------------
            # Load WAV into SpeechRecognition
            # -------------------------------------------------

            with sr.AudioFile(temp_path) as source:

                audio_data = self.recognizer.record(
                    source
                )

            # -------------------------------------------------
            # Google Speech Recognition
            # -------------------------------------------------

            try:

                text = self.recognizer.recognize_google(
                    audio_data
                )

                print(
                    f"You: {text}"
                )

                return text.lower()

            except sr.UnknownValueError:

                print(
                    "VEGETA: I couldn't understand that."
                )

                return None

            except sr.RequestError as error:

                print(
                    "VEGETA: Speech recognition service error."
                )

                print(error)

                return None

        except Exception as error:

            print(
                "VEGETA RECORDING ERROR:"
            )

            print(error)

            return None

        finally:

            try:

                os.remove(temp_path)

            except Exception:
                pass

    # =========================================================
    # COMPATIBILITY METHOD
    # =========================================================

    def listen(self):

        self.start_recording()

        input(
            "Press ENTER to stop recording..."
        )

        return self.stop_recording()


# =============================================================
# GLOBAL LISTENER
# =============================================================

listener = Listener()


# =============================================================
# NORMAL LISTEN FUNCTION
# =============================================================

def listen():

    return listener.listen()


# =============================================================
# PUSH-TO-TALK FUNCTIONS
# =============================================================

def start_recording():

    listener.start_recording()


def stop_recording():

    return listener.stop_recording()