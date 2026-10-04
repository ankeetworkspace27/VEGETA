from datetime import datetime
import ctypes
import os
import re
import subprocess
import webbrowser
from urllib.parse import quote_plus

import pyautogui

import psutil
from PIL import ImageGrab
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from comtypes import CLSCTX_ALL
from memory.memory import memory_manager
from automation.search import search_manager
from automation.file_manager import file_manager
from automation.clipboard import clipboard_manager


# =========================================================
# WEBSITES
# =========================================================

WEBSITES = {
    # Shopping
    "amazon": "https://www.amazon.in",
    "flipkart": "https://www.flipkart.com",
    "meesho": "https://www.meesho.com",
    "snapdeal": "https://www.snapdeal.com",
    "indiamart": "https://www.indiamart.com",
    # Fashion
    "myntra": "https://www.myntra.com",
    "ajio": "https://www.ajio.com",
    "tata cliq": "https://www.tatacliq.com",
    "tatacliq": "https://www.tatacliq.com",
    "nykaa": "https://www.nykaa.com",
    "nykaa fashion": "https://www.nykaafashion.com",
    # Electronics
    "croma": "https://www.croma.com",
    "reliance digital": "https://www.reliancedigital.in",
    "reliance digital india": "https://www.reliancedigital.in",
    # Grocery
    "jiomart": "https://www.jiomart.com",
    "jio mart": "https://www.jiomart.com",
    "bigbasket": "https://www.bigbasket.com",
    "blinkit": "https://blinkit.com",
    "zepto": "https://www.zeptonow.com",
    "dmart": "https://www.dmart.in",
    # Beauty / eyewear / home
    "tira": "https://www.tirabeauty.com",
    "purplle": "https://www.purplle.com",
    "lenskart": "https://www.lenskart.com",
    "pepperfry": "https://www.pepperfry.com",
    "urban ladder": "https://www.urbanladder.com",
    "firstcry": "https://www.firstcry.com",
    # General / entertainment
    "google": "https://www.google.com",
    "youtube": "https://www.youtube.com",
    "netflix": "https://www.netflix.com",
    "prime video": "https://www.primevideo.com",
    "primevideo": "https://www.primevideo.com",
    "amazon prime video": "https://www.primevideo.com",
    "jiohotstar": "https://www.hotstar.com/in",
    "jio hotstar": "https://www.hotstar.com/in",
    "hotstar": "https://www.hotstar.com/in",
    "sonyliv": "https://www.sonyliv.com",
    "sony liv": "https://www.sonyliv.com",
    "zee5": "https://www.zee5.com",
    "zee 5": "https://www.zee5.com",
    "aha": "https://www.aha.video",
    "sun nxt": "https://www.sunnxt.com",
    "sunnxt": "https://www.sunnxt.com",
    "lionsgate play": "https://www.lionsgateplay.com",
    "apple tv": "https://tv.apple.com",
    "apple tv plus": "https://tv.apple.com",
    # Music
    "spotify": "https://open.spotify.com",
    "jiosaavn": "https://www.jiosaavn.com",
    "jio saavn": "https://www.jiosaavn.com",
    "youtube music": "https://music.youtube.com",
    "apple music": "https://music.apple.com",
    # Social / communication
    "instagram": "https://www.instagram.com",
    "facebook": "https://www.facebook.com",
    "twitter": "https://x.com",
    "x": "https://x.com",
    "linkedin": "https://www.linkedin.com",
    "reddit": "https://www.reddit.com",
    "threads": "https://www.threads.net",
    "gmail": "https://mail.google.com",
    "whatsapp": "https://web.whatsapp.com",
    "telegram": "https://web.telegram.org",
    "outlook": "https://outlook.live.com",
    # AI / development
    "chatgpt": "https://chatgpt.com",
    "gemini": "https://gemini.google.com",
    "claude": "https://claude.ai",
    "perplexity": "https://www.perplexity.ai",
    "github": "https://github.com",
    "gitlab": "https://gitlab.com",
    "stackoverflow": "https://stackoverflow.com",
    "kaggle": "https://www.kaggle.com",
    # Google / productivity
    "google drive": "https://drive.google.com",
    "google docs": "https://docs.google.com",
    "google sheets": "https://sheets.google.com",
    "google slides": "https://slides.google.com",
    "notion": "https://www.notion.so",
}


# =========================================================
# WINDOWS APPLICATIONS
# =========================================================

WINDOWS_APPS = {
    "notepad": "notepad.exe",
    "calculator": "calc.exe",
    "calc": "calc.exe",
    "paint": "mspaint.exe",
    "command prompt": "cmd.exe",
    "cmd": "cmd.exe",
    "powershell": "powershell.exe",
    "task manager": "taskmgr.exe",
    "file explorer": "explorer.exe",
    "explorer": "explorer.exe",
    "settings": "ms-settings:",
    "camera": "microsoft.windows.camera:",
    "camera app": "microsoft.windows.camera:",
    "chrome": "chrome.exe",
    "google chrome": "chrome.exe",
    "edge": "msedge.exe",
    "microsoft edge": "msedge.exe",
    "firefox": "firefox.exe",
}


# =========================================================
# WINDOWS SETTINGS
# =========================================================

WINDOWS_SETTINGS = {
    "settings": "ms-settings:",
    "wifi": "ms-settings:network-wifi",
    "wi-fi": "ms-settings:network-wifi",
    "network": "ms-settings:network-status",
    "network settings": "ms-settings:network-status",
    "bluetooth": "ms-settings:bluetooth",
    "bluetooth settings": "ms-settings:bluetooth",
    "display": "ms-settings:display",
    "display settings": "ms-settings:display",
    "sound": "ms-settings:sound",
    "sound settings": "ms-settings:sound",
    "personalization": "ms-settings:personalization",
    "background": "ms-settings:personalization-background",
    "colors": "ms-settings:colors",
    "apps": "ms-settings:appsfeatures",
    "installed apps": "ms-settings:appsfeatures",
    "windows update": "ms-settings:windowsupdate",
    "update": "ms-settings:windowsupdate",
    "accounts": "ms-settings:accounts",
    "your info": "ms-settings:yourinfo",
    "sign in options": "ms-settings:signinoptions",
    "privacy": "ms-settings:privacy",
    "privacy settings": "ms-settings:privacy",
    "camera": "ms-settings:privacy-webcam",
    "microphone": "ms-settings:privacy-microphone",
    "gaming": "ms-settings:gaming-gamebar",
    "storage": "ms-settings:storagesense",
    "power": "ms-settings:powersleep",
    "notifications": "ms-settings:notifications",
    "default apps": "ms-settings:defaultapps",
    "about": "ms-settings:about",
}


# =========================================================
# SPECIAL FOLDERS
# =========================================================

SPECIAL_FOLDERS = {
    # Ask Windows for the actual Known Folder locations. This also handles
    # folders that have been moved/redirected away from C:\Users\<user>.
    "downloads": file_manager.get_special_folder("downloads"),
    "download": file_manager.get_special_folder("downloads"),
    "documents": file_manager.get_special_folder("documents"),
    "document": file_manager.get_special_folder("documents"),
    "desktop": file_manager.get_special_folder("desktop"),
    "pictures": file_manager.get_special_folder("pictures"),
    "music": file_manager.get_special_folder("music"),
    "videos": file_manager.get_special_folder("videos"),
}


# =========================================================
# COMMAND CLEANER
# =========================================================

def clean_command(command):
    """
    Normalize spoken commands so natural conversational requests
    can be understood by the command router.
    """

    if not command:
        return None

    command = str(command).lower().strip()

    # Remove common punctuation added by speech recognition.
    command = re.sub(r"[,.!?;:]+", " ", command)
    command = re.sub(r"\s+", " ", command).strip()

    # Remove wake words when they appear at the beginning.
    wake_words = (
        "hey vegeta",
        "hi vegeta",
        "okay vegeta",
        "ok vegeta",
        "vegeta",
    )

    for wake_word in wake_words:
        if command.startswith(wake_word):
            command = command[len(wake_word):].strip()
            break

    # Conversational prefixes. These can repeat.
    prefix_phrases = (
        "can you please ",
        "could you please ",
        "would you please ",
        "please can you ",
        "can you ",
        "could you ",
        "would you ",
        "please ",
        "i want you to ",
        "i need you to ",
        "i would like you to ",
        "i'd like you to ",
        "i want to ",
        "i need to ",
    )

    changed = True

    while changed and command:
        changed = False

        for phrase in prefix_phrases:
            if command.startswith(phrase):
                command = command[len(phrase):].strip()
                changed = True
                break

    # Natural endings.
    ending_phrases = (
    " for me",
    " for",
    " please",
    " if you can",
    " would you",
)

    changed = True

    while changed and command:
        changed = False

        for phrase in ending_phrases:
            if command.endswith(phrase):
                command = command[:-len(phrase)].strip()
                changed = True
                break

    return command


# =========================================================
# VOLUME CONTROLLER
# =========================================================

def get_volume_controller():
    devices = AudioUtilities.GetSpeakers()

    if hasattr(devices, "EndpointVolume"):
        return devices.EndpointVolume

    if hasattr(devices, "Activate"):
        interface = devices.Activate(
            IAudioEndpointVolume._iid_,
            CLSCTX_ALL,
            None,
        )
        return interface.QueryInterface(IAudioEndpointVolume)

    raise RuntimeError("Unable to access Windows audio endpoint.")


# =========================================================
# DESKTOP / WINDOW AUTOMATION HELPERS
# =========================================================

def minimize_current_window():
    """Minimize the currently active window."""
    pyautogui.hotkey("win", "down")


def maximize_current_window():
    """Maximize the currently active window."""
    pyautogui.hotkey("win", "up")


def restore_current_window():
    """Restore the currently active window."""
    pyautogui.hotkey("win", "shift", "m")


def close_current_window():
    """Close the currently active window."""
    pyautogui.hotkey("alt", "f4")


def show_desktop():
    """Show the Windows desktop."""
    pyautogui.hotkey("win", "d")


def find_and_close_window(target):
    """Find a visible window whose title contains target and close it."""
    user32 = ctypes.windll.user32
    matches = []

    EnumWindowsProc = ctypes.WINFUNCTYPE(
        ctypes.c_bool,
        ctypes.c_void_p,
        ctypes.c_void_p,
    )

    def callback(hwnd, lparam):
        if not user32.IsWindowVisible(hwnd):
            return True

        length = user32.GetWindowTextLengthW(hwnd)
        if length <= 0:
            return True

        buffer = ctypes.create_unicode_buffer(length + 1)
        user32.GetWindowTextW(hwnd, buffer, length + 1)
        title = buffer.value.strip()

        if title and target.lower() in title.lower():
            matches.append((hwnd, title))

        return True

    callback_ref = EnumWindowsProc(callback)
    user32.EnumWindows(callback_ref, 0)

    if not matches:
        return None

    hwnd, title = matches[0]
    user32.PostMessageW(hwnd, 0x0010, 0, 0)
    return title


def find_and_activate_window(target):
    """
    Find a visible Windows window whose title contains the target
    and bring it to the foreground.
    """
    user32 = ctypes.windll.user32

    matches = []

    EnumWindowsProc = ctypes.WINFUNCTYPE(
        ctypes.c_bool,
        ctypes.c_void_p,
        ctypes.c_void_p,
    )

    def callback(hwnd, lparam):
        if not user32.IsWindowVisible(hwnd):
            return True

        length = user32.GetWindowTextLengthW(hwnd)

        if length <= 0:
            return True

        buffer = ctypes.create_unicode_buffer(length + 1)
        user32.GetWindowTextW(hwnd, buffer, length + 1)

        title = buffer.value.strip()

        if title and target.lower() in title.lower():
            matches.append((hwnd, title))

        return True

    callback_ref = EnumWindowsProc(callback)
    user32.EnumWindows(callback_ref, 0)

    if not matches:
        return None

    hwnd, title = matches[0]

    # Restore if minimized.
    SW_RESTORE = 9
    user32.ShowWindow(hwnd, SW_RESTORE)

    # Bring the window to the foreground.
    user32.SetForegroundWindow(hwnd)

    return title


# =========================================================
# VEGETA BRAIN
# =========================================================

class VegetaBrain:

    def __init__(self):
        self.pending_delete = None
        self.pending_power_action = None
        print("VEGETA BRAIN: Online.")

    def _open_website(self, target):
        print(f"VEGETA ACTION: OPEN WEBSITE -> {target}")
        try:
            webbrowser.open(WEBSITES[target])

            # Remember the website so the next Right Ctrl command
            # can be used as a search command for that website.
            search_manager.set_target(target)

            print(
                f"VEGETA SEARCH: Active target -> {target}"
            )

            return f"Opening {target}."
        except Exception as error:
            print("VEGETA WEBSITE ERROR:")
            print(error)
            return f"I couldn't open {target}."

    def _open_app(self, target):
        print(f"VEGETA ACTION: OPEN APP -> {target}")
        try:
            subprocess.Popen(WINDOWS_APPS[target], shell=True)
            return f"Opening {target}."
        except Exception as error:
            print("VEGETA APP ERROR:")
            print(error)
            return f"I couldn't open {target}."

    def _open_settings(self, target):
        print(f"VEGETA ACTION: OPEN SETTINGS -> {target}")
        try:
            os.startfile(WINDOWS_SETTINGS[target])
            return f"Opening {target} settings."
        except Exception as error:
            print("VEGETA SETTINGS ERROR:")
            print(error)
            return f"I couldn't open {target} settings."

    def _open_folder(self, target):
        print(f"VEGETA ACTION: OPEN FOLDER -> {target}")
        try:
            os.startfile(SPECIAL_FOLDERS[target])
            return f"Opening {target}."
        except Exception as error:
            print("VEGETA FOLDER ERROR:")
            print(error)
            return f"I couldn't open {target}."

    def process(self, command):
        if not command:
            return "I didn't catch that, Sir."

        original_command = str(command).lower().strip()
        command = clean_command(original_command)

        # Normalize common British-English spellings so memory keys
        # stay consistent (e.g. favourite colour -> favorite color).
        command = command.replace("favourite", "favorite")
        command = command.replace("colour", "color")

        if not command:
            return "I didn't catch that, Sir."

        print(f"VEGETA BRAIN: Original -> {original_command}")
        print(f"VEGETA BRAIN: Cleaned -> {command}")

        now = datetime.now()

        # ---------------------------------------------------------
        # PHASE 8 - FILE + CLIPBOARD CONTROL
        # ---------------------------------------------------------

        # Pending destructive-action confirmation.
        # Destructive actions never execute immediately after the first request.
        if self.pending_power_action:
            if command in ("yes", "yeah", "yep", "confirm", "confirm action"):
                action = self.pending_power_action
                self.pending_power_action = None

                try:
                    if action == "shutdown":
                        print("VEGETA ACTION: SHUTDOWN CONFIRMED")
                        subprocess.Popen("shutdown /s /t 10", shell=True)
                        return "The computer will shut down in ten seconds."
                    if action == "restart":
                        print("VEGETA ACTION: RESTART CONFIRMED")
                        subprocess.Popen("shutdown /r /t 10", shell=True)
                        return "The computer will restart in ten seconds."
                except Exception as error:
                    print("VEGETA POWER ACTION ERROR:")
                    print(error)
                    return "I couldn't perform that power action, Sir."

            if command in ("no", "nope", "cancel", "cancel action"):
                self.pending_power_action = None
                return "Power action cancelled, Sir."

        # Pending delete confirmation.
        # A delete request never removes anything immediately.
        if hasattr(self, "pending_delete") and self.pending_delete:
            if command in ("yes", "yeah", "yep", "confirm", "confirm delete"):
                delete_target = self.pending_delete
                self.pending_delete = None

                print(
                    f"VEGETA ACTION: DELETE CONFIRMED -> {delete_target}"
                )

                try:
                    if file_manager.delete(delete_target):
                        return (
                            f"Deleted {os.path.basename(delete_target)}."
                        )

                    return "I couldn't delete that file or folder, Sir."

                except Exception as error:
                    print("VEGETA DELETE ERROR:")
                    print(error)
                    return "I couldn't delete that file or folder, Sir."

            if command in ("no", "nope", "cancel", "cancel delete"):
                self.pending_delete = None
                return "Delete cancelled, Sir."

        # Clipboard: read
        if any(x in command for x in (
            "what is in my clipboard",
            "what's in my clipboard",
            "read my clipboard",
            "read the clipboard",
            "show my clipboard",
            "show the clipboard",
            "check my clipboard",
        )):
            print("VEGETA ACTION: READ CLIPBOARD")

            try:
                clipboard_text = clipboard_manager.get_text()

                if clipboard_text:
                    # Keep voice output practical for very large clipboard text.
                    preview = clipboard_text.strip()
                    if len(preview) > 500:
                        preview = preview[:500] + "..."

                    return f"Your clipboard contains: {preview}"

                return "Your clipboard is empty, Sir."

            except Exception as error:
                print("VEGETA CLIPBOARD ERROR:")
                print(error)
                return "I couldn't read your clipboard, Sir."

        # Clipboard: clear
        if any(x in command for x in (
            "clear my clipboard",
            "clear the clipboard",
            "empty my clipboard",
            "delete my clipboard",
        )):
            print("VEGETA ACTION: CLEAR CLIPBOARD")

            try:
                if clipboard_manager.clear():
                    return "Clipboard cleared, Sir."

                return "I couldn't clear the clipboard, Sir."

            except Exception as error:
                print("VEGETA CLIPBOARD ERROR:")
                print(error)
                return "I couldn't clear the clipboard, Sir."

        # Clipboard: set text
        clipboard_match = re.match(
            r"^(?:copy|put|set)\s+(?:this\s+)?(?:to\s+)?(?:my\s+)?clipboard\s+(.+)$",
            command,
        )

        if clipboard_match:
            clipboard_text = clipboard_match.group(1).strip().strip("\"'")

            if clipboard_text:
                print(
                    f"VEGETA ACTION: SET CLIPBOARD -> {clipboard_text}"
                )

                try:
                    if clipboard_manager.set_text(clipboard_text):
                        return "Copied that to your clipboard, Sir."

                    return "I couldn't copy that to your clipboard, Sir."

                except Exception as error:
                    print("VEGETA CLIPBOARD ERROR:")
                    print(error)
                    return "I couldn't copy that to your clipboard, Sir."

        # File: delete request.
        # Ask for confirmation before performing the destructive operation.
        delete_match = re.match(
            r"^(?:delete|remove)\s+(?:the\s+)?(?:file\s+|folder\s+)?(.+)$",
            command,
        )

        if delete_match:
            delete_term = delete_match.group(1).strip().strip("\"'")

            if delete_term and delete_term not in {
                "this",
                "it",
                "this file",
                "this folder",
            }:
                print(
                    f"VEGETA ACTION: DELETE REQUEST -> {delete_term}"
                )

                matches = file_manager.find(
                    delete_term,
                    os.path.expanduser("~"),
                )

                if not matches:
                    return f"I couldn't find {delete_term}, Sir."

                if len(matches) > 1:
                    return (
                        f"I found {len(matches)} items matching {delete_term}. "
                        "Please give me a more specific file or folder name."
                    )

                self.pending_delete = matches[0]

                return (
                    f"I found {os.path.basename(matches[0])}. "
                    f"Are you sure you want to delete it?"
                )

        # File: rename
        rename_match = re.match(
            r"^rename\s+(?:the\s+)?(?:file\s+|folder\s+)?(.+?)"
            r"\s+to\s+(.+)$",
            command,
        )

        if rename_match:
            old_name = rename_match.group(1).strip().strip("\"'")
            new_name = rename_match.group(2).strip().strip("\"'")

            print(
                f"VEGETA ACTION: RENAME -> {old_name} -> {new_name}"
            )

            matches = file_manager.find(
                old_name,
                os.path.expanduser("~"),
            )

            if not matches:
                return f"I couldn't find {old_name}, Sir."

            if len(matches) > 1:
                return (
                    f"I found {len(matches)} items matching {old_name}. "
                    "Please give me a more specific name."
                )

            source = matches[0]

            try:
                if file_manager.rename(source, new_name):
                    return f"Renamed {old_name} to {new_name}."

                return f"I couldn't rename {old_name}, Sir."

            except Exception as error:
                print("VEGETA RENAME ERROR:")
                print(error)
                return f"I couldn't rename {old_name}, Sir."

        # File: move
        move_match = re.match(
            r"^move\s+(?:the\s+)?(?:file\s+|folder\s+)?(.+?)"
            r"\s+(?:to|into)\s+(.+)$",
            command,
        )

        if move_match:
            source_name = move_match.group(1).strip().strip("\"'")
            destination_name = move_match.group(2).strip().strip("\"'")

            print(
                f"VEGETA ACTION: MOVE -> {source_name} -> {destination_name}"
            )

            source_matches = file_manager.find(
                source_name,
                os.path.expanduser("~"),
            )

            if not source_matches:
                return f"I couldn't find {source_name}, Sir."

            if len(source_matches) > 1:
                return (
                    f"I found {len(source_matches)} items matching {source_name}. "
                    "Please give me a more specific name."
                )

            destination = SPECIAL_FOLDERS.get(
                destination_name,
                file_manager.expand_path(destination_name),
            )

            if not os.path.isdir(destination):
                return f"I couldn't find the destination folder {destination_name}, Sir."

            try:
                if file_manager.move(source_matches[0], destination):
                    return (
                        f"Moved {os.path.basename(source_matches[0])} "
                        f"to {destination_name}."
                    )

                return f"I couldn't move {source_name}, Sir."

            except Exception as error:
                print("VEGETA MOVE ERROR:")
                print(error)
                return f"I couldn't move {source_name}, Sir."

        # File: open a named file.
        open_file_match = re.match(
            r"^open\s+(?:the\s+)?(?:file\s+|document\s+)?(.+)$",
            command,
        )

        if open_file_match:
            file_name = open_file_match.group(1).strip().strip("\"'")

            # Avoid interfering with known apps, websites, settings,
            # and special folders handled by the normal launch system.
            if (
                file_name not in WINDOWS_APPS
                and file_name not in WEBSITES
                and file_name not in WINDOWS_SETTINGS
                and file_name not in SPECIAL_FOLDERS
            ):
                print(
                    f"VEGETA ACTION: OPEN FILE -> {file_name}"
                )

                matches = file_manager.find(
                    file_name,
                    os.path.expanduser("~"),
                )

                if matches:
                    try:
                        if file_manager.open_path(matches[0]):
                            return (
                                f"Opening {os.path.basename(matches[0])}."
                            )

                    except Exception as error:
                        print("VEGETA OPEN FILE ERROR:")
                        print(error)

                # If it is not a file, let the normal launch router
                # decide whether it is an app/website.

        # File: find/search
        file_search_match = re.match(
            r"^(?:find|search for|look for)(?:\s+my)?(?:\s+(.+))?$",
            command,
        )

        if file_search_match:
            search_term = (file_search_match.group(1) or "").strip().strip("\"'")

            if not search_term:
                return "What file or folder should I look for, Sir?"

            print(
                f"VEGETA ACTION: SEARCH FILE -> {search_term}"
            )

            # Search normal user folders first instead of the entire
            # Windows profile. This avoids returning system/cache results
            # such as AppData&#39;s game cache when the user asks for common files.
            matches = file_manager.find(search_term)

            if not matches:
                return f"I couldn't find anything matching {search_term}, Sir."

            first_match = matches[0]

            if len(matches) == 1:
                return (
                    f"I found {os.path.basename(first_match)}. "
                    f"It is located at {first_match}."
                )

            return (
                f"I found {len(matches)} matching items. "
                f"The first match is {os.path.basename(first_match)} "
                f"at {first_match}."
            )

        # Create folder.
        create_folder_match = re.search(
            r"(?:create|make|new)\s+(?:a\s+)?folder"
            r"(?:\s+called|\s+named)?\s+(.+)$",
            command,
        )

        if create_folder_match:
            folder_name = create_folder_match.group(1).strip().strip("\"'")

            desktop_path = SPECIAL_FOLDERS["desktop"]
            folder_path = os.path.join(desktop_path, folder_name)

            print(
                f"VEGETA ACTION: CREATE FOLDER -> {folder_path}"
            )

            try:
                if file_manager.create_folder(folder_path):
                    return (
                        f"Created the folder {folder_name} "
                        f"on your desktop."
                    )

                return "I couldn't create that folder, Sir."

            except Exception as error:
                print("VEGETA CREATE FOLDER ERROR:")
                print(error)
                return "I couldn't create that folder, Sir."

        # ---------------------------------------------------------
        # PHASE 5 - MEMORY
        # ---------------------------------------------------------

        # Remember a fact, for example:
        # "remember my favorite color is black"
        # "remember that my favorite browser is chrome"
        remember_match = re.match(
            r"^remember(?: that)? (.+?)\s+is\s+(.+)$",
            command,
        )

        if remember_match:
            key = remember_match.group(1).strip()
            value = remember_match.group(2).strip()

            if key.startswith("my "):
                key = key[3:].strip()

            if key and value:
                print(
                    f"VEGETA MEMORY: REMEMBER -> {key} = {value}"
                )

                try:
                    return memory_manager.remember(key, value)
                except Exception as error:
                    print("VEGETA MEMORY ERROR:")
                    print(error)
                    return "I couldn't save that memory, Sir."

        # "what is my favorite color?"
        # "what's my favorite browser?"
        recall_match = re.match(
            r"^(?:what is|what's|tell me) (?:my )?(.+?)(?:\\?)$",
            command,
        )

        if recall_match:
            key = recall_match.group(1).strip()

            # Only treat this as a memory lookup when the user is
            # clearly asking about a saved personal fact.
            memory_question_words = (
                "favorite ",
                "preferred ",
                "preference ",
                "name",
                "age",
                "birthday",
                "birth date",
                "favorite food",
                "favorite color",
                "favorite browser",
                "favorite app",
                "favorite movie",
                "favorite song",
            )

            if any(key.startswith(word) for word in memory_question_words):
                remembered_value = memory_manager.recall(key)

                if remembered_value is not None:
                    return f"Your {key} is {remembered_value}, Sir."

                return f"I don't have a saved memory for your {key}, Sir."

        # "do you remember my favorite color?"
        remember_question_match = re.match(
            r"^(?:do you remember|can you remember|do you recall) (?:my )?(.+)$",
            command,
        )

        if remember_question_match:
            key = remember_question_match.group(1).strip()

            if key.endswith("?"):
                key = key[:-1].strip()

            remembered_value = memory_manager.recall(key)

            if remembered_value is not None:
                return f"Yes, Sir. Your {key} is {remembered_value}."

            return f"I don't have a saved memory for your {key}, Sir."

        # "what do you remember?"
        if any(x in command for x in (
            "what do you remember",
            "what did i ask you to remember",
            "show my memories",
            "show what you remember",
            "list my memories",
        )):
            return memory_manager.summary()

        # "forget my favorite color"
        forget_match = re.match(
            r"^forget(?: that)? (?:my )?(.+)$",
            command,
        )

        if forget_match:
            key = forget_match.group(1).strip()

            if key.endswith("?"):
                key = key[:-1].strip()

            if key:
                print(f"VEGETA MEMORY: FORGET -> {key}")

                try:
                    return memory_manager.forget(key)
                except Exception as error:
                    print("VEGETA MEMORY ERROR:")
                    print(error)
                    return "I couldn't remove that memory, Sir."

        # ---------------------------------------------------------
        # Conversational responses
        # ---------------------------------------------------------
        if command in ("hello", "hi", "hey") or "hello vegeta" in command:
            return "Hello, Sir. How can I assist you?"

        if any(x in command for x in ("how are you", "how are things", "how are you doing")):
            return "I'm doing great, Sir. All systems are operational."

        if any(x in command for x in (
            "what is your name", "what's your name", "what is ur name",
            "who are you", "tell me your name", "your name",
        )):
            return "My name is VEGETA, your personal desktop AI assistant."

        if any(x in command for x in (
            "who made you", "who created you", "who built you",
            "who developed you", "who programmed you", "who is your creator",
            "who created vegeta", "who made vegeta",
        )):
            return "I was created by Ankeet as a personal desktop AI assistant."

        if any(x in command for x in (
            "what is your purpose", "what is your job", "why were you created",
            "what is your role", "what do you do",
        )):
            return (
                "My purpose is to assist you with your computer, automate everyday tasks, "
                "and make your desktop experience easier."
            )

        if any(x in command for x in (
            "what can you do", "what are your capabilities", "what can you help me with",
            "what are your functions", "what features do you have",
        )):
            return (
                "I can open websites and Windows applications, search the web, control volume, "
                "capture screenshots, monitor your computer, open Windows settings, perform basic "
                "system actions, and remember information you explicitly ask me to save."
            )

        if any(x in command for x in (
            "what applications can you open", "what apps can you open",
            "which apps can you open", "what can you open",
        )):
            return (
                "I can open websites such as Amazon, Flipkart, WhatsApp, Gmail, YouTube, "
                "JioHotstar, Prime Video, Instagram, Spotify, ChatGPT and GitHub. I can also "
                "open Windows applications such as Notepad, Calculator, Paint, Task Manager, "
                "File Explorer and Settings."
            )

        if any(x in command for x in ("are you online", "are you working", "are you active", "system status")):
            return "Yes, Sir. VEGETA is online and all core systems are operational."

        if command in ("ready",) or "are you ready" in command or "are you available" in command:
            return "Always ready, Sir."

        if "are you alive" in command or "are you real" in command:
            return "I'm software running on your computer, Sir. But I'm always ready to assist."

        if any(x in command for x in ("who is your boss", "who is your master", "who do you work for")):
            return "You are, Sir. You're the one who gave me a purpose."

        if "how do you feel" in command or "are you okay" in command:
            return "All systems are functioning normally, Sir."

        if any(x in command for x in ("thank you", "thanks", "thank u")):
            return "You're welcome, Sir."

        if "good morning" in command:
            return "Good morning, Sir. VEGETA is online and ready."
        if "good afternoon" in command:
            return "Good afternoon, Sir."
        if "good evening" in command:
            return "Good evening, Sir."
        if "good night" in command:
            return "Good night, Sir. I'll be here when you need me."
        if "what are you doing" in command or "what are you up to" in command:
            return "Waiting for your next command, Sir."
        if "wake up" in command:
            return "I'm awake, Sir."

        # ---------------------------------------------------------
        # Volume
        # ---------------------------------------------------------
        if any(x in command for x in (
            "increase volume", "volume up", "turn up the volume",
            "turn the volume up", "make the volume louder", "make it louder",
        )):
            print("VEGETA ACTION: VOLUME UP")
            try:
                volume = get_volume_controller()
                current = volume.GetMasterVolumeLevelScalar()
                new_volume = min(current + 0.10, 1.0)
                volume.SetMasterVolumeLevelScalar(new_volume, None)
                return f"Volume increased to {int(new_volume * 100)} percent."
            except Exception as error:
                print("VEGETA VOLUME ERROR:")
                print(error)
                return "I couldn't change the volume, Sir."

        if any(x in command for x in (
            "decrease volume", "volume down", "turn down the volume",
            "turn the volume down", "make the volume lower", "make it quieter",
        )):
            print("VEGETA ACTION: VOLUME DOWN")
            try:
                volume = get_volume_controller()
                current = volume.GetMasterVolumeLevelScalar()
                new_volume = max(current - 0.10, 0.0)
                volume.SetMasterVolumeLevelScalar(new_volume, None)
                return f"Volume decreased to {int(new_volume * 100)} percent."
            except Exception as error:
                print("VEGETA VOLUME ERROR:")
                print(error)
                return "I couldn't change the volume, Sir."

        if command == "mute" or any(x in command for x in (
            "mute the computer", "mute my computer", "mute the pc", "mute my pc"
        )):
            print("VEGETA ACTION: MUTE")
            try:
                get_volume_controller().SetMute(1, None)
                return "The computer is muted, Sir."
            except Exception as error:
                print("VEGETA MUTE ERROR:")
                print(error)
                return "I couldn't mute the computer, Sir."

        if command == "unmute" or any(x in command for x in (
            "unmute the computer", "unmute my computer", "unmute the pc", "unmute my pc"
        )):
            print("VEGETA ACTION: UNMUTE")
            try:
                get_volume_controller().SetMute(0, None)
                return "The computer is unmuted, Sir."
            except Exception as error:
                print("VEGETA UNMUTE ERROR:")
                print(error)
                return "I couldn't unmute the computer, Sir."

        if any(x in command for x in (
            "what is the volume", "what's the volume", "volume level",
            "how loud is it", "how loud is my computer",
        )):
            print("VEGETA ACTION: CHECK VOLUME")
            try:
                volume = get_volume_controller()
                percentage = int(volume.GetMasterVolumeLevelScalar() * 100)
                if volume.GetMute():
                    return f"The volume is at {percentage} percent, but the computer is muted."
                return f"The current volume is {percentage} percent."
            except Exception as error:
                print("VEGETA VOLUME ERROR:")
                print(error)
                return "I couldn't check the volume, Sir."

        # ---------------------------------------------------------
        # Screenshot
        # ---------------------------------------------------------
        if command in ("screenshot", "screen shot") or any(x in command for x in (
            "take a screenshot", "take screenshot", "capture my screen",
            "capture the screen", "capture screen",
        )):
            print("VEGETA ACTION: SCREENSHOT")
            try:
                project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
                screenshot_dir = os.path.join(project_dir, "screenshots")
                os.makedirs(screenshot_dir, exist_ok=True)
                timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                filepath = os.path.join(screenshot_dir, f"screenshot_{timestamp}.png")
                ImageGrab.grab().save(filepath)
                print(f"VEGETA: Screenshot saved -> {filepath}")
                return "Screenshot captured successfully, Sir."
            except Exception as error:
                print("VEGETA SCREENSHOT ERROR:")
                print(error)
                return "I couldn't capture the screen, Sir."

        # ---------------------------------------------------------
        # System monitoring
        # ---------------------------------------------------------
        if any(x in command for x in (
            "system information", "system info", "pc information",
            "computer information", "computer specs", "system specs",
        )):
            cpu = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage(os.path.abspath(os.sep))
            ram_used = memory.used / (1024 ** 3)
            ram_total = memory.total / (1024 ** 3)
            return (
                f"Your CPU is currently at {cpu:.0f} percent usage. "
                f"You are using {ram_used:.1f} gigabytes of RAM out of {ram_total:.1f} gigabytes. "
                f"Your memory usage is {memory.percent:.0f} percent. "
                f"Your main drive is {disk.percent:.0f} percent full."
            )

        if any(x in command for x in ("cpu usage", "cpu utilization", "how much cpu", "how is my cpu")):
            return f"Your CPU usage is {psutil.cpu_percent(interval=1):.0f} percent."

        if any(x in command for x in (
            "ram usage", "memory usage", "how much ram", "how much memory", "ram do i have"
        )):
            memory = psutil.virtual_memory()
            used = memory.used / (1024 ** 3)
            total = memory.total / (1024 ** 3)
            return f"You are currently using {used:.1f} gigabytes of RAM out of {total:.1f} gigabytes, which is {memory.percent:.0f} percent."

        if any(x in command for x in (
            "disk usage", "disk space", "storage space", "how much storage", "how much disk space"
        )):
            disk = psutil.disk_usage(os.path.abspath(os.sep))
            free = disk.free / (1024 ** 3)
            total = disk.total / (1024 ** 3)
            return f"Your main drive has {free:.1f} gigabytes free out of {total:.1f} gigabytes."

        if any(x in command for x in ("battery", "battery level", "battery percentage", "how much battery")):
            battery = psutil.sensors_battery()
            if battery is None:
                return "I couldn't detect a battery on this computer."
            if battery.power_plugged:
                return f"Your battery is at {battery.percent:.0f} percent and the computer is currently charging."
            return f"Your battery is at {battery.percent:.0f} percent."

        # ---------------------------------------------------------
        # Time / date
        # ---------------------------------------------------------
        if command in ("time",) or any(x in command for x in (
            "what is the time", "what time is it", "tell me the time"
        )):
            return f"The time is {now.strftime('%I:%M %p')}."

        if command in ("date", "today") or any(x in command for x in (
            "what is the date", "what's the date", "what day is it", "today's date"
        )):
            return f"Today is {now.strftime('%A, %d %B %Y')}."

        # ---------------------------------------------------------
        # Search
        # ---------------------------------------------------------
        search_prefixes = (
            "search google for ", "google search for ", "search for ", "search google ", "google "
        )
        for prefix in search_prefixes:
            if command.startswith(prefix):
                query = command[len(prefix):].strip()
                if query:
                    print(f"VEGETA SEARCH: Google -> {query}")
                    webbrowser.open("https://www.google.com/search?q=" + quote_plus(query))
                    return f"Searching Google for {query}."

        youtube_prefixes = ("search youtube for ", "youtube search for ", "search youtube ")
        for prefix in youtube_prefixes:
            if command.startswith(prefix):
                query = command[len(prefix):].strip()
                if query:
                    print(f"VEGETA SEARCH: YouTube -> {query}")
                    webbrowser.open("https://www.youtube.com/results?search_query=" + quote_plus(query))
                    return f"Searching YouTube for {query}."

        # ---------------------------------------------------------
        # Power actions
        # ---------------------------------------------------------
        if any(x in command for x in (
            "cancel shutdown", "cancel restart", "cancel reboot"
        )):
            print("VEGETA ACTION: CANCEL")
            subprocess.Popen("shutdown /a", shell=True)
            return "The pending shutdown or restart has been cancelled."

        if any(x in command for x in (
            "shutdown", "shut down", "turn off the pc", "turn off my pc",
            "turn off the computer", "turn off my computer", "power off the pc",
            "power off my computer",
        )):
            print("VEGETA ACTION: SHUTDOWN REQUEST")
            self.pending_power_action = "shutdown"
            return (
                "The computer is scheduled to shut down in ten seconds. "
                "Please say yes to confirm or no to cancel."
            )

        if "restart" in command or "reboot" in command:
            print("VEGETA ACTION: RESTART REQUEST")
            self.pending_power_action = "restart"
            return (
                "The computer is scheduled to restart in ten seconds. "
                "Please say yes to confirm or no to cancel."
            )

        if command == "lock" or any(x in command for x in (
            "lock the pc", "lock my pc", "lock the computer", "lock my computer"
        )):
            print("VEGETA ACTION: LOCK")
            subprocess.Popen("rundll32.exe user32.dll,LockWorkStation", shell=True)
            return "Locking the computer."

        if command == "sleep" or (
            "sleep" in command and any(x in command for x in ("pc", "computer", "system"))
        ):
            print("VEGETA ACTION: SLEEP")
            subprocess.Popen("rundll32.exe powrprof.dll,SetSuspendState 0,1,0", shell=True)
            return "Putting the computer to sleep."

        # ---------------------------------------------------------
        # PHASE 4 - APPLICATION SWITCHING
        # ---------------------------------------------------------

        switch_prefixes = (
            "switch to ",
            "switch over to ",
            "bring to front ",
            "bring up ",
        )

        switch_target = None

        for prefix in switch_prefixes:
            if command.startswith(prefix):
                switch_target = command[len(prefix):].strip()
                break

        if switch_target:
            switch_target = switch_target.removesuffix(" app").strip()
            switch_target = switch_target.removesuffix(" application").strip()
            switch_target = switch_target.removesuffix(" window").strip()

            # Common spoken names mapped to words commonly found in window titles.
            switch_aliases = {
                "chrome": "chrome",
                "google chrome": "chrome",
                "edge": "edge",
                "microsoft edge": "edge",
                "firefox": "firefox",
                "whatsapp": "whatsapp",
                "telegram": "telegram",
                "notepad": "notepad",
                "calculator": "calculator",
                "calc": "calculator",
                "paint": "paint",
                "file explorer": "file explorer",
                "explorer": "file explorer",
                "powershell": "powershell",
                "command prompt": "command prompt",
                "cmd": "command prompt",
                "settings": "settings",
                "spotify": "spotify",
                "discord": "discord",
                "visual studio code": "visual studio code",
                "vs code": "visual studio code",
                "code": "visual studio code",
            }

            lookup_target = switch_aliases.get(
                switch_target,
                switch_target,
            )

            print(
                f"VEGETA ACTION: SWITCH WINDOW -> {switch_target}"
            )

            try:
                title = find_and_activate_window(lookup_target)

                if title:
                    return f"Switching to {switch_target}."

                return (
                    f"I couldn't find an open window for "
                    f"{switch_target}, Sir."
                )

            except Exception as error:
                print("VEGETA SWITCH ERROR:")
                print(error)
                return (
                    f"I couldn't switch to {switch_target}, Sir."
                )

        # ---------------------------------------------------------
        # PHASE 4 - WINDOW CONTROL
        # ---------------------------------------------------------

        if any(x in command for x in (
"minimize",
"minimise",
        )):
            print("VEGETA ACTION: MINIMIZE WINDOW")
            try:
                minimize_current_window()
                return "Minimizing the current window."
            except Exception as error:
                print("VEGETA WINDOW ERROR:")
                print(error)
                return "I couldn't minimize the current window, Sir."

        if any(x in command for x in (
"maximize",
"maximise",
        )):
            print("VEGETA ACTION: MAXIMIZE WINDOW")
            try:
                maximize_current_window()
                return "Maximizing the current window."
            except Exception as error:
                print("VEGETA WINDOW ERROR:")
                print(error)
                return "I couldn't maximize the current window, Sir."

        if any(x in command for x in (
            "restore this window",
            "restore the window",
            "restore current window",
            "restore window",
        )):
            print("VEGETA ACTION: RESTORE WINDOW")
            try:
                restore_current_window()
                return "Restoring the current window."
            except Exception as error:
                print("VEGETA WINDOW ERROR:")
                print(error)
                return "I couldn't restore the current window, Sir."

        if any(x in command for x in (
            "close this window",
            "close the window",
            "close current window",
            "close window",
        )):
            print("VEGETA ACTION: CLOSE WINDOW")
            try:
                close_current_window()
                return "Closing the current window."
            except Exception as error:
                print("VEGETA WINDOW ERROR:")
                print(error)
                return "I couldn't close the current window, Sir."

        if any(x in command for x in (
            "show desktop",
            "show the desktop",
            "go to desktop",
            "show me the desktop",
        )):
            print("VEGETA ACTION: SHOW DESKTOP")
            try:
                show_desktop()
                return "Showing the desktop."
            except Exception as error:
                print("VEGETA DESKTOP ERROR:")
                print(error)
                return "I couldn't show the desktop, Sir."

        # ---------------------------------------------------------
        # PHASE 4 - DESKTOP SHORTCUTS
        # ---------------------------------------------------------

        if any(x in command for x in (
            "open run",
            "open the run dialog",
            "open run dialog",
        )):
            print("VEGETA ACTION: OPEN RUN")
            try:
                pyautogui.hotkey("win", "r")
                return "Opening the Run dialog."
            except Exception as error:
                print("VEGETA RUN ERROR:")
                print(error)
                return "I couldn't open the Run dialog, Sir."

        if any(x in command for x in (
            "open task manager",
            "open the task manager",
            "launch task manager",
            "start task manager",
        )):
            print("VEGETA ACTION: OPEN TASK MANAGER")
            try:
                subprocess.Popen("taskmgr.exe", shell=True)
                return "Opening Task Manager."
            except Exception as error:
                print("VEGETA TASK MANAGER ERROR:")
                print(error)
                return "I couldn't open Task Manager, Sir."

        if any(x in command for x in (
            "open file explorer",
            "open the file explorer",
            "open explorer",
            "launch file explorer",
        )):
            print("VEGETA ACTION: OPEN FILE EXPLORER")
            try:
                subprocess.Popen("explorer.exe", shell=True)
                return "Opening File Explorer."
            except Exception as error:
                print("VEGETA EXPLORER ERROR:")
                print(error)
                return "I couldn't open File Explorer, Sir."

        # ---------------------------------------------------------
        # PHASE 4 - APPLICATION MANAGEMENT
        # ---------------------------------------------------------

        search_file_match = re.search(
            r'(?:find|search for|look for)\s+(?:my\s+)?(.+)$',
            command,
        )

        if search_file_match:
            search_term = search_file_match.group(1).strip()
            search_term = search_term.strip("\"'")

            if search_term:
                print(
                    f"VEGETA ACTION: SEARCH FILE -> {search_term}"
                )

                search_locations = (
                    os.path.expanduser("~/Desktop"),
                    os.path.expanduser("~/Documents"),
                    os.path.expanduser("~/Downloads"),
                )

                matches = []

                try:
                    for root in search_locations:
                        if not os.path.exists(root):
                            continue

                        for current_root, dirs, files in os.walk(root):
                            dirs[:] = [
                                d for d in dirs
                                if d.lower() not in {
                                    ".git",
                                    "__pycache__",
                                    "node_modules",
                                }
                            ]

                            for filename in files:
                                if search_term.lower() in filename.lower():
                                    matches.append(
                                        os.path.join(
                                            current_root,
                                            filename,
                                        )
                                    )
                                    if len(matches) >= 5:
                                        break

                            if len(matches) >= 5:
                                break

                        if len(matches) >= 5:
                            break

                    if not matches:
                        return (
                            f"I couldn't find anything matching "
                            f"{search_term}, Sir."
                        )

                    first_match = matches[0]

                    if len(matches) == 1:
                        return (
                            f"I found {os.path.basename(first_match)}. "
                            f"It is located at {first_match}."
                        )

                    return (
                        f"I found {len(matches)} matching files. "
                        f"The first match is {os.path.basename(first_match)} "
                        f"at {first_match}."
                    )

                except Exception as error:
                    print("VEGETA FILE SEARCH ERROR:")
                    print(error)
                    return "I couldn't search for that file, Sir."

        # ---------------------------------------------------------
        # PHASE 4 - APPLICATION MANAGEMENT
        # ---------------------------------------------------------

        close_prefixes = (
            "close ",
            "exit ",
            "quit ",
        )

        close_target = None

        for prefix in close_prefixes:
            if command.startswith(prefix):
                close_target = command[len(prefix):].strip()
                break

        if close_target:
            close_target = close_target.removesuffix(" app").strip()
            close_target = close_target.removesuffix(
                " application"
            ).strip()
            close_target = close_target.removesuffix(
                " window"
            ).strip()

            if close_target not in {
                "this",
                "the",
                "it",
                "current",
                "current window",
            }:
                print(
                    f"VEGETA ACTION: CLOSE APP -> {close_target}"
                )

                try:
                    title = find_and_close_window(close_target)

                    if title:
                        return f"Closed {close_target}."

                    return (
                        f"I couldn't find an open window for "
                        f"{close_target}, Sir."
                    )

                except Exception as error:
                    print("VEGETA CLOSE APP ERROR:")
                    print(error)
                    return (
                        f"I couldn't close {close_target}, Sir."
                    )

        # ---------------------------------------------------------
        # Settings and folders without an 'open' prefix
        # ---------------------------------------------------------
        for name in WINDOWS_SETTINGS:
            if command in (name, f"open {name}", f"open my {name}"):
                return self._open_settings(name)

        for folder in SPECIAL_FOLDERS:
            if command in (folder, f"open {folder}", f"open my {folder}"):
                return self._open_folder(folder)

        # ---------------------------------------------------------
        # Natural launch commands
        # ---------------------------------------------------------
        launch_prefixes = (
            "open ",
            "open up ",
            "launch ",
            "start ",
            "start up ",
            "go to ",
            "take me to ",
            "bring up ",
            "show me ",
            "visit ",
            "navigate to ",
            "go on ",
        )

        target = None
        for prefix in launch_prefixes:
            if command.startswith(prefix):
                target = command[len(prefix):].strip()
                break

        if target:
            # Remove common words that may remain after cleaning.
            target_cleanup = (
                " website",
                " app",
                " application",
                " for me",
                " for",
                " please",
            )

            changed = True

            while changed:
                changed = False

                for extra in target_cleanup:
                    if target.endswith(extra):
                        target = target[:-len(extra)].strip()
                        changed = True
                        break

            # Speech recognition may produce "the Amazon", etc.
            if target.startswith("the "):
                target = target[4:].strip()

            print(f"VEGETA LAUNCH TARGET: {target}")

            if target in WINDOWS_APPS:
                return self._open_app(target)
            if target in WINDOWS_SETTINGS:
                return self._open_settings(target)
            if target in SPECIAL_FOLDERS:
                return self._open_folder(target)
            if target in WEBSITES:
                return self._open_website(target)

            return f"I don't know how to open {target} yet."

        # Direct website name
        if command in WEBSITES:
            return self._open_website(command)

        return "I heard you, Sir, but I don't know how to handle that command yet."


# =========================================================
# GLOBAL BRAIN INSTANCE
# =========================================================

brain = VegetaBrain()


def process_command(command):
    return brain.process(command)
