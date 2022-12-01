class Block:
    """The class representing a block in which read/written records are stored."""
    def __init__(self):
        """
        Initializes Block object that is initially empty.
        """
        self.current_size = 0
        self.records = []

    def serialize(self):
        """
        Returns a serialized block consisting of records separated by newline.

        :return: Serialized block.
        :rtype: str
        """
        serialized_records = [record.serialize() for record in self.records]
        serialized_block = "\n".join(serialized_records)

        return serialized_block

    def clear(self):
        """
        Clears a block.
        """
        self.current_size = 0
        self.records.clear()

    def is_empty(self):
        """
        Checks if a block is empty.

        :return: True if a block is empty, otherwise false.
        :rtype: bool
        """
        return self.current_size == 0
