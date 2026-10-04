from datetime import datetime
import time

from PySide6.QtCore import (
    Qt,
    QTimer,
    QThread,
    Signal,
    QObject,
)
from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
)

from pynput import keyboard

from ui.orb import AIOrb

from voice.listen import (
    start_recording,
    stop_recording,
)

from voice.speak import speak

from ai.brain import process_command as brain_process

from automation.search import search_manager


# =========================================================
# VOICE PROCESSING WORKER
# =========================================================

class VoiceWorker(QThread):

    result_ready = Signal(object)
    finished_processing = Signal()

    def run(self):

        try:

            print("VEGETA: Processing recording...")

            # Stop microphone and convert speech to text
            command = stop_recording()

            self.result_ready.emit(command)

        except Exception as error:

            print("VEGETA VOICE WORKER ERROR:")
            print(error)

            self.result_ready.emit(None)

        finally:

            self.finished_processing.emit()


# =========================================================
# GLOBAL KEYBOARD BRIDGE
# =========================================================

class KeyboardBridge(QObject):

    key_pressed = Signal()
    key_released = Signal()

    def __init__(self):

        super().__init__()

        self.key_down = False

        self.listener = keyboard.Listener(
            on_press=self.on_press,
            on_release=self.on_release,
        )

        self.listener.daemon = True

        self.listener.start()

        print(
            "VEGETA: Global keyboard listener started."
        )

        print(
            "VEGETA: Hold RIGHT CTRL to talk."
        )

    # =====================================================
    # KEY PRESS
    # =====================================================

    def on_press(self, key):

        if key == keyboard.Key.ctrl_r:

            # Prevent repeated key events
            if self.key_down:
                return

            self.key_down = True

            print(
                "VEGETA: RIGHT CTRL PRESSED"
            )

            self.key_pressed.emit()

    # =====================================================
    # KEY RELEASE
    # =====================================================

    def on_release(self, key):

        if key == keyboard.Key.ctrl_r:

            if not self.key_down:
                return

            self.key_down = False

            print(
                "VEGETA: RIGHT CTRL RELEASED"
            )

            self.key_released.emit()

    # =====================================================
    # STOP KEYBOARD LISTENER
    # =====================================================

    def stop(self):

        try:

            self.listener.stop()

        except Exception as error:

            print(
                "VEGETA KEYBOARD STOP ERROR:"
            )

            print(error)


# =========================================================
# HOME WINDOW
# =========================================================

class HomeWindow(QWidget):

    def __init__(self):

        super().__init__()

        # =====================================================
        # WINDOW
        # =====================================================

        self.setWindowTitle(
            "VEGETA AI Assistant"
        )

        self.resize(
            900,
            600
        )

        # =====================================================
        # STATE
        # =====================================================

        self.is_recording = False
        self.recording_started_at = None
        self.shutdown_requested = False

        self.voice_worker = None

        # VEGETA's current voice/UI state.
        # The orb reflects this state visually.
        self.assistant_state = "ready"

        # =====================================================
        # MAIN LAYOUT
        # =====================================================

        layout = QVBoxLayout()

        # =====================================================
        # TITLE
        # =====================================================

        self.title_label = QLabel(
            "VEGETA"
        )

        self.title_label.setAlignment(
            Qt.AlignCenter
        )

        self.subtitle_label = QLabel(
            "AI Desktop Assistant"
        )

        self.subtitle_label.setAlignment(
            Qt.AlignCenter
        )

        # =====================================================
        # ORB
        # =====================================================

        self.orb = AIOrb()

        # =====================================================
        # GREETING
        # =====================================================

        self.greeting_label = QLabel()

        self.greeting_label.setAlignment(
            Qt.AlignCenter
        )

        self.time_label = QLabel()

        self.time_label.setAlignment(
            Qt.AlignCenter
        )

        self.date_label = QLabel()

        self.date_label.setAlignment(
            Qt.AlignCenter
        )

        # =====================================================
        # STYLES
        # =====================================================

        self.title_label.setStyleSheet(
            """
            font-size:42px;
            font-weight:bold;
            color:#00E5FF;
            """
        )

        self.subtitle_label.setStyleSheet(
            """
            font-size:16px;
            color:#B0BEC5;
            letter-spacing:2px;
            """
        )

        self.greeting_label.setStyleSheet(
            """
            font-size:34px;
            font-weight:bold;
            color:white;
            """
        )

        self.time_label.setStyleSheet(
            """
            font-size:48px;
            font-weight:bold;
            color:#4FC3F7;
            """
        )

        self.date_label.setStyleSheet(
            """
            font-size:18px;
            color:#AAAAAA;
            """
        )

        # =====================================================
        # LAYOUT
        # =====================================================

        layout.addStretch()

        layout.addWidget(
            self.title_label
        )

        layout.addWidget(
            self.subtitle_label
        )

        layout.addSpacing(30)

        layout.addWidget(
            self.orb,
            alignment=Qt.AlignCenter
        )

        layout.addSpacing(20)

        layout.addWidget(
            self.greeting_label
        )

        layout.addWidget(
            self.time_label
        )

        layout.addWidget(
            self.date_label
        )

        layout.addSpacing(30)

        layout.addStretch()

        self.setLayout(
            layout
        )

        # =====================================================
        # WINDOW STYLE
        # =====================================================

        self.setStyleSheet(
            """
            QWidget {
                background:#1E1E1E;
            }
            """
        )

        # =====================================================
        # CLOCK
        # =====================================================

        self.timer = QTimer(self)

        self.timer.timeout.connect(
            self.update_datetime
        )

        self.timer.start(
            1000
        )

        self.update_datetime()

        # =====================================================
        # GLOBAL KEYBOARD
        # =====================================================

        self.keyboard_bridge = KeyboardBridge()

        self.keyboard_bridge.key_pressed.connect(
            self.start_listening
        )

        self.keyboard_bridge.key_released.connect(
            self.stop_listening
        )

        # =====================================================
        # ORB BACKUP
        # =====================================================

        self.connect_orb()

        self.set_ready_status()

        print(
            "VEGETA: System ready."
        )

    # =========================================================
    # CONNECT ORB
    # =========================================================

    def connect_orb(self):

        # New orb implementation
        if hasattr(
            self.orb,
            "orb_clicked",
        ):

            try:

                self.orb.orb_clicked.connect(
                    self.start_listening
                )

                print(
                    "VEGETA: Orb connected."
                )

                return

            except Exception as error:

                print(
                    "VEGETA ORB CONNECTION ERROR:"
                )

                print(error)

        # Older orb implementation
        if hasattr(
            self.orb,
            "clicked",
        ):

            try:

                self.orb.clicked.connect(
                    self.start_listening
                )

                print(
                    "VEGETA: Orb connected."
                )

                return

            except Exception as error:

                print(
                    "VEGETA ORB CONNECTION ERROR:"
                )

                print(error)

        # Fallback for older custom orb
        if hasattr(
            self.orb,
            "on_orb_click",
        ):

            self.orb.on_orb_click = (
                self.start_listening
            )

    # =========================================================
    # DATE / TIME
    # =========================================================

    def update_datetime(self):

        now = datetime.now()

        if now.hour < 12:

            greeting = (
                "🌅 Good Morning, Sir"
            )

        elif now.hour < 17:

            greeting = (
                "☀️ Good Afternoon, Sir"
            )

        elif now.hour < 21:

            greeting = (
                "🌇 Good Evening, Sir"
            )

        else:

            greeting = (
                "🌙 Good Night, Sir"
            )

        self.greeting_label.setText(
            greeting
        )

        self.time_label.setText(
            now.strftime(
                "%I:%M:%S %p"
            )
        )

        self.date_label.setText(
            now.strftime(
                "%A, %d %B %Y"
            )
        )

    # =========================================================
    # START LISTENING
    # =========================================================

    def start_listening(self):
        """
        Start a new push-to-talk recording.

        Right Ctrl is deliberately treated as a physical push-to-talk
        trigger. A new recording is allowed only when VEGETA is actually
        ready. This prevents accidental recordings while the previous
        command is still being processed or spoken.
        """

        print(
            "HOME: START LISTENING CALLED"
        )

        if self.shutdown_requested:
            print(
                "VEGETA: Shutdown is in progress."
            )
            return

        # Already recording.
        if self.is_recording:
            print(
                "VEGETA: Already recording."
            )
            return

        # Do not interrupt speech or command processing.
        if self.assistant_state != "ready":
            print(
                f"VEGETA: Cannot start recording while state is "
                f"{self.assistant_state.upper()}."
            )
            return

        # Previous processing thread is still running.
        if (
            self.voice_worker is not None
            and self.voice_worker.isRunning()
        ):
            print(
                "VEGETA: Still processing previous command."
            )
            return

        self.is_recording = True
        self.recording_started_at = time.monotonic()

        print(
            "VEGETA: Starting microphone..."
        )

        self.set_listening_status()

        try:
            start_recording()

            # voice.listen.start_recording() normally handles its own
            # microphone errors. Give the recorder a moment to initialize
            # and verify that the shared listener actually entered recording
            # mode when that object is available.
            time.sleep(0.05)

            try:
                from voice.listen import listener

                if not getattr(listener, "recording", False):
                    raise RuntimeError(
                        "Microphone did not enter recording mode."
                    )
            except ImportError:
                # Keep compatibility if voice.listen ever removes the
                # module-level listener object.
                pass

        except Exception as error:

            print(
                "VEGETA START RECORDING ERROR:"
            )

            print(error)

            self.is_recording = False
            self.recording_started_at = None
            self.set_ready_status()

            try:
                stop_recording()
            except Exception:
                pass

    # =========================================================
    # STOP LISTENING
    # =========================================================

    def stop_listening(self):
        """
        Finish the current push-to-talk recording and hand it to the
        background worker for speech recognition.
        """

        if not self.is_recording:
            return

        print(
            "HOME: STOP LISTENING CALLED"
        )

        self.is_recording = False

        started_at = self.recording_started_at
        self.recording_started_at = None

        # Ignore an accidental ultra-short press. This avoids sending
        # effectively empty audio to speech recognition.
        if started_at is not None:
            recording_duration = time.monotonic() - started_at

            if recording_duration < 0.20:
                print(
                    f"VEGETA: Recording too short "
                    f"({recording_duration:.2f}s)."
                )

                try:
                    stop_recording()
                except Exception as error:
                    print(
                        "VEGETA STOP RECORDING ERROR:"
                    )
                    print(error)

                self.set_ready_status()
                return

        print(
            "VEGETA: Stopping microphone..."
        )

        self.set_processing_status()

        # -----------------------------------------------------
        # Start worker to process the recorded audio.
        # -----------------------------------------------------

        worker = VoiceWorker()
        self.voice_worker = worker

        worker.result_ready.connect(
            self.process_command
        )

        worker.finished_processing.connect(
            self.voice_worker_finished
        )

        try:
            worker.start()

        except Exception as error:
            print(
                "VEGETA VOICE WORKER START ERROR:"
            )
            print(error)

            self.voice_worker = None
            self.set_ready_status()

    # =========================================================
    # PROCESS COMMAND
    # =========================================================

    def process_command(self, command):

        print(
            f"HOME: COMMAND RECEIVED -> {command}"
        )

        if not command:

            print(
                "VEGETA: No usable command received."
            )

            self.set_ready_status()

            return

        # A worker result should only be handled while VEGETA is in
        # the processing stage. This prevents an old/late worker signal
        # from unexpectedly changing a newer voice session.
        if self.assistant_state != "processing":
            print(
                "VEGETA: Ignoring stale voice result."
            )
            return

        # -----------------------------------------------------
        # Active website search mode
        # -----------------------------------------------------
        # Search mode is persistent, but it only intercepts an
        # explicitly spoken web-search command. Normal VEGETA
        # commands such as OPEN, FIND, CREATE, DELETE, etc. must
        # still reach the main brain.
        active_target = search_manager.get_target()

        if active_target:

            # -------------------------------------------------
            # Explicitly leave search mode
            # -------------------------------------------------
            if search_manager.is_exit_command(command):
                search_manager.clear_target()

                response = "Exiting search mode."

                print(f"VEGETA: {response}")
                self.set_speaking_status()

                try:
                    speak(response)
                except Exception as error:
                    print("VEGETA TTS ERROR:")
                    print(error)

                self.set_ready_status()
                return

            raw_query = str(command).strip()
            lowered_query = raw_query.lower()

            # ONLY these prefixes activate the persistent website
            # search. In particular, do NOT treat 'find' or 'open'
            # as web searches because those belong to the main brain.
            search_prefixes = (
                "search for ",
                "search ",
                "look for ",
                "play ",
                "watch ",
                "show me ",
                "look up ",
            )

            search_query = None

            for prefix in search_prefixes:
                if lowered_query.startswith(prefix):
                    search_query = raw_query[len(prefix):].strip()
                    break

            if search_query:

                print(f"VEGETA SEARCH MODE: {active_target}")
                print(f"VEGETA SEARCH QUERY: {search_query}")

                try:
                    search_success = search_manager.search(search_query)
                except Exception as error:
                    print("VEGETA SEARCH ERROR:")
                    print(error)
                    search_success = False

                if search_success:
                    # Keep the target active so another explicit
                    # search can be performed on the same website.
                    response = (
                        f"Searching {active_target} for {search_query}."
                    )

                    print(f"VEGETA: {response}")
                    self.set_speaking_status()

                    try:
                        print(f"VEGETA TTS: {response}")
                        speak(response)
                    except Exception as error:
                        print("VEGETA TTS ERROR:")
                        print(error)

                    self.set_ready_status()
                    return

                print("VEGETA: Search failed; keeping target active.")

        # -----------------------------------------------------
        # Send command to VEGETA brain
        # -----------------------------------------------------

        try:

            response = brain_process(
                command
            )

        except Exception as error:

            print(
                "VEGETA BRAIN ERROR:"
            )

            print(error)

            self.set_ready_status()

            return

        print(
            f"VEGETA: {response}"
        )

        # -----------------------------------------------------
        # Speaking
        # -----------------------------------------------------

        self.set_speaking_status()

        try:

            speak(
                response
            )

        except Exception as error:

            print(
                "VEGETA TTS ERROR:"
            )

            print(error)

        self.set_ready_status()

    # =========================================================
    # WORKER FINISHED
    # =========================================================

    def voice_worker_finished(self):
        """
        Clean up the worker reference.

        This method intentionally does NOT change the assistant state.
        The command/TTS lifecycle owns the visible state:
            RIGHT CTRL DOWN -> LISTENING
            RIGHT CTRL UP   -> PROCESSING
            COMMAND         -> SPEAKING
            TTS COMPLETE    -> READY
        """

        print(
            "VEGETA: Voice worker finished."
        )

        finished_worker = self.voice_worker

        # Clear only if the signal belongs to the worker currently tracked
        # by the window. This prevents an old worker callback from clearing
        # a newer worker reference.
        if finished_worker is not None and not finished_worker.isRunning():
            self.voice_worker = None

    # =========================================================
    # ASSISTANT STATE
    # =========================================================

    def set_assistant_state(self, state):
        """
        Keep one authoritative state for the voice/UI flow.

        States:
            ready      -> waiting for a command
            listening  -> microphone is recording
            processing -> speech/command is being processed
            speaking   -> VEGETA is speaking
        """

        state = str(state).lower().strip()

        valid_states = (
            "ready",
            "listening",
            "processing",
            "speaking",
        )

        if state not in valid_states:
            state = "ready"

        if self.assistant_state == state:
            return

        self.assistant_state = state

        print(
            f"VEGETA STATE: {state.upper()}"
        )

        # The orb uses its own visual state names.
        orb_state = {
            "ready": "idle",
            "listening": "listening",
            "processing": "thinking",
            "speaking": "speaking",
        }[state]

        try:
            self.orb.set_state(orb_state)
        except Exception as error:
            print("VEGETA ORB STATE ERROR:")
            print(error)

    # =========================================================
    # LISTENING STATUS
    # =========================================================

    def set_listening_status(self):
        self.set_assistant_state("listening")

    # =========================================================
    # PROCESSING STATUS
    # =========================================================

    def set_processing_status(self):
        self.set_assistant_state("processing")

    # =========================================================
    # SPEAKING STATUS
    # =========================================================

    def set_speaking_status(self):
        self.set_assistant_state("speaking")

    # =========================================================
    # READY STATUS
    # =========================================================

    def set_ready_status(self):
        self.set_assistant_state("ready")

    # =========================================================
    # CLOSE EVENT
    # =========================================================

    def closeEvent(self, event):

        self.shutdown_requested = True

        print(
            "VEGETA: Shutting down..."
        )

        # -----------------------------------------------------
        # Stop keyboard listener
        # -----------------------------------------------------

        if self.keyboard_bridge is not None:

            print(
                "VEGETA: Stopping keyboard listener..."
            )

            self.keyboard_bridge.stop()

        # -----------------------------------------------------
        # Stop microphone if recording
        # -----------------------------------------------------

        if self.is_recording:

            print(
                "VEGETA: Stopping microphone..."
            )

            self.is_recording = False
            self.recording_started_at = None

            try:

                stop_recording()

            except Exception as error:

                print(
                    "VEGETA STOP RECORDING ERROR:"
                )

                print(error)

        # -----------------------------------------------------
        # Wait for voice worker
        # -----------------------------------------------------

        if (
            self.voice_worker is not None
            and self.voice_worker.isRunning()
        ):

            print(
                "VEGETA: Waiting for voice worker..."
            )

            self.voice_worker.wait()

        print(
            "VEGETA: Shutdown complete."
        )

        event.accept()