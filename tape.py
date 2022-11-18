from block import Block
from constans import *
from fileHandler import FileHandler


class Tape:
    def __init__(self, filename):
        self.filename = filename
        self.block = Block(self.filename)
        open(filename, "w").close()  # create an empty file or overwrite file if it already exists
        self.fileHandler = FileHandler(self.filename)

    def add_record(self, record):
        if self.block.current_size < MAX_BLOCK_SIZE:
            self.block.records.append(record)
            self.block.current_size += RECORD_SIZE
        else:
            self.save_to_file()
            self.add_record(record)

    def fetch_record(self):
        self.block.current_size -= RECORD_SIZE
        return self.block.records.pop(0)

    def read_from_file(self):
        self.fileHandler.read_block(self)

    def save_to_file(self):
        self.fileHandler.write_block(self)
