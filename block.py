
class Block:
    def __init__(self):
        self.current_size = 0
        self.records = []

    def serialize(self):
        serialized_records = [record.serialize() for record in self.records]
        serialized_block = "\n".join(serialized_records)

        return serialized_block

    def clear(self):
        self.current_size = 0
        self.records.clear()

    def is_empty(self):
        return self.current_size == 0
