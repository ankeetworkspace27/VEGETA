from automation.keyboard import keyboard_controller
from automation.mouse import mouse_controller
from automation.window import window_controller


class AppActions:
    """
    High-level application interaction controller for VEGETA.

    Combines window, keyboard, and mouse automation into
    simple actions that VEGETA's brain can use.
    """

    def focus(self, window_name):
        """
        Bring an application/window to the foreground.
        """

        return window_controller.focus_window(window_name)

    def minimize(self, window_name):
        """
        Minimize an application/window.
        """

        return window_controller.minimize_window(window_name)

    def maximize(self, window_name):
        """
        Maximize an application/window.
        """

        return window_controller.maximize_window(window_name)

    def press(self, key):
        """
        Press a keyboard key.
        """

        keyboard_controller.press(key)

    def hotkey(self, *keys):
        """
        Press a keyboard shortcut.
        """

        keyboard_controller.hotkey(*keys)

    def type_text(self, text, interval=0.02):
        """
        Type text into the currently focused application.
        """

        keyboard_controller.type_text(text, interval)

    def click(self, x=None, y=None):
        """
        Click using the mouse.
        """

        mouse_controller.click(x, y)

    def double_click(self, x=None, y=None):
        """
        Double-click using the mouse.
        """

        mouse_controller.double_click(x, y)

    def right_click(self, x=None, y=None):
        """
        Right-click using the mouse.
        """

        mouse_controller.right_click(x, y)

    def move_mouse(self, x, y, duration=0.2):
        """
        Move the mouse.
        """

        mouse_controller.move_to(x, y, duration)

    def scroll(self, amount):
        """
        Scroll the current application.
        """

        mouse_controller.scroll(amount)

    def search_with_keyboard(self, window_name, shortcut, query):
        """
        Focus an application, use a search shortcut,
        type a query, and submit it.
        """

        focused = self.focus(window_name)

        if not focused:
            return False

        self.hotkey(*shortcut)
        self.type_text(query)
        self.press("enter")

        return True


# Global VEGETA application-action controller.
app_actions = AppActions()