import re
import time
from urllib.parse import quote_plus

from automation.keyboard import keyboard_controller
from automation.window import window_controller


class SearchManager:

    def __init__(self):
        # The active website/search target stays active until
        # the user explicitly exits search mode.
        self.target = None

    # ---------------------------------------------------------
    # Target
    # ---------------------------------------------------------

    def set_target(self, target):
        if target:
            self.target = target.lower().strip()
            print(f"VEGETA SEARCH: Target -> {self.target}")

    def clear_target(self):
        self.target = None
        print("VEGETA SEARCH: Target cleared.")

    def get_target(self):
        return self.target

    # ---------------------------------------------------------
    # Query cleanup
    # ---------------------------------------------------------

    def clean_query(self, query):
        """
        Remove only common search-command prefixes.

        IMPORTANT:
        This does NOT restrict what the user can search for.
        Everything else is kept as part of the query.
        """

        query = str(query).strip()

        if not query:
            return ""

        # Longest/more specific phrases first.
        prefixes = (
            "search for ",
            "search ",
            "look up ",
            "look for ",
            "find ",
            "watch ",
            "play ",
        )

        cleaned = query.lower()

        for prefix in prefixes:
            if cleaned.startswith(prefix):
                query = query[len(prefix):].strip()
                break

        return query

    # ---------------------------------------------------------
    # Exit search mode
    # ---------------------------------------------------------

    def is_exit_command(self, command):
        command = str(command).lower().strip()

        exit_phrases = (
            "exit search mode",
            "exit search",
            "stop searching",
            "stop search",
            "cancel search",
            "cancel searching",
            "leave search mode",
        )

        return command in exit_phrases

    # ---------------------------------------------------------
    # Chrome address bar
    # ---------------------------------------------------------

    def search_chrome(self, query):

        if not query:
            print("VEGETA SEARCH: Empty query.")
            return False

        if not window_controller.focus_chrome():
            print("VEGETA SEARCH: Chrome not found.")
            return False

        time.sleep(0.5)

        keyboard_controller.hotkey("ctrl", "l")
        time.sleep(0.2)

        keyboard_controller.type_text(query)
        time.sleep(0.2)

        keyboard_controller.press("enter")

        print(
            f"VEGETA SEARCH: Chrome search complete -> {query}"
        )

        return True

    # ---------------------------------------------------------
    # YouTube
    # ---------------------------------------------------------

    def search_youtube(self, query):

        if not query:
            print("VEGETA SEARCH: Empty query.")
            return False

        if not window_controller.focus_chrome():
            print("VEGETA SEARCH: Chrome not found.")
            return False

        time.sleep(0.5)

        encoded_query = quote_plus(query)

        youtube_url = (
            "https://www.youtube.com/results?search_query="
            + encoded_query
        )

        print(
            f"VEGETA SEARCH: YouTube -> {query}"
        )

        keyboard_controller.hotkey("ctrl", "l")
        time.sleep(0.2)

        keyboard_controller.type_text(youtube_url)
        time.sleep(0.2)

        keyboard_controller.press("enter")

        print(
            "VEGETA SEARCH: YouTube search complete."
        )

        return True

    # ---------------------------------------------------------
    # General search
    # ---------------------------------------------------------

    def search(self, query):

        if not query:
            print("VEGETA SEARCH: Empty query.")
            return False

        if not self.target:
            print("VEGETA SEARCH: No active target.")
            return False

        cleaned_query = self.clean_query(query)

        if not cleaned_query:
            print("VEGETA SEARCH: Empty query after cleanup.")
            return False

        print(
            f"VEGETA SEARCH: Searching '{cleaned_query}' "
            f"in {self.target}"
        )

        # YouTube
        if self.target == "youtube":
            return self.search_youtube(cleaned_query)

        # Everything else currently uses Chrome's address bar.
        return self.search_chrome(cleaned_query)


search_manager = SearchManager()
