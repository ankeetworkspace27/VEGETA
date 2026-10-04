from database.database import (
    delete_memory,
    get_all_memories,
    get_memory,
    save_memory,
)


class MemoryManager:
    """
    High-level interface for VEGETA's long-term memory.
    """

    def remember(self, key, value, category="general"):
        """
        Save a memory.
        """

        save_memory(key, value, category)

        return f"I'll remember that your {key} is {value}."

    def recall(self, key):
        """
        Retrieve one memory.
        """

        memory = get_memory(key)

        if memory:
            return memory["value"]

        return None

    def forget(self, key):
        """
        Delete one memory.
        """

        deleted = delete_memory(key)

        if deleted:
            return f"I've forgotten your {key}."

        return f"I don't have a memory for {key}."

    def all_memories(self):
        """
        Retrieve all saved memories.
        """

        return get_all_memories()

    def summary(self):
        """
        Create a readable summary of all memories.
        """

        memories = self.all_memories()

        if not memories:
            return "I don't have any saved memories yet."

        lines = ["Here's what I remember:"]

        for memory in memories:
            lines.append(
                f"- {memory['key']}: {memory['value']}"
            )

        return "\n".join(lines)


# Global memory manager used by VEGETA
memory_manager = MemoryManager()