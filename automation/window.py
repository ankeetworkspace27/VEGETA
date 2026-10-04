import ctypes
import time

from ctypes import WINFUNCTYPE


user32 = ctypes.windll.user32


class WindowController:

    def __init__(self):
        self.user32 = user32

    # ---------------------------------------------------------
    # Get all visible windows
    # ---------------------------------------------------------

    def get_windows(self):

        windows = []

        def enum_callback(hwnd, _):

            if self.user32.IsWindowVisible(hwnd):

                length = self.user32.GetWindowTextLengthW(hwnd)

                if length > 0:

                    title = ctypes.create_unicode_buffer(
                        length + 1
                    )

                    self.user32.GetWindowTextW(
                        hwnd,
                        title,
                        length + 1
                    )

                    window_title = title.value.strip()

                    if window_title:

                        windows.append({
                            "hwnd": hwnd,
                            "title": window_title,
                        })

            return True

        callback = WINFUNCTYPE(
            ctypes.c_bool,
            ctypes.c_void_p,
            ctypes.c_void_p,
        )(enum_callback)

        self.user32.EnumWindows(
            callback,
            0
        )

        return windows

    # ---------------------------------------------------------
    # Find a window
    # ---------------------------------------------------------

    def find_window(self, search_text):

        if not search_text:
            return None

        search_text = str(
            search_text
        ).strip().lower()

        windows = self.get_windows()

        for window in windows:

            title = window["title"].lower()

            if search_text in title:

                return window

        return None

    # ---------------------------------------------------------
    # Focus a window
    # ---------------------------------------------------------

    def focus_window(self, search_text):

        window = self.find_window(
            search_text
        )

        if not window:

            print(
                f"VEGETA WINDOW: Window not found -> {search_text}"
            )

            return False

        hwnd = window["hwnd"]

        try:

            # Restore if minimized.
            self.user32.ShowWindow(
                hwnd,
                9
            )

            # Bring to foreground.
            self.user32.SetForegroundWindow(
                hwnd
            )

            time.sleep(0.5)

            print(
                f"VEGETA WINDOW: Focused -> "
                f"{window['title']}"
            )

            return True

        except Exception as error:

            print(
                f"VEGETA WINDOW: Focus failed -> {error}"
            )

            return False

    # ---------------------------------------------------------
    # Focus Chrome
    # ---------------------------------------------------------

    def focus_chrome(self):

        window = self.find_window(
            "Google Chrome"
        )

        if not window:

            window = self.find_window(
                "Chrome"
            )

        if not window:

            print(
                "VEGETA WINDOW: Chrome window not found."
            )

            return False

        hwnd = window["hwnd"]

        try:

            self.user32.ShowWindow(
                hwnd,
                9
            )

            self.user32.SetForegroundWindow(
                hwnd
            )

            time.sleep(0.5)

            print(
                f"VEGETA WINDOW: Chrome focused -> "
                f"{window['title']}"
            )

            return True

        except Exception as error:

            print(
                f"VEGETA WINDOW: Chrome focus failed -> "
                f"{error}"
            )

            return False

    # ---------------------------------------------------------
    # Minimize window
    # ---------------------------------------------------------

    def minimize_window(self, search_text):

        window = self.find_window(
            search_text
        )

        if not window:

            print(
                f"VEGETA WINDOW: Window not found -> {search_text}"
            )

            return False

        self.user32.ShowWindow(
            window["hwnd"],
            6
        )

        print(
            f"VEGETA WINDOW: Minimized -> "
            f"{window['title']}"
        )

        return True

    # ---------------------------------------------------------
    # Maximize window
    # ---------------------------------------------------------

    def maximize_window(self, search_text):

        window = self.find_window(
            search_text
        )

        if not window:

            print(
                f"VEGETA WINDOW: Window not found -> {search_text}"
            )

            return False

        self.user32.ShowWindow(
            window["hwnd"],
            3
        )

        print(
            f"VEGETA WINDOW: Maximized -> "
            f"{window['title']}"
        )

        return True


window_controller = WindowController()