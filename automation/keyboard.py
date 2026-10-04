import pyautogui
import time


class KeyboardController:
    """
    Handles keyboard automation for VEGETA.
    """

    def press(self, key):
        pyautogui.press(key)
        print(f"VEGETA KEYBOARD: Pressed -> {key}")

    def hotkey(self, *keys):
        pyautogui.hotkey(*keys)
        print(f"VEGETA KEYBOARD: Hotkey -> {' + '.join(keys)}")

    def type_text(self, text, interval=0.02):
        pyautogui.write(text, interval=interval)
        print(f"VEGETA KEYBOARD: Typed -> {text}")

    def enter(self):
        self.press("enter")

    def escape(self):
        self.press("esc")

    def select_all(self):
        self.hotkey("ctrl", "a")

    def copy(self):
        self.hotkey("ctrl", "c")

    def paste(self):
        self.hotkey("ctrl", "v")


keyboard_controller = KeyboardController()