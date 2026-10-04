import time
import webbrowser


class WebLauncher:
    """
    Handles website launching for VEGETA.
    """

    def open(self, url, wait_time=2):
        """
        Open a website using the default browser.
        """

        try:
            webbrowser.open(url)

            print(
                f"VEGETA WEB: Opening -> {url}"
            )

            time.sleep(wait_time)

            return True

        except Exception as error:
            print(
                f"VEGETA WEB: Failed to open -> {error}"
            )
            print(error)

            return False


web_launcher = WebLauncher()