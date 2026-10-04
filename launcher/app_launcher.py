import subprocess
import time


class AppLauncher:
    """
    Launches Windows applications for VEGETA.
    """

    def launch(self, command, wait_time=2):
        """
        Launch an application using a Windows command.
        """

        try:
            subprocess.Popen(
                command,
                shell=True
            )

            print(
                f"VEGETA LAUNCHER: Launching -> {command}"
            )

            time.sleep(wait_time)

            return True

        except Exception as error:
            print(
                f"VEGETA LAUNCHER: Launch failed -> {error}"
            )
            return False

    def launch_and_focus(
        self,
        command,
        window_name,
        wait_time=2
    ):
        """
        Launch an application and then focus its window.
        """

        launched = self.launch(
            command,
            wait_time
        )

        if not launched:
            return False

        # Import here to avoid unnecessary circular imports.
        from automation.window import window_controller

        focused = window_controller.focus_window(
            window_name
        )

        return focused


app_launcher = AppLauncher()