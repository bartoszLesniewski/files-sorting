from block import Block
from constans import *
from diskOperationsHandler import DiskOperationsHandler
from record import Record


class Tape:
    def __init__(self, filename="tape1.txt"):
        self.block = Block()
        self.fileHandler = DiskOperationsHandler(filename)

    def add_record(self, record):
        if isinstance(record, str):
            serialized_record = record
            record = Record()
            record.deserialize(serialized_record)

        if self.block.current_size < MAX_BLOCK_SIZE:
            self.block.records.append(record)
            self.block.current_size += RECORD_SIZE
        else:
            self.save_block_to_file()
            self.add_record(record)

    def fetch_record(self):
        if self.block.is_empty() and self.fileHandler.eof:
            return None
        else:
            if self.block.is_empty():
                self.read_block_from_file()

            # after reading a block, it can still be empty, because end of file can be reached when trying to read
            if not self.block.is_empty():
                self.block.current_size -= RECORD_SIZE
                return self.block.records.pop(0)

    def read_block_from_file(self):
        self.fileHandler.read_block(self)

    def save_block_to_file(self):
        self.fileHandler.write_block(self)

    def flush(self):
        if not self.block.is_empty():
            self.save_block_to_file()

    def clear(self):
        self.block.clear()
        self.fileHandler.reset()
