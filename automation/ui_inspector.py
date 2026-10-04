from pywinauto import Desktop


class UIInspector:
    """
    Inspects visible Windows UI elements for VEGETA.
    """

    def get_windows(self):
        """
        Return currently visible top-level windows.
        """

        windows = Desktop(backend="uia").windows(
            visible_only=True
        )

        results = []

        for window in windows:
            try:
                title = window.window_text()

                if title:
                    results.append({
                        "title": title,
                        "control_type": window.element_info.control_type,
                    })

            except Exception:
                continue

        return results

    def inspect_window(self, title):
        """
        Inspect the controls inside a window whose title
        contains the supplied text.
        """

        windows = Desktop(backend="uia").windows(
            visible_only=True
        )

        title = title.lower()

        for window in windows:

            try:
                window_title = window.window_text()

                if title not in window_title.lower():
                    continue

                controls = []

                descendants = window.descendants()

                for control in descendants:

                    try:
                        control_title = control.window_text()
                        control_type = (
                            control.element_info.control_type
                        )

                        if control_title or control_type:

                            controls.append({
                                "title": control_title,
                                "control_type": control_type,
                            })

                    except Exception:
                        continue

                return controls

            except Exception:
                continue

        return []


ui_inspector = UIInspector()