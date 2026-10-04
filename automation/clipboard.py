import tkinter as tk


class ClipboardManager:
    """
    Handles clipboard operations for VEGETA.
    """

    def __init__(self):
        self.root = None

    # ---------------------------------------------------------
    # INTERNAL CLIPBOARD ACCESS
    # ---------------------------------------------------------

    def _create_root(self):
        if self.root is None:
            self.root = tk.Tk()
            self.root.withdraw()

        self.root.update()

    # ---------------------------------------------------------
    # SET CLIPBOARD
    # ---------------------------------------------------------

    def set_text(self, text):
        if text is None:
            return False

        try:
            self._create_root()

            self.root.clipboard_clear()
            self.root.clipboard_append(str(text))
            self.root.update()

            print(f"VEGETA CLIPBOARD: Set -> {text}")
            return True

        except Exception as error:
            print(f"VEGETA CLIPBOARD: Set failed -> {error}")
            return False

    # ---------------------------------------------------------
    # GET CLIPBOARD
    # ---------------------------------------------------------

    def get_text(self):
        try:
            self._create_root()

            text = self.root.clipboard_get()
            self.root.update()

            print(f"VEGETA CLIPBOARD: Read -> {text}")
            return text

        except tk.TclError:
            print("VEGETA CLIPBOARD: Clipboard is empty.")
            return ""

        except Exception as error:
            print(f"VEGETA CLIPBOARD: Read failed -> {error}")
            return ""

    # ---------------------------------------------------------
    # CLEAR CLIPBOARD
    # ---------------------------------------------------------

    def clear(self):
        try:
            self._create_root()

            self.root.clipboard_clear()
            self.root.update()

            print("VEGETA CLIPBOARD: Cleared.")
            return True

        except Exception as error:
            print(f"VEGETA CLIPBOARD: Clear failed -> {error}")
            return False

    # ---------------------------------------------------------
    # CLOSE
    # ---------------------------------------------------------

    def close(self):
        if self.root is not None:
            try:
                self.root.destroy()
            except Exception:
                pass

            self.root = None


clipboard_manager = ClipboardManager()