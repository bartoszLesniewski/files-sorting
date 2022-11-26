from block import Block
from constans import *
from diskOperationsHandler import DiskOperationsHandler
from record import Record


class Tape:
    """The class representing a tape - a file where records are stored. """
    def __init__(self, filename="tape1.txt"):
        """
        Initializes Tape object.

        :param filename: The name of the file that the tape represents.
        :type filename: str
        """
        self.block = Block()
        self.fileHandler = DiskOperationsHandler(filename)

    def add_record(self, record):
        """
        Adds a new record to the tape. A record can be given in either a serialized or deserialized form.

        :param record: A record in serialized or deserialized form.
        :type record: Record | str
        """
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
        """
        Checks if there is any record left on the tape and fetches it.

        :return: The record that has been fetched.
        :rtype: Record | None
        """
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
        """
        Reads a block containing records from a file.
        """
        self.fileHandler.read_block(self)

    def save_block_to_file(self):
        """
        Writes a block of records to a file.
        """
        self.fileHandler.write_block(self)

    def flush(self):
        """
        Flushes partially filled block by writing it to a file.
        """
        if not self.block.is_empty():
            self.save_block_to_file()

    def clear(self):
        """
        Clears the tape and resets the content and parameters of the associated file.
        """
        self.block.clear()
        self.fileHandler.reset()
