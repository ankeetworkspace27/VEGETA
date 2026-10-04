class ContextManager:
    """
    Stores short-term information for the current VEGETA session.
    """

    def __init__(self):
        self.last_command = None
        self.last_response = None
        self.last_action = None
        self.last_target = None

        # Stores recent conversation messages.
        self.history = []

    def update(
        self,
        command=None,
        response=None,
        action=None,
        target=None,
    ):
        """
        Update the current session context.
        """

        if command is not None:
            self.last_command = command

        if response is not None:
            self.last_response = response

        if action is not None:
            self.last_action = action

        if target is not None:
            self.last_target = target

    def add_history(self, speaker, message):
        """
        Add a message to the current conversation history.
        """

        self.history.append({
            "speaker": speaker,
            "message": message,
        })

    def get_history(self):
        """
        Return the complete conversation history.
        """

        return self.history

    def get_recent_history(self, limit=5):
        """
        Return the most recent conversation messages.
        """

        return self.history[-limit:]

    def get(self, name):
        """
        Retrieve one piece of context.
        """

        return getattr(self, name, None)

    def clear(self):
        """
        Clear the current session context.
        """

        self.last_command = None
        self.last_response = None
        self.last_action = None
        self.last_target = None
        self.history = []

    def summary(self):
        """
        Return the current session context.
        """

        return {
            "last_command": self.last_command,
            "last_response": self.last_response,
            "last_action": self.last_action,
            "last_target": self.last_target,
            "history": self.history,
        }


context_manager = ContextManager()