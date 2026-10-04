import pyautogui


class MouseController:
    """
    Handles mouse automation for VEGETA.
    """

    def move_to(self, x, y, duration=0.2):
        """
        Move the mouse to a screen position.
        """
        pyautogui.moveTo(x, y, duration=duration)
        print(f"VEGETA MOUSE: Moved -> ({x}, {y})")

    def click(self, x=None, y=None):
        """
        Click at the current mouse position or at a specified position.
        """
        if x is not None and y is not None:
            self.move_to(x, y)

        pyautogui.click()
        print("VEGETA MOUSE: Clicked")

    def double_click(self, x=None, y=None):
        """
        Double-click at the current mouse position or at a specified position.
        """
        if x is not None and y is not None:
            self.move_to(x, y)

        pyautogui.doubleClick()
        print("VEGETA MOUSE: Double-clicked")

    def right_click(self, x=None, y=None):
        """
        Right-click at the current mouse position or at a specified position.
        """
        if x is not None and y is not None:
            self.move_to(x, y)

        pyautogui.rightClick()
        print("VEGETA MOUSE: Right-clicked")

    def scroll(self, amount):
        """
        Scroll vertically.
        Positive = up
        Negative = down
        """
        pyautogui.scroll(amount)
        print(f"VEGETA MOUSE: Scrolled -> {amount}")

    def drag_to(self, x, y, duration=0.5):
        """
        Drag the mouse to a specified screen position.
        """
        pyautogui.dragTo(x, y, duration=duration)
        print(f"VEGETA MOUSE: Dragged -> ({x}, {y})")


mouse_controller = MouseController()